from unittest import TestCase
from unittest.mock import patch
from sqlalchemy import create_engine,select,func
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import get_current_identity
from app.core.config import Settings,get_settings
from app.core.roles import CUENTA_PRUEBAS
from app.core.token_verifier import VerifiedIdentity
from app.api.v1.soporte import get_soporte_db
from app.db.gerencia_tables import metadata,equipo,actividad

class GerenciaTests(TestCase):
 def setUp(self):
  sync=patch("app.api.v1.personal.sincronizar_instalador");sync.start();self.addCleanup(sync.stop)
  self.engine=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
  self.bind=self.engine.execution_options(schema_translate_map={'public':None});metadata.create_all(self.bind)
  self.email=CUENTA_PRUEBAS;self.verificada=True
  def db():
   with Session(self.bind) as s:yield s
  app.dependency_overrides[get_soporte_db]=db
  app.dependency_overrides[get_current_identity]=lambda:VerifiedIdentity(email=self.email,email_verified=self.verificada,subject='qa',role='authenticated')
  app.dependency_overrides[get_settings]=lambda:Settings(ADMIN_EMAILS=CUENTA_PRUEBAS,SUPABASE_URL='https://example.test',SUPABASE_PUBLISHABLE_KEY='qa',REGISTRO_WRITE_ENABLED=True)
  self.c=TestClient(app);self.h={'X-Rol':'gerencia'};self.base='/api/v1/gerencia/gestion'
  self.payload={'nombre':'Empleado QA','email':'qa@serna.example.invalid','perfil':'administrador','sede':'el-carmen'}
 def tearDown(self):self.c.close();app.dependency_overrides.clear();self.engine.dispose()
 def crear(self):
  r=self.c.post(self.base+'/empleados',headers=self.h,json=self.payload);self.assertEqual(r.status_code,200,r.text);return r.json()
 def test_crear_editar_desactivar_audita_sin_borrar(self):
  p=self.crear();ruta=self.base+'/empleados/'+p['id']
  r=self.c.put(ruta,headers=self.h,json=self.payload|{'nombre':'Empleado actualizado','revision':1,'motivo':'Corrección del nombre'})
  self.assertEqual(r.status_code,200,r.text)
  self.assertEqual(self.c.put(ruta+'/estado',headers=self.h,json={'activo':False,'revision':2,'motivo':'Fin de prueba'}).status_code,200)
  with Session(self.bind) as db:
   e=db.execute(select(equipo)).mappings().one();self.assertFalse(e['activo']);self.assertTrue(e['es_prueba'])
   eventos=db.execute(select(actividad).order_by(actividad.c.id)).mappings().all()
   self.assertEqual([x['accion'] for x in eventos],['creado','modificado','personal_inactivo'])
   self.assertEqual(eventos[1]['antes']['nombre'],'Empleado QA');self.assertEqual(eventos[1]['despues']['nombre'],'Empleado actualizado')
   self.assertTrue(all(x['actor']==CUENTA_PRUEBAS for x in eventos))
  self.assertEqual(self.c.delete(ruta,headers=self.h).status_code,405)
 def test_rechaza_cambios_obsoletos_y_duplicados(self):
  p=self.crear();ruta=self.base+'/empleados/'+p['id']
  self.assertEqual(self.c.post(self.base+'/empleados',headers=self.h,json=self.payload).status_code,409)
  self.assertEqual(self.c.put(ruta+'/estado',headers=self.h,json={'activo':False,'revision':1,'motivo':'Prueba'}).status_code,200)
  self.assertEqual(self.c.put(ruta,headers=self.h,json=self.payload|{'revision':1,'motivo':'Obsoleto'}).status_code,409)
  with Session(self.bind) as db:self.assertEqual(db.scalar(select(func.count()).select_from(actividad)),2)
 def test_solo_gerencia_y_cuenta_verificada(self):
  for rol in ['administrador','propietario','instalador','ingeniero','auxiliar_gerencia']:
   self.assertEqual(self.c.get(self.base+'/resumen',headers={'X-Rol':rol}).status_code,403)
  self.email='intruso@example.test'
  self.assertEqual(self.c.get(self.base+'/resumen',headers=self.h).status_code,403)
  self.email=CUENTA_PRUEBAS;self.verificada=False
  self.assertEqual(self.c.post(self.base+'/empleados',headers=self.h,json=self.payload).status_code,403)
  del app.dependency_overrides[get_current_identity]
  self.assertEqual(self.c.get(self.base+'/actividad',headers=self.h).status_code,401)
 def test_validacion_no_permite_asignarse_accesos(self):
  for datos in [self.payload|{'perfil':'inventado'},self.payload|{'sede':'otra'},self.payload|{'es_prueba':False},self.payload|{'perfil':'gerencia'}]:
   self.assertEqual(self.c.post(self.base+'/empleados',headers=self.h,json=datos).status_code,422)
 def test_catalogo_y_filtros(self):
  self.crear();r=self.c.get(self.base+'/resumen',headers=self.h).json()
  self.assertEqual(len(r['sedes']),14);self.assertEqual(r['total_empleados'],1)
  self.assertEqual([x['id'] for x in r['sedes'] if x['lavadero']],['mirolindo'])
  self.assertEqual(self.c.get(self.base+'/empleados',headers=self.h,params={'sede':'cali'}).json()['empleados'],[])
  self.assertEqual(len(self.c.get(self.base+'/empleados',headers=self.h,params={'q':'QA'}).json()['empleados']),1)
 def test_crear_sede_solo_gerencia_sin_habilitar_operaciones(self):
  from app.db.gerencia_tables import sedes_nuevas
  datos={'nombre':'Centro de prueba','ciudad':'Ciudad de prueba'}
  self.assertEqual(self.c.post(self.base+'/sedes',headers={'X-Rol':'administrador'},json=datos).status_code,403)
  r=self.c.post(self.base+'/sedes',headers=self.h,json=datos)
  self.assertEqual(r.status_code,200,r.text);self.assertFalse(r.json()['operativa'])
  self.assertEqual(self.c.post(self.base+'/sedes',headers=self.h,json=datos|{'nombre':'CENTRO DE PRUEBA'}).status_code,409)
  self.assertEqual(self.c.post(self.base+'/sedes',headers=self.h,json={'nombre':'El Carmen','ciudad':'Ibagué'}).status_code,409)
  result=self.c.get(self.base+'/resumen',headers=self.h).json()
  self.assertEqual(len(result['sedes']),15)
  with Session(self.bind) as db:
   self.assertEqual(db.scalar(select(func.count()).select_from(sedes_nuevas)),1)
   self.assertEqual(db.scalar(select(actividad.c.actor).where(actividad.c.accion=='sede_creada')),CUENTA_PRUEBAS)
