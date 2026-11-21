from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, insert, update, func
from sqlalchemy.exc import IntegrityError
from app.core.auth import get_current_identity, require_write_access
from app.core.config import get_settings
from app.core.roles import roles_permitidos
from app.core.sedes import SEDES
from app.db.session import SessionLocal, engine
from app.db.soporte_tables import empleados, mensajes, auditoria

router = APIRouter(prefix='/soporte',tags=['soporte'])

def get_soporte_db():
    # Esquema explícito: soporte no cambia de bandeja al seleccionar otra sede.
    with SessionLocal(bind=engine.execution_options(schema_translate_map={})) as db:
        yield db

def identidad_soporte(identity=Depends(get_current_identity)):
    if not identity.email_verified: raise HTTPException(403,detail='Verifica tu cuenta para abrir la conversación.')
    return identity

def es_gerencia(identity, settings, rol):
    return rol == 'gerencia' and 'gerencia' in roles_permitidos(identity.email, settings)

def require_gerencia(identity=Depends(identidad_soporte),settings=Depends(get_settings),x_rol:str|None=Header(default=None)):
    if not es_gerencia(identity, settings, x_rol): raise HTTPException(403,detail='Solo Gerencia puede gestionar esta bandeja.')
    return identity

class Documento(BaseModel):
    model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
    documento:str=Field(pattern=r'^\d{5,15}$')

class Empleado(Documento):
    nombre:str=Field(min_length=2,max_length=120)
    email:str=Field(max_length=254,pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
    sede:str

class Estado(BaseModel):
    model_config=ConfigDict(extra='forbid')
    activo:bool

class Mensaje(BaseModel):
    model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
    solicitud_id:UUID
    texto:str=Field(min_length=1,max_length=2000)

def autorizar_conversacion(db, ident, identity, gerente, bloquear=False):
    q=select(empleados).where(empleados.c.id==str(ident))
    if bloquear: q=q.with_for_update()
    empleado=db.execute(q).mappings().first()
    if not empleado or (not gerente and (empleado['email']!=identity.email.lower() or not empleado['activo'])):
        raise HTTPException(404,detail='La conversación no está disponible para esta cuenta.')
    return empleado

@router.post('/verificar')
def verificar(payload:Documento,identity=Depends(identidad_soporte),db=Depends(get_soporte_db)):
    e=db.execute(select(empleados.c.id,empleados.c.nombre).where(empleados.c.documento==payload.documento,empleados.c.email==identity.email.lower(),empleados.c.activo.is_(True))).mappings().first()
    if not e: raise HTTPException(403,detail='No pudimos verificar tu acceso. Confirma tu cédula y tu cuenta con Gerencia.')
    return {'conversacion_id':e['id'],'nombre':e['nombre']}

@router.get('/gerencia/empleados')
def listar_empleados(q:str=Query(default='',max_length=120),offset:int=Query(default=0,ge=0),identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
    consulta=select(empleados)
    if q: consulta=consulta.where(empleados.c.nombre.ilike('%'+q+'%')|empleados.c.documento.contains(q)|empleados.c.email.ilike('%'+q+'%'))
    filas=db.execute(consulta.order_by(empleados.c.nombre,empleados.c.id).offset(offset).limit(101)).mappings().all()
    return {'empleados':[dict(e) for e in filas[:100]],'hay_mas':len(filas)>100}

@router.post('/gerencia/empleados',dependencies=[Depends(require_write_access)])
def crear_empleado(payload:Empleado,identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
    if payload.sede not in SEDES: raise HTTPException(422,detail='Selecciona una sede válida.')
    ident=str(uuid4())
    try:
        db.execute(insert(empleados).values(id=ident,nombre=payload.nombre,documento=payload.documento,email=payload.email.lower(),sede=payload.sede,activo=True,registrado_por=identity.email))
        db.execute(insert(auditoria).values(empleado_id=ident,actor=identity.email,accion='registrado'))
        db.commit()
    except IntegrityError as exc:
        db.rollback();raise HTTPException(409,detail='La cédula o el correo ya están registrados. Revisa el directorio.') from exc
    return {'id':ident}

@router.put('/gerencia/empleados/{ident}',dependencies=[Depends(require_write_access)])
def estado_empleado(ident:UUID,payload:Estado,identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
    autorizar_conversacion(db,ident,identity,True,bloquear=True)
    db.execute(update(empleados).where(empleados.c.id==str(ident)).values(activo=payload.activo))
    db.execute(insert(auditoria).values(empleado_id=str(ident),actor=identity.email,accion='activado' if payload.activo else 'desactivado'))
    db.commit()
    return {'activo':payload.activo}

@router.get('/gerencia/conversaciones')
def conversaciones(offset:int=Query(default=0,ge=0),identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
    ultima=select(mensajes.c.empleado_id,func.max(mensajes.c.id).label('ultimo_id')).group_by(mensajes.c.empleado_id).subquery()
    filas=db.execute(select(empleados.c.id,empleados.c.nombre,empleados.c.sede,empleados.c.activo,mensajes.c.texto,mensajes.c.created_at,mensajes.c.autor_tipo).join(ultima,ultima.c.empleado_id==empleados.c.id).join(mensajes,mensajes.c.id==ultima.c.ultimo_id).order_by(mensajes.c.id.desc()).offset(offset).limit(51)).mappings().all()
    return {'conversaciones':[dict(e) for e in filas[:50]],'hay_mas':len(filas)>50}

@router.get('/conversaciones/{ident}/mensajes')
def leer(ident:UUID,antes:int|None=Query(default=None,gt=0),despues:int|None=Query(default=None,ge=0),identity=Depends(identidad_soporte),settings=Depends(get_settings),x_rol:str|None=Header(default=None),db=Depends(get_soporte_db)):
    autorizar_conversacion(db,ident,identity,es_gerencia(identity,settings,x_rol))
    q=select(mensajes.c.id,mensajes.c.texto,mensajes.c.autor_tipo,mensajes.c.created_at).where(mensajes.c.empleado_id==str(ident))
    if antes is not None and despues is not None: raise HTTPException(400,detail='Selecciona una dirección para consultar el historial.')
    if antes: q=q.where(mensajes.c.id<antes)
    if despues is not None: q=q.where(mensajes.c.id>despues)
    filas=db.execute(q.order_by(mensajes.c.id.asc() if despues is not None else mensajes.c.id.desc()).limit(51)).mappings().all()
    return {'mensajes':[dict(m) for m in (filas[:50] if despues is not None else reversed(filas[:50]))],'hay_anteriores':despues is None and len(filas)>50,'hay_mas':despues is not None and len(filas)>50}

@router.post('/conversaciones/{ident}/mensajes',dependencies=[Depends(require_write_access)])
def escribir(ident:UUID,payload:Mensaje,identity=Depends(identidad_soporte),settings=Depends(get_settings),x_rol:str|None=Header(default=None),db=Depends(get_soporte_db)):
    gerente=es_gerencia(identity,settings,x_rol)
    autorizar_conversacion(db,ident,identity,gerente,bloquear=True)
    anterior=db.execute(select(mensajes).where(mensajes.c.solicitud_id==str(payload.solicitud_id))).mappings().first()
    tipo='gerencia' if gerente else 'empleado'
    if anterior:
        if anterior['empleado_id']!=str(ident) or anterior['autor_email']!=identity.email or anterior['texto']!=payload.texto or anterior['autor_tipo']!=tipo:
            raise HTTPException(409,detail='Este envío ya fue utilizado. Actualiza la conversación.')
        return {'enviado':True,'id':anterior['id']}
    try:
        resultado=db.execute(insert(mensajes).values(solicitud_id=str(payload.solicitud_id),empleado_id=str(ident),autor_email=identity.email,autor_tipo=tipo,texto=payload.texto))
        ident_mensaje=resultado.inserted_primary_key[0]
        db.commit()
    except IntegrityError as exc:
        db.rollback();raise HTTPException(409,detail='El envío ya está registrado. Actualiza la conversación.') from exc
    return {'enviado':True,'id':ident_mensaje}
