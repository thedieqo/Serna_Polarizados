"""Migración aditiva: no modifica consumos ni remuneraciones anteriores."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text
from app.db.session import engine
from app.db.registro_tables import metadata, trabajadores, trabajador_auditoria, confirmaciones_trabajo, vidrios_realizados
from app.core.sedes import SEDES

def preparar():
    with engine.begin() as conn:
        conn.execute(text('SELECT pg_advisory_xact_lock(7421983)'))
        for sede, config in SEDES.items():
            schema = config['schema']
            conn.execution_options(schema_translate_map={None:schema})
            nuevas = [trabajadores, trabajador_auditoria, confirmaciones_trabajo, vidrios_realizados]
            metadata.create_all(conn,tables=nuevas)
            for tabla in nuevas:
                conn.execute(text(f'ALTER TABLE "{schema}"."{tabla.name}" ENABLE ROW LEVEL SECURITY'))
            conn.execute(text(f'ALTER TABLE "{schema}".inventario_movimientos ADD COLUMN IF NOT EXISTS confirmacion_id VARCHAR'))
            conn.execute(text(f'CREATE UNIQUE INDEX IF NOT EXISTS inventario_consumo_confirmacion_unico ON "{schema}".inventario_movimientos (confirmacion_id, sku)'))
            conn.execute(text(f'ALTER TABLE "{schema}".inventario_movimientos DROP CONSTRAINT IF EXISTS inventario_consumo_instalacion_unico'))
            print(sede, 'control de trabajo preparado')

if __name__ == '__main__': preparar()
