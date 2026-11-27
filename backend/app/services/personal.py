"""Mantiene las asignaciones operativas ya aprobadas sin otorgar accesos nuevos."""
from uuid import uuid4
from sqlalchemy import MetaData,select,insert,update
from app.core.sedes import SEDES
from app.db.registro_tables import trabajadores,trabajador_auditoria

def sincronizar_instalador(db,persona,sede,activo,actor):
 # Solo replica una cuenta que ya fue aprobada en el módulo de instaladores.
 # Los documentos o la activación del directorio no conceden acceso por sí solos.
 tablas=[];encontrado=False
 for clave,config in SEDES.items():
  meta=MetaData();t=trabajadores.to_metadata(meta,schema=config['schema'])
  audit=trabajador_auditoria.to_metadata(meta,schema=config['schema'])
  r=db.execute(select(t).where(t.c.email==persona['email']).with_for_update()).mappings().first()
  tablas.append((clave,t,audit,r));encontrado=encontrado or bool(r)
 if not encontrado:return
 for clave,t,audit,r in tablas:
  activar=activo and clave==sede and persona['perfil'] in ('instalador','instalador_ppf')
  if r:
   if r['activo']==activar and (not activar or r['nombre']==persona['nombre']):continue
   db.execute(update(t).where(t.c.id==r['id']).values(activo=activar,nombre=persona['nombre'] if activar else r['nombre'],aprobado_por=actor))
   db.execute(insert(audit).values(trabajador_id=r['id'],actor=actor,accion='personal_activado' if activar else 'personal_desactivado'))
  elif activar:
   ident=str(uuid4());db.execute(insert(t).values(id=ident,nombre=persona['nombre'],email=persona['email'],activo=True,aprobado_por=actor))
   db.execute(insert(audit).values(trabajador_id=ident,actor=actor,accion='personal_trasladado'))
