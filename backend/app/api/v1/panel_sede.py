"""Indicadores y consultas de Gerencia limitados a la sede autorizada."""
from datetime import datetime,timezone,date
from uuid import UUID,uuid4
from pydantic import BaseModel,ConfigDict,Field
from typing import Literal
from zoneinfo import ZoneInfo
from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy import select,func,case,insert,update
from app.api.v1.soporte import require_gerencia,get_soporte_db
from app.core.auth import require_sede,require_role_access,require_write_access
from app.db.session import get_db
from app.db.gerencia_tables import pendientes_sede
from app.api.v1.gerencia import auditar
from app.db.registro_tables import instalaciones,vehiculos,instalacion_novedades as novedades
router=APIRouter(prefix='/sede',tags=['panel_sede'],dependencies=[Depends(require_sede),Depends(require_role_access),Depends(require_gerencia)])
BOGOTA=ZoneInfo('America/Bogota')

def resumen(db,ahora=None):
 ahora=ahora or datetime.now(timezone.utc)
 local=ahora.astimezone(BOGOTA);inicio=local.replace(day=1,hour=0,minute=0,second=0,microsecond=0).astimezone(timezone.utc)
 filtro=(instalaciones.c.fecha>=inicio,instalaciones.c.fecha<=ahora,instalaciones.c.estado!='anulado')
 venta=db.execute(select(func.coalesce(func.sum(instalaciones.c.precio_total_cop),0).label('ventas_cop'),func.count().label('instalaciones_mes'),func.coalesce(func.sum(case((instalaciones.c.precio_total_cop.is_(None),1),else_=0)),0).label('sin_precio')).where(*filtro)).mappings().one()
 garantias=db.scalar(select(func.count()).select_from(novedades).where(novedades.c.fecha_atencion>=inicio,novedades.c.fecha_atencion<=ahora))
 return dict(venta)|{'garantias_mes':garantias,'mes':local.strftime('%Y-%m'),'actualizado_en':ahora}

@router.get('/resumen')
def inicio(sede=Depends(require_sede),db=Depends(get_db),central=Depends(get_soporte_db)):
 datos=resumen(db)
 datos['pendientes']=central.scalar(select(func.count()).select_from(pendientes_sede).where(pendientes_sede.c.sede==sede,pendientes_sede.c.completado.is_(False)))
 return datos

@router.get('/pendientes')
def pendientes(offset:int=Query(0,ge=0),completados:bool=False,sede=Depends(require_sede),db=Depends(get_soporte_db)):
 q=select(pendientes_sede).where(pendientes_sede.c.sede==sede,pendientes_sede.c.completado==completados).order_by(pendientes_sede.c.vencimiento,pendientes_sede.c.id)
 rows=db.execute(q.offset(offset).limit(21)).mappings().all()
 return {'registros':[dict(r) for r in rows[:20]],'hay_mas':len(rows)>20}

class Pendiente(BaseModel):
 model_config=ConfigDict(extra='forbid',str_strip_whitespace=True)
 titulo:str=Field(min_length=3,max_length=150)
 categoria:Literal['contrato','luz','agua','internet','otro']
 vencimiento:date

@router.post('/pendientes',dependencies=[Depends(require_write_access)])
def crear_pendiente(payload:Pendiente,sede=Depends(require_sede),identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
 ident=str(uuid4());datos=payload.model_dump()|{'id':ident,'sede':sede,'completado':False,'revision':1,'creado_por':identity.email}
 db.execute(insert(pendientes_sede).values(**datos))
 auditar(db,ident,identity.email,'pendiente_creado','Registro de pendiente administrativo de sede',None,datos|{'vencimiento':payload.vencimiento.isoformat()});db.commit()
 return datos

class ResolverPendiente(BaseModel):
 model_config=ConfigDict(extra='forbid')
 completado:bool
 revision:int=Field(ge=1)

@router.put('/pendientes/{ident}',dependencies=[Depends(require_write_access)])
def resolver_pendiente(ident:UUID,payload:ResolverPendiente,sede=Depends(require_sede),identity=Depends(require_gerencia),db=Depends(get_soporte_db)):
 r=db.execute(select(pendientes_sede).where(pendientes_sede.c.id==str(ident),pendientes_sede.c.sede==sede).with_for_update()).mappings().first()
 if not r:raise HTTPException(404,detail='Pendiente no encontrado en esta sede.')
 if r['revision']!=payload.revision:raise HTTPException(409,detail='El pendiente cambió. Actualiza para continuar.')
 db.execute(update(pendientes_sede).where(pendientes_sede.c.id==str(ident)).values(completado=payload.completado,revision=r['revision']+1))
 auditar(db,str(ident),identity.email,'pendiente_completado' if payload.completado else 'pendiente_reabierto',r['titulo'],{'sede':sede,'completado':r['completado']},{'sede':sede,'completado':payload.completado});db.commit()
 return {'completado':payload.completado,'revision':r['revision']+1}

@router.get('/garantias')
def garantias(offset:int=Query(0,ge=0),db=Depends(get_db)):
 q=select(novedades,vehiculos.c.placa).join(instalaciones,novedades.c.instalacion_id==instalaciones.c.id).join(vehiculos,vehiculos.c.id==instalaciones.c.vehiculo_id).order_by(novedades.c.fecha_atencion.desc(),novedades.c.id.desc())
 rows=db.execute(q.offset(offset).limit(21)).mappings().all()
 return {'registros':[dict(r) for r in rows[:20]],'hay_mas':len(rows)>20}
