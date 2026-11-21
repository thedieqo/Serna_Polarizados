from unittest import TestCase
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.core.auth import accesos_identidad, get_current_identity
from app.core.config import Settings, get_settings
from app.core.roles import CUENTA_PRUEBAS
from app.core.token_verifier import VerifiedIdentity
from app.main import app

class AccesosTests(TestCase):
    def setUp(self): self.settings=Settings(ADMIN_EMAILS=CUENTA_PRUEBAS+',admin@example.com')
    def identidad(self,email,verified=True):
        return VerifiedIdentity(email=email,email_verified=verified,subject='test',role='authenticated')
    def test_correo_no_verificado_no_consulta_permisos(self):
        with patch('app.core.auth.sedes_instalador_aprobado') as consulta:
            self.assertEqual(accesos_identidad(self.identidad('x@example.com',False),self.settings)['perfiles'],[])
            consulta.assert_not_called()
    def test_administrador_solo_su_sede(self):
        with patch('app.core.auth.sedes_instalador_aprobado',return_value=[]):
            p=accesos_identidad(self.identidad('calisp@gmail.com'),self.settings)['perfiles']
        self.assertEqual([x['rol'] for x in p],['administrador'])
        self.assertEqual([x['id'] for x in p[0]['sedes']],['cali'])
    def test_instalador_usa_asignacion_aprobada(self):
        with patch('app.core.auth.sedes_instalador_aprobado',return_value=['tunja']):
            p=accesos_identidad(self.identidad('trabajador@example.com'),self.settings)['perfiles']
        self.assertEqual([x['rol'] for x in p],['instalador'])
        self.assertEqual(p[0]['sedes'][0]['id'],'tunja')
    def test_correo_sin_asignaciones_no_entra(self):
        with patch('app.core.auth.sedes_instalador_aprobado',return_value=[]):
            r=accesos_identidad(self.identidad('x@example.com'),self.settings)
        self.assertEqual(r['perfiles'],[])
        self.assertEqual(r['authorization_code'],'USUARIO_NO_AUTORIZADO')
    def test_cuenta_pruebas_conserva_roles_sin_elevar_otras_cuentas(self):
        r=accesos_identidad(self.identidad(CUENTA_PRUEBAS),self.settings)
        self.assertEqual(len(r['perfiles']),4)
        self.assertEqual(len(r['perfiles'][0]['sedes']),11)
    def test_http_headers_no_deciden_los_roles_descubiertos(self):
        app.dependency_overrides[get_current_identity]=lambda:self.identidad('calisp@gmail.com')
        app.dependency_overrides[get_settings]=lambda:self.settings
        try:
            with patch('app.core.auth.sedes_instalador_aprobado',return_value=[]),TestClient(app) as c:
                r=c.get('/api/v1/auth/accesos',headers={'X-Rol':'gerencia','X-Sede':'el-carmen'})
                self.assertEqual(r.status_code,200)
                self.assertEqual(r.json()['perfiles'][0]['rol'],'administrador')
                self.assertEqual(len(r.json()['perfiles']),1)
        finally: app.dependency_overrides.clear()
    def test_endpoint_requiere_sesion(self):
        with TestClient(app) as c: self.assertEqual(c.get('/api/v1/auth/accesos').status_code,401)
