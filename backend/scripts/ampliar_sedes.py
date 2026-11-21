"""Migración acotada a tres nuevas sedes. Sin --apply solo muestra el plan."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from uuid import uuid4
from sqlalchemy import MetaData,inspect,text,select,insert
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import Session
from app.db.session import engine
from app.core.sedes import SEDES
from app.db.gerencia_tables import equipo,actividad
from app.services.inventario import inicializar
from preparar_sedes import TABLES
NUEVAS=('7-de-agosto','porvenir','santo-tomas')

def ejecutar(aplicar=False):
 with engine.begin() as conn:
  conn.execute(text('SELECT pg_advisory_xact_lock(7421981)'))
  original=MetaData();original.reflect(conn,schema='public',only=TABLES)
  for sede in NUEVAS:
   schema=SEDES[sede]['schema'];existe=inspect(conn).has_schema(schema)
   if existe and not set(TABLES).issubset(set(inspect(conn).get_table_names(schema=schema))):raise RuntimeError('Sede incompleta: '+sede)
   print(sede,'ya preparada' if existe else 'crear esquema vacío, catálogos, RLS e inventario inicial')
   if not aplicar:continue
   if not existe:
    conn.execute(CreateSchema(schema));nueva=MetaData()
    for tabla in original.sorted_tables:
     copia=tabla.to_metadata(nueva,schema=schema,referred_schema_fn=lambda *args:schema)
     for columna in copia.columns:
      if columna.primary_key and columna.server_default is not None and 'nextval' in str(columna.server_default.arg):columna.server_default=None;columna.autoincrement=True
    nueva.create_all(conn)
    for tabla in original.sorted_tables:
     if tabla.name.startswith('catalogo_'):
      destino=nueva.tables[f'{schema}.{tabla.name}'];conn.execute(destino.insert().from_select(list(tabla.columns.keys()),select(tabla)))
    for tabla in TABLES:conn.execute(text(f'ALTER TABLE "{schema}"."{tabla}" ENABLE ROW LEVEL SECURITY'))
    conn.execution_options(schema_translate_map={None:schema})
    with Session(bind=conn,join_transaction_mode='create_savepoint') as db:inicializar(db);db.commit()
    conn.execution_options(schema_translate_map={})
   for rol,label,sufijo in [('administrador','Administrador','administrador'),('instalador','Instalador 1','instalador1'),('instalador','Instalador 2','instalador2'),('instalador_ppf','Instalador PPF','ppf'),('auxiliar_administrativo','Auxiliar administrativo','auxiliar')]:
    email=sufijo+'.'+sede+'@serna.example.invalid'
    if conn.execute(select(equipo.c.id).where(equipo.c.email==email)).first():continue
    r=dict(id=str(uuid4()),nombre=label+' · '+SEDES[sede]['nombre'],email=email,perfil=rol,sede=sede,activo=True,es_prueba=True,revision=1)
    conn.execute(insert(equipo).values(**r));conn.execute(insert(actividad).values(empleado_id=r['id'],actor='configuracion-inicial',accion='creado',motivo='Ampliación autorizada a 14 sedes; perfil ficticio sin acceso',antes=None,despues=r))
  print('Migración aplicada.' if aplicar else 'Plan verificado: no se modificaron datos. Use --apply para aplicar.')
if __name__=='__main__':ejecutar('--apply' in sys.argv)
