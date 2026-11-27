"""Fichas privadas y rotación con autorización por operación y sede."""
import base64
import binascii
from datetime import datetime, timezone
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, insert, update, MetaData
from sqlalchemy.exc import IntegrityError
from app.api.v1.soporte import get_soporte_db
from app.api.v1.gerencia import auditar, PERFILES, GLOBALES
from app.core.auth import get_current_identity, require_write_access, acceso_sede
from app.core.config import get_settings
from app.core.roles import roles_permitidos
from app.core.sedes import SEDES
from app.db.gerencia_tables import equipo
from app.db.personal_tables import fichas, archivos, traslados
from app.services.personal import sincronizar_instalador

router = APIRouter(prefix='/personal', tags=['personal'])
CAPACIDADES = ['Laterales', 'Panorámicos', 'Parabrisas de camión o buseta', 'Custodias', 'Sunroof', 'PPF', 'Semi-blindaje', 'Windshield', 'Administración', 'Caja y pagos', 'Inventario', 'Lavadero', 'Gestión de personal', 'Soporte técnico']

def acceso(identity=Depends(get_current_identity), settings=Depends(get_settings), x_rol: str|None=Header(None), x_sede: str|None=Header(None)):
 if not identity.email_verified: raise HTTPException(403, 'Correo no verificado.')
 gerente = x_rol == 'gerencia' and 'gerencia' in roles_permitidos(identity.email, settings)
 if not gerente and not (x_rol == 'administrador' and acceso_sede(identity.email,x_rol,x_sede,settings)):
  raise HTTPException(403, 'No tienes acceso al equipo de esta sede.')
 return {'gerente':gerente,'sede':x_sede,'email':identity.email}

def gerente(a=Depends(acceso)):
 if not a['gerente']: raise HTTPException(403, 'Solo Gerencia puede realizar esta acción.')
 return a

def persona(db, ident, lock=False):
 q=select(equipo).where(equipo.c.id==str(ident))
 r=db.execute(q.with_for_update() if lock else q).mappings().first()
 if not r: raise HTTPException(404,'Empleado no encontrado.')
 return dict(r)

def ficha(db, ident):
 r=db.execute(select(fichas).where(fichas.c.empleado_id==str(ident))).mappings().first()
 return dict(r) if r else {'datos':{},'estado':'pendiente','documento':None}

def version(p, revision):
 if p['revision'] != revision: raise HTTPException(409,'La ficha cambió. Actualiza antes de continuar.')

def guardar_ficha(db,p,datos,estado):
 values={'documento':datos.get('documento') or None,'datos':datos,'estado':estado}
 if db.scalar(select(fichas.c.empleado_id).where(fichas.c.empleado_id==p['id'])):
  db.execute(update(fichas).where(fichas.c.empleado_id==p['id']).values(**values))
 else: db.execute(insert(fichas).values(empleado_id=p['id'],**values))

def faltantes(db,p,d):
 fields={'nombres':'nombres','apellidos':'apellidos','documento':'cédula','telefono':'teléfono','grupo_sanguineo':'grupo sanguíneo','eps':'EPS','capacidades':'capacidades'}
 missing=[label for k,label in fields.items() if not d.get(k)]
 if not p['sede'] and p['perfil'] not in GLOBALES: missing.append('sede')
 if not db.scalar(select(archivos.c.tipo).where(archivos.c.empleado_id==p['id'],archivos.c.tipo=='foto')): missing.append('foto')
 return missing

def publico(db,p,completo=False):
 f=ficha(db,p['id']); d=f['datos']; tipos=list(db.scalars(select(archivos.c.tipo).where(archivos.c.empleado_id==p['id'])))
 out={k:p[k] for k in ('id','nombre','email','perfil','sede','revision','es_prueba')}
 out.update(nombre_corto=' '.join([d.get('nombres','').split(' ')[0],d.get('apellidos','').split(' ')[0]]).strip() or p['nombre'],
  estado=f['estado'] if p['activo'] else ('pendiente' if f['estado']=='pendiente' else 'inactivo'),
  telefono=d.get('telefono',''),capacidades=d.get('capacidades',[]),foto='foto' in tipos)
 if completo: out.update(datos=d,archivos=tipos,faltantes=faltantes(db,p,d))
 return out

class Datos(BaseModel):
 model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
 nombres:str=Field(default='',max_length=80)
 apellidos:str=Field(default='',max_length=80)
 documento:str=Field(default='',pattern=r'^\d{0,20}$')
 telefono:str=Field(default='',max_length=25,pattern=r'^[+\d ()-]*$')
 grupo_sanguineo:str=Field(default='',pattern=r'^(|A\+|A-|B\+|B-|AB\+|AB-|O\+|O-)$')
 eps:str=Field(default='',max_length=100)
 capacidades:list[str]=Field(default_factory=list,max_length=30)
 contacto_emergencia:str=Field(default='',max_length=120)
 telefono_emergencia:str=Field(default='',max_length=25)
 revision:int=Field(ge=1)
 motivo:str=Field(min_length=3,max_length=300)

class Estado(BaseModel):
 model_config=ConfigDict(extra='forbid')
 activo:bool
 revision:int=Field(ge=1)
 motivo:str=Field(min_length=3,max_length=300)

@router.get('/catalogo')
def catalogo(a=Depends(acceso)):
 return {'sedes':[{'id':k,'nombre':v['nombre']} for k,v in SEDES.items()], 'capacidades':CAPACIDADES,'perfiles':PERFILES,'gerente':a['gerente']}

@router.get('/empleados')
def listar(sede:str|None=None,q:str=Query('',max_length=100),disponibles:bool=False,offset:int=Query(0,ge=0),a=Depends(acceso),db=Depends(get_soporte_db)):
 query=select(equipo)
 if not a['gerente'] and not disponibles: query=query.where(equipo.c.sede==a['sede'])
 elif sede: query=query.where(equipo.c.sede==sede)
 if disponibles and not a['gerente']:
  query=query.join(fichas,fichas.c.empleado_id==equipo.c.id).where(equipo.c.sede!=a['sede'],equipo.c.activo.is_(True),fichas.c.estado=='activo')
 if q: query=query.where(equipo.c.nombre.ilike('%'+q+'%'))
 rows=db.execute(query.order_by(equipo.c.nombre,equipo.c.id).limit(51).offset(offset)).mappings().all()
 result=[publico(db,r) for r in rows[:50]]
 if disponibles and not a['gerente']:
  result=[{k:v for k,v in r.items() if k not in ('email','telefono')} for r in result]
 return {'empleados':result,'hay_mas':len(rows)>50}

@router.get('/empleados/{ident}')
def detalle(ident:UUID,a=Depends(acceso),db=Depends(get_soporte_db)):
 p=persona(db,ident)
 if not a['gerente'] and p['sede']!=a['sede']: raise HTTPException(404,'Empleado no encontrado en esta sede.')
 return publico(db,p,a['gerente'])

@router.put('/empleados/{ident}/ficha',dependencies=[Depends(require_write_access)])
def editar(ident:UUID,payload:Datos,a=Depends(gerente),db=Depends(get_soporte_db)):
 p=persona(db,ident,True);version(p,payload.revision);prev=ficha(db,ident)
 d=payload.model_dump(exclude={'revision','motivo'})
 if any(c not in CAPACIDADES for c in d['capacidades']): raise HTTPException(422,'Selecciona capacidades del catálogo.')
 nombre=' '.join([d['nombres'],d['apellidos']]).strip() or p['nombre']
 if len(nombre)>120: raise HTTPException(422,'El nombre completo admite hasta 120 caracteres.')
 if prev['estado']=='activo' and faltantes(db,p,d): raise HTTPException(422,'Completa los datos obligatorios o desactiva primero al empleado.')
 try:
  guardar_ficha(db,p,d,prev['estado']);db.execute(update(equipo).where(equipo.c.id==p['id']).values(nombre=nombre,revision=p['revision']+1))
  auditar(db,p['id'],a['email'],'ficha_actualizada',payload.motivo,prev['datos'],d);db.commit()
 except IntegrityError as exc: db.rollback();raise HTTPException(409,'Esta cédula ya pertenece a otro empleado.') from exc
 return publico(db,persona(db,ident),True)

@router.put('/empleados/{ident}/estado',dependencies=[Depends(require_write_access)])
def estado(ident:UUID,payload:Estado,a=Depends(gerente),db=Depends(get_soporte_db)):
 p=persona(db,ident,True);version(p,payload.revision);f=ficha(db,ident)
 missing=faltantes(db,p,f['datos'])
 if payload.activo and missing: raise HTTPException(422,'Falta completar: '+', '.join(missing)+'.')
 nuevo='activo' if payload.activo else 'inactivo'
 sincronizar_instalador(db,p,p['sede'],payload.activo,a['email'])
 guardar_ficha(db,p,f['datos'],nuevo)
 db.execute(update(equipo).where(equipo.c.id==p['id']).values(activo=payload.activo,revision=p['revision']+1))
 auditar(db,p['id'],a['email'],'personal_'+nuevo,payload.motivo,{'estado':f['estado']},{'estado':nuevo});db.commit()
 return publico(db,persona(db,ident),True)

class Archivo(BaseModel):
 model_config=ConfigDict(extra='forbid')
 contenido:str=Field(max_length=11200000)
 revision:int=Field(ge=1)

@router.put('/empleados/{ident}/archivos/{tipo}',dependencies=[Depends(require_write_access)])
def subir(ident:UUID,tipo:str,payload:Archivo,a=Depends(gerente),db=Depends(get_soporte_db)):
 if tipo not in ('foto','hoja_vida','contrato'): raise HTTPException(422,'Tipo de archivo inválido.')
 p=persona(db,ident,True);version(p,payload.revision)
 try: data=base64.b64decode(payload.contenido,validate=True)
 except (ValueError,binascii.Error) as exc: raise HTTPException(422,'Archivo inválido.') from exc
 if not data or len(data)>(2 if tipo=='foto' else 8)*1024*1024: raise HTTPException(422,'Máximo 2 MB por foto y 8 MB por documento.')
 mime='image/png' if data.startswith(b'\x89PNG\r\n\x1a\n') else 'image/jpeg' if data.startswith(b'\xff\xd8\xff') else 'application/pdf' if data.startswith(b'%PDF-') else None
 if not mime or (tipo=='foto' and mime=='application/pdf'): raise HTTPException(422,'Usa JPG o PNG para la foto; PDF, JPG o PNG para documentos.')
 values={'contenido':data,'mime':mime,'created_at':datetime.now(timezone.utc)}
 where=(archivos.c.empleado_id==p['id']) & (archivos.c.tipo==tipo)
 if db.scalar(select(archivos.c.tipo).where(where)): db.execute(update(archivos).where(where).values(**values))
 else: db.execute(insert(archivos).values(empleado_id=p['id'],tipo=tipo,**values))
 db.execute(update(equipo).where(equipo.c.id==p['id']).values(revision=p['revision']+1))
 auditar(db,p['id'],a['email'],'archivo_cargado','Carga de '+tipo,None,{'tipo':tipo,'bytes':len(data)});db.commit()
 return publico(db,persona(db,ident),True)

@router.get('/empleados/{ident}/archivos/{tipo}')
def descargar(ident:UUID,tipo:str,a=Depends(acceso),db=Depends(get_soporte_db)):
 p=persona(db,ident)
 if not a['gerente'] and (tipo!='foto' or p['sede']!=a['sede']): raise HTTPException(403,'Archivo reservado a Gerencia.')
 r=db.execute(select(archivos).where(archivos.c.empleado_id==p['id'],archivos.c.tipo==tipo)).mappings().first()
 if not r: raise HTTPException(404,'Archivo no cargado.')
 return Response(r['contenido'],media_type=r['mime'],headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Content-Disposition':'attachment; filename="'+tipo+({'image/png':'.png','image/jpeg':'.jpg','application/pdf':'.pdf'}[r['mime']])+'"'})

class Solicitud(BaseModel):
 model_config=ConfigDict(extra='forbid')
 empleado_id:UUID
 destino:str
 motivo:str=Field(min_length=3,max_length=300)

@router.post('/traslados',dependencies=[Depends(require_write_access)])
def solicitar(payload:Solicitud,a=Depends(acceso),db=Depends(get_soporte_db)):
 if payload.destino not in SEDES or (not a['gerente'] and payload.destino!=a['sede']): raise HTTPException(403,'Solo puedes solicitar empleados para tu sede.')
 p=persona(db,payload.empleado_id,True)
 if not p['sede'] or p['sede']==payload.destino or not p['activo'] or ficha(db,p['id'])['estado']!='activo': raise HTTPException(422,'Selecciona un empleado activo en otra sede.')
 if db.scalar(select(traslados.c.id).where(traslados.c.empleado_id==p['id'],traslados.c.estado=='pendiente')): raise HTTPException(409,'Este empleado ya tiene un traslado pendiente.')
 datos={'id':str(uuid4()),'empleado_id':p['id'],'origen':p['sede'],'destino':payload.destino,'solicitante':a['email'],'motivo':payload.motivo,'estado':'pendiente'}
 db.execute(insert(traslados).values(**datos));auditar(db,p['id'],a['email'],'traslado_solicitado',payload.motivo,None,datos);db.commit();return datos

@router.get('/traslados')
def solicitudes(offset:int=Query(0,ge=0),a=Depends(acceso),db=Depends(get_soporte_db)):
 q=select(traslados,equipo.c.nombre).join(equipo,equipo.c.id==traslados.c.empleado_id)
 if not a['gerente']: q=q.where((traslados.c.origen==a['sede'])|(traslados.c.destino==a['sede']))
 rows=db.execute(q.order_by(traslados.c.created_at.desc(),traslados.c.id).offset(offset).limit(51)).mappings().all()
 return {'traslados':[dict(r) for r in rows[:50]],'hay_mas':len(rows)>50}

class Resolucion(BaseModel):
 model_config=ConfigDict(extra='forbid')
 aprobar:bool
 motivo:str=Field(min_length=3,max_length=300)

@router.put('/traslados/{ident}',dependencies=[Depends(require_write_access)])
def resolver(ident:UUID,payload:Resolucion,a=Depends(gerente),db=Depends(get_soporte_db)):
 # Bloqueo de empleado antes de solicitud: mismo orden que solicitar.
 r=db.execute(select(traslados).where(traslados.c.id==str(ident))).mappings().first()
 if not r: raise HTTPException(404,'Solicitud no encontrada.')
 p=persona(db,r['empleado_id'],True)
 r=db.execute(select(traslados).where(traslados.c.id==str(ident)).with_for_update()).mappings().one()
 if r['estado']!='pendiente': raise HTTPException(409,'La solicitud ya fue resuelta.')
 if payload.aprobar:
  if p['sede']!=r['origen'] or not p['activo'] or ficha(db,p['id'])['estado']!='activo': raise HTTPException(409,'La asignación cambió. Rechaza esta solicitud y crea una nueva.')
  sincronizar_instalador(db,p,r['destino'],True,a['email'])
  db.execute(update(equipo).where(equipo.c.id==p['id']).values(sede=r['destino'],revision=p['revision']+1))
 valores={'estado':'aprobado' if payload.aprobar else 'rechazado','resuelto_por':a['email'],'respuesta':payload.motivo,'resuelto_at':datetime.now(timezone.utc)}
 db.execute(update(traslados).where(traslados.c.id==str(ident)).values(**valores))
 auditar(db,p['id'],a['email'],'traslado_'+valores['estado'],payload.motivo,{'sede':r['origen']},{'sede':r['destino'] if payload.aprobar else r['origen'],'solicitud':str(ident)});db.commit()
 return {'estado':valores['estado']}
