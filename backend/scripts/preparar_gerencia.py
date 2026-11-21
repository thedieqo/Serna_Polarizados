"""Inicializa directorio de prueba de Gerencia sin habilitar nuevas cuentas."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from uuid import uuid4
from sqlalchemy import text,select,insert
from app.db.session import engine
from app.db.gerencia_tables import metadata,equipo,actividad
from app.core.sedes import SEDES

def preparar():
 with engine.begin() as c:
  c.execute(text('SELECT pg_advisory_xact_lock(7421985)'))
  metadata.create_all(c)
  for t in metadata.sorted_tables:c.execute(text(f'ALTER TABLE public."{t.name}" ENABLE ROW LEVEL SECURITY'))
  # Un marcador evita reponer empleados de prueba borrados/desactivados o editados.
  if c.execute(select(actividad.c.id).where(actividad.c.accion=='inicializacion')).first():
   print('Directorio ya inicializado. No se alteraron empleados.');return
  rows=[]
  for rol,nombre in [('gerencia','Gerencia'),('auxiliar_gerencia','Auxiliar de gerencia'),('propietario','Dueño'),('ingeniero','Ingeniero de pruebas')]:
   rows.append(dict(nombre=nombre+' · Prueba',email=rol+'@serna.example.invalid',perfil=rol,sede=None))
  for sede,config in SEDES.items():
   for rol,label,sufijo in [('administrador','Administrador','administrador'),('instalador','Instalador 1','instalador1'),('instalador','Instalador 2','instalador2'),('instalador_ppf','Instalador PPF','ppf'),('auxiliar_administrativo','Auxiliar administrativo','auxiliar')]:
    rows.append(dict(nombre=label+' · '+config['nombre'],email=sufijo+'.'+sede+'@serna.example.invalid',perfil=rol,sede=sede))
  for r in rows:
   if c.execute(select(equipo.c.id).where(equipo.c.email==r['email'])).first():continue
   r.update(id=str(uuid4()),activo=True,es_prueba=True,revision=1)
   c.execute(insert(equipo).values(**r));c.execute(insert(actividad).values(empleado_id=r['id'],actor='configuracion-inicial',accion='creado',motivo='Perfil ficticio solicitado para pruebas; no habilita acceso',antes=None,despues=r))
  c.execute(insert(actividad).values(empleado_id='configuracion',actor='configuracion-inicial',accion='inicializacion',motivo='Directorio inicial de pruebas preparado',antes=None,despues={'cantidad':len(rows)}))
  print(f'Directorio preparado: {len(rows)} perfiles ficticios. Las cuentas de acceso siguen sin cambios.')
if __name__=='__main__':preparar()
