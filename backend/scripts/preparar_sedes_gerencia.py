"""Catálogo administrativo de nuevas sedes. No modifica esquemas operativos."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text
from app.db.session import engine
from app.db.gerencia_tables import sedes_nuevas
if __name__=='__main__':
 print('Crear tabla de fichas de nuevas sedes y protegerla con RLS. Sin cambios a sedes existentes ni accesos.')
 if '--apply' in sys.argv:
  with engine.begin() as c:
   sedes_nuevas.create(c,checkfirst=True)
   c.execute(text('ALTER TABLE public.gerencia_sedes_nuevas ENABLE ROW LEVEL SECURITY'))
  print('Tabla preparada.')
