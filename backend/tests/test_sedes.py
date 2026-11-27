import asyncio
from unittest import TestCase
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from app.core.auth import require_sede
from app.core.sedes import SEDES, permitidas
from app.core.config import Settings
from app.core.token_verifier import VerifiedIdentity
from app.db.registro_tables import instalaciones

class SedesTests(TestCase):
    def setUp(self):
        self.settings=Settings(ADMIN_EMAILS='uno@example.com,dos@example.com,tres@example.com')
    def identity(self,email,verified=True):
        return VerifiedIdentity(email=email,email_verified=verified,subject='test',role='authenticated')
    def test_ibague_ambas(self):
        self.assertEqual(permitidas('uno@example.com',self.settings),['el-carmen','mirolindo'])
    def test_sedes_independientes(self):
        for sede, config in SEDES.items():
            if config['correo']:
                self.assertEqual(permitidas(config['correo'],self.settings),[sede])
                self.assertEqual(asyncio.run(require_sede(sede,self.identity(config['correo']),self.settings)),sede)
                with self.assertRaises(HTTPException):
                    asyncio.run(require_sede('el-carmen',self.identity(config['correo']),self.settings))
    def test_rechaza_sede_manipulada_y_sesion_no_verificada(self):
        for sede, identity in [('public',self.identity('uno@example.com')),('el-carmen',self.identity('uno@example.com',False)),(None,self.identity('uno@example.com'))]:
            with self.assertRaises(HTTPException):
                asyncio.run(require_sede(sede,identity,self.settings))
    def test_sql_calificado_sin_fallback_public(self):
        for config in SEDES.values():
            schema=config['schema']
            sql=str(select(instalaciones).compile(dialect=postgresql.dialect(),schema_translate_map={None:schema},render_schema_translate=True))
            self.assertIn(schema+'.instalaciones',sql)
            if schema!='public': self.assertNotIn('public.instalaciones',sql)

    def test_misma_id_datos_separados(self):
        from sqlalchemy import create_engine, text, insert
        from sqlalchemy.orm import Session
        from app.db.registro_tables import metadata, clientes
        motor=create_engine('sqlite://')
        with motor.connect() as conn:
            for schema in ['sede_cali','sede_pasto']:
                conn.execute(text(f"ATTACH DATABASE ':memory:' AS {schema}"))
            conn.commit()
        for schema, nombre in [('sede_cali','Cliente Cali'),('sede_pasto','Cliente Pasto')]:
            separado=motor.execution_options(schema_translate_map={None:schema})
            metadata.create_all(separado)
            with Session(separado) as db:
                db.execute(insert(clientes).values(id=1,documento='MISMO-DOCUMENTO',nombre=nombre,contacto=''))
                db.commit()
        for schema, nombre in [('sede_cali','Cliente Cali'),('sede_pasto','Cliente Pasto')]:
            with Session(motor.execution_options(schema_translate_map={None:schema})) as db:
                self.assertEqual(db.execute(select(clientes.c.nombre).where(clientes.c.id==1)).scalar_one(),nombre)
        motor.dispose()

    def test_api_rechaza_sede_ajena_antes_de_consultar(self):
        from fastapi.testclient import TestClient
        from app.main import app
        from app.core.auth import get_current_identity
        from app.core.config import get_settings
        app.dependency_overrides[get_current_identity]=lambda: self.identity('calisp@gmail.com')
        app.dependency_overrides[get_settings]=lambda: self.settings
        try:
            with TestClient(app) as cliente:
                for ruta in ['/api/v1/instalaciones/historial','/api/v1/clientes/','/api/v1/vehiculos/','/api/v1/instalaciones/1/detalle','/api/v1/instalaciones/ventas/resumen?anio=2026&mes=11']:
                    self.assertEqual(cliente.get(ruta,headers={'X-Sede':'pasto'}).status_code,403)
                self.assertEqual(cliente.get('/api/v1/instalaciones/historial').status_code,400)
        finally:
            app.dependency_overrides.clear()

    def test_correo_el_carmen_exclusivo_y_revocable(self):
        email='sernapolarizadosibague.1@gmail.com'
        settings=Settings(ADMIN_EMAILS=email+',uno@example.com')
        self.assertEqual(permitidas(email.upper(),settings),['el-carmen'])
        self.assertEqual(permitidas(email,self.settings),[])
        self.assertEqual(permitidas('uno@example.com',settings),['el-carmen','mirolindo'])
        from app.core.auth import acceso_sede,accesos_identidad
        from unittest.mock import patch
        self.assertTrue(acceso_sede(email,'administrador','el-carmen',settings))
        for rol in ['administrador','instalador','gerencia','propietario']:
            self.assertFalse(acceso_sede(email,rol,'mirolindo',settings))
        with patch('app.core.auth.sedes_instalador_aprobado',return_value=['mirolindo']):
            r=accesos_identidad(self.identity(email),settings)
        self.assertEqual(r['perfiles'],[{'rol':'administrador','sedes':[{'id':'el-carmen','nombre':'El Carmen (Ibagué)'}]}])

    def test_api_el_carmen_no_puede_cambiar_a_mirolindo(self):
        from fastapi.testclient import TestClient
        from app.main import app
        from app.core.auth import get_current_identity
        from app.core.config import get_settings
        email='sernapolarizadosibague.1@gmail.com'
        app.dependency_overrides[get_current_identity]=lambda:self.identity(email)
        app.dependency_overrides[get_settings]=lambda:Settings(ADMIN_EMAILS=email)
        try:
            with TestClient(app) as cliente:
                h={'X-Rol':'administrador','X-Sede':'el-carmen'}
                self.assertTrue(cliente.get('/api/v1/auth/session',headers=h).json()['authorized'])
                h['X-Sede']='mirolindo'
                self.assertFalse(cliente.get('/api/v1/auth/session',headers=h).json()['authorized'])
                for ruta in ['/api/v1/instalaciones/historial','/api/v1/clientes/','/api/v1/inventario']:
                    self.assertEqual(cliente.get(ruta,headers=h).status_code,403)
        finally:app.dependency_overrides.clear()
