"""Carga inicial explícita por sede. No descuenta instalaciones históricas."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import engine
from app.db.registro_tables import metadata, inventario, inventario_movimientos
from app.core.sedes import SEDES
from app.services.inventario import inicializar
with engine.begin() as conn:
    conn.execute(text('SELECT pg_advisory_xact_lock(7421982)'))
    for sede, config in SEDES.items():
        conn.execution_options(schema_translate_map={None:config['schema']})
        metadata.create_all(conn,tables=[inventario,inventario_movimientos])
        for tabla in ['inventario','inventario_movimientos']:
            conn.execute(text(f'ALTER TABLE "{config["schema"]}"."{tabla}" ENABLE ROW LEVEL SECURITY'))
        with Session(bind=conn,join_transaction_mode='create_savepoint') as db:
            inicializar(db)
            db.commit()
        print(sede, 'inventario preparado')
