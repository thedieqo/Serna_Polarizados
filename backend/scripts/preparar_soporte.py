"""Crea el directorio de contacto y chat interno sin copiar datos de clientes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text
from app.db.session import engine
from app.db.soporte_tables import metadata

def preparar():
    with engine.begin() as conn:
        conn.execute(text('SELECT pg_advisory_xact_lock(7421984)'))
        metadata.create_all(conn)
        for tabla in metadata.sorted_tables:
            conn.execute(text(f'ALTER TABLE public."{tabla.name}" ENABLE ROW LEVEL SECURITY'))
        print('Directorio, historial de mensajes y auditoría preparados con RLS.')

if __name__=='__main__': preparar()
