from unittest import TestCase
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import get_current_identity
from app.core.config import Settings,get_settings
from app.core.roles import CUENTA_PRUEBAS,puede_usar_ruta,roles_permitidos,sedes_perfil
from app.core.token_verifier import VerifiedIdentity
class RolesTests(TestCase):
    def setUp(self):
        self.settings=Settings(ADMIN_EMAILS=CUENTA_PRUEBAS+',admin@example.com')
    def test_cuenta_pruebas_y_accesos(self):
        self.assertEqual(len(roles_permitidos(CUENTA_PRUEBAS,self.settings)),4)
        self.assertEqual(len(sedes_perfil(CUENTA_PRUEBAS,'gerencia',self.settings)),14)
        self.assertEqual(sedes_perfil('admin@example.com','gerencia',self.settings),[])
    def test_propietario_solo_lectura(self):
        self.assertTrue(puede_usar_ruta('propietario','GET','/api/v1/instalaciones/ventas/resumen'))
        self.assertFalse(puede_usar_ruta('propietario','POST','/api/v1/instalaciones/registro'))
        self.assertFalse(puede_usar_ruta('instalador','GET','/api/v1/instalaciones/historial'))
    def test_http_perfiles_no_otorgan_permisos(self):
        app.dependency_overrides[get_settings]=lambda:self.settings
        app.dependency_overrides[get_current_identity]=lambda:VerifiedIdentity(email=CUENTA_PRUEBAS,email_verified=True,subject='test',role='authenticated')
        try:
            with TestClient(app) as client:
                for perfil in ['propietario','instalador']:
                    headers={'X-Rol':perfil,'X-Sede':'el-carmen'}
                    self.assertEqual(client.post('/api/v1/instalaciones/registro',headers=headers,json={}).status_code,403)
                    self.assertEqual(client.get('/api/v1/clientes/',headers=headers).status_code,403)
                self.assertEqual(client.get('/api/v1/auth/session',headers={'X-Rol':'propietario','X-Sede':'cali'}).json()['authorized'],True)
                self.assertEqual(client.get('/api/v1/auth/session',headers={'X-Rol':'inventado','X-Sede':'cali'}).json()['authorized'],False)
        finally: app.dependency_overrides.clear()
    def test_gerencia_no_crea_instalaciones(self):
        for path in ['/api/v1/instalaciones/registro','/api/v1/instalaciones/','/api/v1/instalaciones/preview']:
            self.assertFalse(puede_usar_ruta('gerencia','POST',path))
        self.assertTrue(puede_usar_ruta('gerencia','GET','/api/v1/instalaciones/historial'))
        self.assertTrue(puede_usar_ruta('administrador','POST','/api/v1/instalaciones/registro'))
