import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text
from app.db.session import engine
from app.db.gerencia_tables import sedes_datos,pendientes_sede
if __name__=='__main__':
 print('Crear tabla privada de direcciones, sin modificar direcciones ni registros existentes.')
 if '--apply' in sys.argv:
  with engine.begin() as c:
   for t in (sedes_datos,pendientes_sede):
    t.create(c,checkfirst=True)
    c.execute(text(f'ALTER TABLE public.{t.name} ENABLE ROW LEVEL SECURITY'))
  print('Tabla preparada.')
