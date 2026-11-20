"""Crea esquemas vacíos por sede; conserva El Carmen en public. Ejecutar desde backend."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sqlalchemy import MetaData, inspect, text, select
from sqlalchemy.schema import CreateSchema
from app.db.session import engine
from app.core.sedes import SEDES

TABLES = ['inventario', 'inventario_movimientos', 'clientes','vehiculos','instalaciones','instalacion_detalles','instalacion_novedades',
          'catalogo_instaladores','catalogo_opacidades_polarizado','catalogo_tecnologias_polarizado',
          'catalogo_tipos_factura','catalogo_vidrios_polarizado']

def preparar():
    with engine.begin() as conn:
        conn.execute(text('SELECT pg_advisory_xact_lock(7421981)'))
        original = MetaData()
        original.reflect(conn, schema='public', only=TABLES)
        for sede, config in SEDES.items():
            schema = config['schema']
            if schema == 'public':
                continue
            if inspect(conn).has_schema(schema):
                existentes = set(inspect(conn).get_table_names(schema=schema))
                if not set(TABLES).issubset(existentes):
                    raise RuntimeError(f'Esquema incompleto: {schema}; revisar antes de continuar')
                print(sede, 'ya preparada')
                continue
            conn.execute(CreateSchema(schema))
            nueva = MetaData()
            for tabla in original.sorted_tables:
                copia = tabla.to_metadata(nueva, schema=schema, referred_schema_fn=lambda *args: schema)
                for columna in copia.columns:
                    if columna.primary_key and columna.server_default is not None and 'nextval' in str(columna.server_default.arg):
                        columna.server_default = None
                        columna.autoincrement = True
            nueva.create_all(conn)
            for tabla in original.sorted_tables:
                if tabla.name.startswith('catalogo_'):
                    destino = nueva.tables[f'{schema}.{tabla.name}']
                    conn.execute(destino.insert().from_select(list(tabla.columns.keys()), select(tabla)))
            print(sede, 'preparada sin registros de clientes')

if __name__ == '__main__':
    preparar()
