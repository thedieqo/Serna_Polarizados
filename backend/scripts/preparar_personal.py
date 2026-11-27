"""Migración aditiva, plan por defecto. No cambia accesos ni borra empleados."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text
from app.db.session import engine
from app.db.personal_tables import fichas, archivos, traslados

def preparar(aplicar=False):
 tablas=[fichas,archivos,traslados]
 print('Crear si faltan: '+', '.join(t.name for t in tablas)+'. Archivos privados con RLS. Sin cambios a registros existentes.')
 if not aplicar:return
 with engine.begin() as c:
  c.execute(text('SELECT pg_advisory_xact_lock(7421986)'))
  for t in tablas:
   t.create(c,checkfirst=True)
   c.execute(text(f'ALTER TABLE public."{t.name}" ENABLE ROW LEVEL SECURITY'))
 print('Extensión de personal preparada.')
if __name__=='__main__':preparar('--apply' in sys.argv)
