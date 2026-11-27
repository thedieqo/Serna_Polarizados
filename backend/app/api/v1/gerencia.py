"""Gestión central para Gerencia, independiente de la sede seleccionada."""
from datetime import datetime,timezone
from uuid import UUID,uuid4
from fastapi import APIRouter,Depends,HTTPException,Query
from pydantic import BaseModel,ConfigDict,Field,model_validator
from sqlalchemy import select,insert,update,func,Integer,case
from sqlalchemy.exc import IntegrityError
from app.api.v1.soporte import get_soporte_db,require_gerencia
from app.core.auth import require_write_access
from app.core.sedes import SEDES
from app.db.gerencia_tables import equipo,actividad,sedes_nuevas
import unicodedata

router=APIRouter(prefix='/gerencia/gestion',tags=['gerencia'],dependencies=[Depends(require_gerencia)])
PERFILES={'gerencia':'Gerencia','auxiliar_gerencia':'Auxiliar de gerencia','propietario':'Dueño','ingeniero':'Ingeniero de pruebas','administrador':'Administrador de sede','instalador':'Instalador','instalador_ppf':'Instalador de PPF','auxiliar_administrativo':'Auxiliar administrativo'}
GLOBALES={'gerencia','auxiliar_gerencia','propietario','ingeniero'}

def sedes_catalogo():
 return [{'id':k,'nombre':v['nombre'],'lavadero':k=='mirolindo','operativa':True} for k,v in SEDES.items()]

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
 from app.db.personal_tables import fichas
 conteos=db.execute(select(equipo.c.sede,func.count().label('total'),func.sum(case(((equipo.c.activo.is_(True)) & (fichas.c.estado=='activo'),1),else_=0)).label('activos')).select_from(equipo.outerjoin(fichas,fichas.c.empleado_id==equipo.c.id)).group_by(equipo.c.sede)).mappings().all()
 nuevas=db.execute(select(sedes_nuevas).order_by(sedes_nuevas.c.created_at)).mappings().all()
 catalogo=sedes_catalogo()+[{'id':r['id'],'nombre':r['nombre']+' ('+r['ciudad']+')','lavadero':False,'operativa':False} for r in nuevas]
 return {'sedes':catalogo,'perfiles':PERFILES,'equipo_por_sede':[dict(x) for x in conteos], 'total_empleados':sum(x['total'] for x in conteos),'activos':sum(x['activos'] or 0 for x in conteos),'modo':'pruebas'}

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
 ident=str(uuid4());datos=payload.model_dump()|{'id':ident,'activo':False,'es_prueba':True,'revision':1}
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
 antes=obtener(db,ident,payload.revision)
 from app.api.v1.personal import ficha
 f=ficha(db,ident)
 if f['estado']=='activo' and any(getattr(payload,k)!=antes[k] for k in ('email','perfil','sede')):
  raise HTTPException(409,detail='Desactiva primero para cambiar correo o cargo. Para cambiar de sede utiliza Traslados.')
 if f['estado']=='activo' and payload.nombre!=antes['nombre']:
  raise HTTPException(409,detail='Actualiza el nombre desde la ficha del empleado.')
 datos=payload.model_dump(exclude={'revision','motivo'});despues=antes|datos|{'revision':antes['revision']+1}
 try:
  db.execute(update(equipo).where(equipo.c.id==str(ident)).values(**datos,revision=despues['revision'],updated_at=datetime.now(timezone.utc)))
  auditar(db,str(ident),identity.email,'modificado',payload.motivo,antes,despues);db.commit()
 except IntegrityError as exc:
  db.rollback();raise HTTPException(409,detail='Este correo ya está registrado.') from exc
 return despues

@router.put('/empleados/{ident}/estado',dependencies=[Depends(require_write_access)])
def estado(ident:UUID,payload:Estado,identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
 from app.api.v1.personal import estado as cambiar, Estado as EstadoPersonal
 return cambiar(ident,EstadoPersonal(**payload.model_dump()),{'email':identity.email,'gerente':True},db)

@router.get('/actividad')
def historial(empleado_id:UUID|None=None,offset:int=Query(0,ge=0),db=Depends(get_soporte_db)):
 q=select(actividad,equipo.c.nombre.label('empleado_nombre')).outerjoin(equipo,equipo.c.id==actividad.c.empleado_id)
 if empleado_id:q=q.where(actividad.c.empleado_id==str(empleado_id))
 filas=db.execute(q.order_by(actividad.c.id.desc()).offset(offset).limit(51)).mappings().all()
 return {'actividad':[dict(r) for r in filas[:50]],'hay_mas':len(filas)>50}


class NuevaSede(BaseModel):
 model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
 nombre:str=Field(min_length=2,max_length=100)
 ciudad:str=Field(min_length=2,max_length=100)

def clave_sede(nombre):
 return ''.join(c for c in unicodedata.normalize('NFKD',nombre.casefold()) if c.isalnum())

@router.post('/sedes',dependencies=[Depends(require_write_access)])
def crear_sede(payload:NuevaSede,identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
 etiqueta=payload.nombre+' ('+payload.ciudad+')';clave=clave_sede(etiqueta)
 if any(clave_sede(s['nombre'])==clave for s in SEDES.values()):
  raise HTTPException(409,detail='Esta sede ya está registrada.')
 ident=str(uuid4())
 try:
  db.execute(insert(sedes_nuevas).values(id=ident,nombre=payload.nombre,ciudad=payload.ciudad,clave=clave,creado_por=identity.email))
  auditar(db,ident,identity.email,'sede_creada','Registro de sede; funciones operativas pendientes',None,{'nombre':etiqueta,'operativa':False});db.commit()
 except IntegrityError as exc:
  db.rollback();raise HTTPException(409,detail='Esta sede ya está registrada.') from exc
 return {'id':ident,'nombre':etiqueta,'operativa':False,'lavadero':False}
