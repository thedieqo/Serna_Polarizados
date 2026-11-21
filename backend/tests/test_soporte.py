from unittest import TestCase
from uuid import uuid4
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import get_current_identity
from app.core.config import get_settings, Settings
from app.core.roles import CUENTA_PRUEBAS
from app.core.token_verifier import VerifiedIdentity
from app.api.v1.soporte import get_soporte_db
from app.db.soporte_tables import metadata,mensajes

class SoporteTests(TestCase):
    def setUp(self):
        self.engine=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
        self.bind=self.engine.execution_options(schema_translate_map={'public':None})
        metadata.create_all(self.bind)
        self.email=CUENTA_PRUEBAS;self.verified=True
        def db():
            with Session(self.bind) as s: yield s
        app.dependency_overrides[get_soporte_db]=db
        app.dependency_overrides[get_current_identity]=lambda:VerifiedIdentity(email=self.email,email_verified=self.verified,subject='qa',role='authenticated')
        app.dependency_overrides[get_settings]=lambda:Settings(ADMIN_EMAILS=CUENTA_PRUEBAS,SUPABASE_URL='https://example.test',SUPABASE_PUBLISHABLE_KEY='qa',REGISTRO_WRITE_ENABLED=True)
        self.c=TestClient(app)
        self.headers={'X-Rol':'gerencia'}
        r=self.c.post('/api/v1/soporte/gerencia/empleados',headers=self.headers,json={'nombre':'Empleado Uno','documento':'12345678','email':'uno@example.test','sede':'cali'})
        self.assertEqual(r.status_code,200,r.text);self.ident=r.json()['id']
        self.ruta=f'/api/v1/soporte/conversaciones/{self.ident}/mensajes'
    def tearDown(self): self.c.close();app.dependency_overrides.clear();self.engine.dispose()
    def enviar(self,texto='Consulta',headers=None,solicitud=None):
        return self.c.post(self.ruta,headers=headers or {},json={'texto':texto,'solicitud_id':solicitud or str(uuid4())})
    def test_cedula_debe_coincidir_con_cuenta_verificada(self):
        self.email='otro@example.test'
        self.assertEqual(self.c.post('/api/v1/soporte/verificar',json={'documento':'12345678'}).status_code,403)
        self.email='uno@example.test';self.verified=False
        self.assertEqual(self.c.post('/api/v1/soporte/verificar',json={'documento':'12345678'}).status_code,403)
        self.verified=True
        self.assertEqual(self.c.post('/api/v1/soporte/verificar',json={'documento':'12345678'}).json()['conversacion_id'],self.ident)
    def test_no_se_puede_leer_ni_escribir_chat_ajeno(self):
        self.email='otro@example.test'
        self.assertEqual(self.c.get(self.ruta).status_code,404)
        self.assertEqual(self.enviar().status_code,404)
        self.assertEqual(self.enviar(headers=self.headers).status_code,404)
        self.assertEqual(self.c.get('/api/v1/soporte/gerencia/empleados',headers=self.headers).status_code,403)
    def test_historial_respuesta_y_reintento_no_duplica(self):
        self.email='uno@example.test';clave=str(uuid4())
        self.assertEqual(self.enviar(solicitud=clave).status_code,200)
        self.assertEqual(self.enviar(solicitud=clave).status_code,200)
        self.assertEqual(self.enviar('Otra cosa',solicitud=clave).status_code,409)
        self.email=CUENTA_PRUEBAS
        self.assertEqual(self.enviar('Respuesta de gerencia',headers=self.headers).status_code,200)
        self.email='uno@example.test'
        m=self.c.get(self.ruta).json()['mensajes']
        self.assertEqual([r['autor_tipo'] for r in m],['empleado','gerencia'])
        self.assertEqual(len(m),2)
        self.assertNotIn('autor_email',m[0])
    def test_desactivar_bloquea_hasta_sesion_existente(self):
        self.email='uno@example.test';self.enviar()
        self.email=CUENTA_PRUEBAS
        r=self.c.put(f'/api/v1/soporte/gerencia/empleados/{self.ident}',headers=self.headers,json={'activo':False})
        self.assertEqual(r.status_code,200)
        self.email='uno@example.test'
        self.assertEqual(self.enviar().status_code,404)
        self.assertEqual(self.c.get(self.ruta).status_code,404)
        self.email=CUENTA_PRUEBAS
        self.assertEqual(len(self.c.get(self.ruta,headers=self.headers).json()['mensajes']),1)
    def test_solo_gerencia_registra_y_cedulas_unicas(self):
        payload={'nombre':'Empleado Dos','documento':'12345678','email':'dos@example.test','sede':'cali'}
        self.assertEqual(self.c.post('/api/v1/soporte/gerencia/empleados',headers=self.headers,json=payload).status_code,409)
        self.email='uno@example.test'
        for rol in ['gerencia','administrador','propietario','instalador']:
            self.assertEqual(self.c.post('/api/v1/soporte/gerencia/empleados',headers={'X-Rol':rol},json=payload).status_code,403)
    def test_historial_paginado_y_bandeja(self):
        self.email='uno@example.test'
        for i in range(52): self.assertEqual(self.enviar(str(i)).status_code,200)
        data=self.c.get(self.ruta).json()
        self.assertEqual(len(data['mensajes']),50);self.assertTrue(data['hay_anteriores'])
        antes=self.c.get(self.ruta,params={'antes':data['mensajes'][0]['id']}).json()
        self.assertEqual([m['texto'] for m in antes['mensajes']],['0','1'])
        incremental=self.c.get(self.ruta,params={'despues':0}).json()
        self.assertTrue(incremental['hay_mas'])
        self.assertEqual([m['texto'] for m in incremental['mensajes']], [str(i) for i in range(50)])
        resto=self.c.get(self.ruta,params={'despues':incremental['mensajes'][-1]['id']}).json()
        self.assertEqual([m['texto'] for m in resto['mensajes']],['50','51'])
        self.assertEqual(self.c.get(self.ruta,params={'antes':3,'despues':0}).status_code,400)
        self.email=CUENTA_PRUEBAS
        lista=self.c.get('/api/v1/soporte/gerencia/conversaciones',headers=self.headers).json()['conversaciones']
        self.assertEqual(lista[0]['texto'],'51')
    def test_sin_sesion_no_revela_empleados(self):
        del app.dependency_overrides[get_current_identity]
        self.assertEqual(self.c.post('/api/v1/soporte/verificar',json={'documento':'12345678'}).status_code,401)
        self.assertEqual(self.c.get(self.ruta).status_code,401)
    def test_validacion_de_mensajes(self):
        self.email='uno@example.test'
        for texto in ['   ','x'*2001]: self.assertEqual(self.enviar(texto).status_code,422)

    def test_contacto_publico_sin_login_no_expone_historial(self):
        del app.dependency_overrides[get_current_identity]
        r=self.c.post('/api/v1/soporte/contacto/verificar',json={'documento':'12345678'})
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(r.json(),{'puede_enviar':True})
        payload={'documento':'12345678','texto':'Necesito ayuda','solicitud_id':str(uuid4())}
        for _ in range(2):self.assertEqual(self.c.post('/api/v1/soporte/contacto/mensajes',json=payload).status_code,200)
        self.assertEqual(self.c.get(self.ruta).status_code,401)
        with Session(self.bind) as db:
            rows=db.execute(select(mensajes)).mappings().all()
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['autor_tipo'],'consulta')
            self.assertEqual(rows[0]['autor_email'],'')

    def test_contacto_publico_revalida_empleado_y_limita_intentos(self):
        self.assertEqual(self.c.post('/api/v1/soporte/contacto/verificar',json={'documento':'99999999'}).status_code,404)
        self.c.put(f'/api/v1/soporte/gerencia/empleados/{self.ident}',headers=self.headers,json={'activo':False})
        r=self.c.post('/api/v1/soporte/contacto/mensajes',json={'documento':'12345678','texto':'Consulta','solicitud_id':str(uuid4())})
        self.assertEqual(r.status_code,404)
        for _ in range(28):self.c.post('/api/v1/soporte/contacto/verificar',json={'documento':'99999999'})
        self.assertEqual(self.c.post('/api/v1/soporte/contacto/verificar',json={'documento':'99999999'}).status_code,429)
