"""Gestión central para Gerencia, independiente de la sede seleccionada."""
from datetime import datetime,timezone
from uuid import UUID,uuid4
from fastapi import APIRouter,Depends,HTTPException,Query
from pydantic import BaseModel,ConfigDict,Field,model_validator
from sqlalchemy import select,insert,update,func,Integer
from sqlalchemy.exc import IntegrityError
from app.api.v1.soporte import get_soporte_db,require_gerencia
from app.core.auth import require_write_access
from app.core.sedes import SEDES
from app.db.gerencia_tables import equipo,actividad

router=APIRouter(prefix='/gerencia/gestion',tags=['gerencia'],dependencies=[Depends(require_gerencia)])
PERFILES={'gerencia':'Gerencia','auxiliar_gerencia':'Auxiliar de gerencia','propietario':'Dueño','ingeniero':'Ingeniero de pruebas','administrador':'Administrador de sede','instalador':'Instalador','instalador_ppf':'Instalador de PPF','auxiliar_administrativo':'Auxiliar administrativo'}
GLOBALES={'gerencia','auxiliar_gerencia','propietario','ingeniero'}

def sedes_catalogo():
 return [{'id':k,'nombre':v['nombre'],'lavadero':k=='mirolindo'} for k,v in SEDES.items()]

def resumen_empleado(row):
 return {k:row[k] for k in ('id','nombre','email','perfil','sede','activo','es_prueba','revision')}

def auditar(db,ident,actor,accion,motivo,antes,despues):
 db.execute(insert(actividad).values(empleado_id=ident,actor=actor,accion=accion,motivo=motivo,antes=antes,despues=despues))

class Datos(BaseModel):
 model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
 nombre:str=Field(min_length=2,max_length=120)
 email:str=Field(max_length=254,pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
 perfil:str
 sede:str|None=None
 @model_validator(mode='after')
 def validar(self):
  if self.perfil not in PERFILES:raise ValueError('Selecciona un perfil válido.')
  if self.perfil in GLOBALES:
   if self.sede is not None:raise ValueError('Este perfil tiene alcance general.')
  elif self.sede not in SEDES:raise ValueError('Selecciona una sede válida.')
  self.email=self.email.lower()
  return self

class Edicion(Datos):
 revision:int=Field(ge=1)
 motivo:str=Field(min_length=3,max_length=300)

class Estado(BaseModel):
 model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
 activo:bool
 revision:int=Field(ge=1)
 motivo:str=Field(min_length=3,max_length=300)

@router.get('/resumen')
def resumen(db=Depends(get_soporte_db)):
 conteos=db.execute(select(equipo.c.sede,func.count().label('total'),func.sum(equipo.c.activo.cast(Integer)).label('activos')).group_by(equipo.c.sede)).mappings().all()
 return {'sedes':sedes_catalogo(),'perfiles':PERFILES,'equipo_por_sede':[dict(x) for x in conteos], 'total_empleados':sum(x['total'] for x in conteos),'activos':sum(x['activos'] or 0 for x in conteos),'modo':'pruebas'}

@router.get('/empleados')
def listar(q:str=Query('',max_length=120),sede:str|None=None,perfil:str|None=None,offset:int=Query(0,ge=0),db=Depends(get_soporte_db)):
 consulta=select(equipo)
 if sede:consulta=consulta.where(equipo.c.sede==sede) if sede!='general' else consulta.where(equipo.c.sede.is_(None))
 if perfil:consulta=consulta.where(equipo.c.perfil==perfil)
 if q:consulta=consulta.where(equipo.c.nombre.ilike('%'+q+'%')|equipo.c.email.ilike('%'+q+'%'))
 filas=db.execute(consulta.order_by(equipo.c.nombre,equipo.c.id).offset(offset).limit(51)).mappings().all()
 return {'empleados':[resumen_empleado(r) for r in filas[:50]],'hay_mas':len(filas)>50}

@router.post('/empleados',dependencies=[Depends(require_write_access)])
def crear(payload:Datos,identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
 ident=str(uuid4());datos=payload.model_dump()|{'id':ident,'activo':True,'es_prueba':True,'revision':1}
 try:
  db.execute(insert(equipo).values(**datos));auditar(db,ident,identity.email,'creado','Registro de prueba',None,datos);db.commit()
 except IntegrityError as exc:
  db.rollback();raise HTTPException(409,detail='Este correo ya está registrado.') from exc
 return datos

def obtener(db,ident,revision):
 r=db.execute(select(equipo).where(equipo.c.id==str(ident)).with_for_update()).mappings().first()
 if not r:raise HTTPException(404,detail='No encontramos este empleado.')
 if r['revision']!=revision:raise HTTPException(409,detail='Este registro cambió. Actualiza antes de continuar.')
 return resumen_empleado(r)

@router.put('/empleados/{ident}',dependencies=[Depends(require_write_access)])
def editar(ident:UUID,payload:Edicion,identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
 antes=obtener(db,ident,payload.revision);datos=payload.model_dump(exclude={'revision','motivo'});despues=antes|datos|{'revision':antes['revision']+1}
 try:
  db.execute(update(equipo).where(equipo.c.id==str(ident)).values(**datos,revision=despues['revision'],updated_at=datetime.now(timezone.utc)))
  auditar(db,str(ident),identity.email,'modificado',payload.motivo,antes,despues);db.commit()
 except IntegrityError as exc:
  db.rollback();raise HTTPException(409,detail='Este correo ya está registrado.') from exc
 return despues

@router.put('/empleados/{ident}/estado',dependencies=[Depends(require_write_access)])
def estado(ident:UUID,payload:Estado,identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
 antes=obtener(db,ident,payload.revision)
 if antes['activo']==payload.activo:return antes
 despues=antes|{'activo':payload.activo,'revision':antes['revision']+1}
 db.execute(update(equipo).where(equipo.c.id==str(ident)).values(activo=payload.activo,revision=despues['revision'],updated_at=datetime.now(timezone.utc)))
 auditar(db,str(ident),identity.email,'reactivado' if payload.activo else 'desactivado',payload.motivo,antes,despues);db.commit()
 return despues

@router.get('/actividad')
def historial(empleado_id:UUID|None=None,offset:int=Query(0,ge=0),db=Depends(get_soporte_db)):
 q=select(actividad)
 if empleado_id:q=q.where(actividad.c.empleado_id==str(empleado_id))
 filas=db.execute(q.order_by(actividad.c.id.desc()).offset(offset).limit(51)).mappings().all()
 return {'actividad':[dict(r) for r in filas[:50]],'hay_mas':len(filas)>50}
