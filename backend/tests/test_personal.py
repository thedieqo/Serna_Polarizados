import base64
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.gerencia_tables import equipo, actividad
from app.db.personal_tables import fichas
from test_gerencia import GerenciaTests
from app.core.config import Settings,get_settings
from app.main import app

class PersonalTests(GerenciaTests):
 def setUp(self):
  super().setUp()
  app.dependency_overrides[get_settings]=lambda:Settings(ADMIN_EMAILS='diegonangumaw@gmail.com,sernapolarizadosibague.1@gmail.com',SUPABASE_URL='https://example.test',SUPABASE_PUBLISHABLE_KEY='qa',REGISTRO_WRITE_ENABLED=True)
  self.url='/api/v1/personal'
 def perfil(self):
  p=self.crear()
  d={'nombres':'Helena Patricia','apellidos':'Quin Barragán','documento':'12345678','telefono':'3001234567','grupo_sanguineo':'O+','eps':'EPS prueba','capacidades':['Administración'],'revision':p['revision'],'motivo':'Completar ficha'}
  r=self.c.put(self.url+'/empleados/'+p['id']+'/ficha',headers=self.h,json=d)
  self.assertEqual(r.status_code,200,r.text);return r.json()
 def activar(self,p):
  path=self.url+'/empleados/'+p['id']
  r=self.c.put(path+'/archivos/foto',headers=self.h,json={'revision':p['revision'],'contenido':base64.b64encode(b'\x89PNG\r\n\x1a\nfixture').decode()})
  self.assertEqual(r.status_code,200,r.text)
  r=self.c.put(path+'/estado',headers=self.h,json={'revision':r.json()['revision'],'activo':True,'motivo':'Datos verificados'})
  self.assertEqual(r.status_code,200,r.text);return r.json()
 def test_foto_obligatoria_documentos_opcionales(self):
  p=self.perfil();self.assertEqual(p['estado'],'pendiente');self.assertEqual(p['nombre_corto'],'Helena Quin')
  r=self.c.put(self.url+'/empleados/'+p['id']+'/estado',headers=self.h,json={'revision':p['revision'],'activo':True,'motivo':'Intentar activar'})
  self.assertEqual(r.status_code,422);self.assertIn('foto',r.text)
  p=self.activar(p);self.assertEqual(p['estado'],'activo');self.assertEqual(p['archivos'],['foto'])
 def test_no_bypass_por_estado_antiguo(self):
  p=self.crear();r=self.c.put(self.base+'/empleados/'+p['id']+'/estado',headers=self.h,json={'revision':1,'activo':True,'motivo':'Prueba incompleta'})
  self.assertEqual(r.status_code,422)
 def test_administrador_no_ve_datos_privados_ni_archivos(self):
  p=self.activar(self.perfil());ruta=self.url+'/empleados/'+p['id']
  self.email='sernapolarizadosibague.1@gmail.com';h={'X-Rol':'administrador','X-Sede':'el-carmen'}
  r=self.c.get(ruta,headers=h);self.assertEqual(r.status_code,200,r.text)
  for key in ['datos','documento','eps','grupo_sanguineo','archivos','faltantes']:self.assertNotIn(key,r.json())
  self.assertEqual(self.c.get(ruta+'/archivos/foto',headers=h).status_code,200)
  self.assertEqual(self.c.get(ruta+'/archivos/contrato',headers=h).status_code,403)
  self.assertEqual(self.c.put(ruta+'/ficha',headers=h,json={'revision':p['revision'],'motivo':'Intrusión'}).status_code,403)
  self.assertEqual(self.c.get(ruta,headers=h|{'X-Sede':'mirolindo'}).status_code,403)
  self.assertEqual(self.c.get(ruta,headers=h|{'X-Rol':'gerencia'}).status_code,403)
 def test_traslado_solo_gerencia_sin_duplicados_y_con_historial(self):
  p=self.activar(self.perfil());data={'empleado_id':p['id'],'destino':'mirolindo','motivo':'Apoyo por demanda'}
  admin={'X-Rol':'administrador','X-Sede':'mirolindo'}
  r=self.c.post(self.url+'/traslados',headers=admin,json=data);self.assertEqual(r.status_code,200,r.text);t=r.json()
  self.assertEqual(self.c.post(self.url+'/traslados',headers=admin,json=data).status_code,409)
  self.assertEqual(self.c.post(self.url+'/traslados',headers=admin,json=data|{'destino':'cali'}).status_code,403)
  route=self.url+'/traslados/'+t['id'];decision={'aprobar':True,'motivo':'Rotación autorizada'}
  self.assertEqual(self.c.put(route,headers=admin,json=decision).status_code,403)
  with Session(self.bind) as db:self.assertEqual(db.scalar(select(equipo.c.sede).where(equipo.c.id==p['id'])),'el-carmen')
  r=self.c.put(route,headers=self.h,json=decision);self.assertEqual(r.status_code,200,r.text)
  self.assertEqual(self.c.put(route,headers=self.h,json=decision).status_code,409)
  self.assertEqual(self.c.get(self.url+'/empleados/'+p['id'],headers={'X-Rol':'administrador','X-Sede':'el-carmen'}).status_code,404)
  with Session(self.bind) as db:
   self.assertEqual(db.scalar(select(equipo.c.sede).where(equipo.c.id==p['id'])),'mirolindo')
   event=db.execute(select(actividad).where(actividad.c.accion=='traslado_aprobado')).mappings().one()
   self.assertEqual(event['antes']['sede'],'el-carmen');self.assertEqual(event['despues']['sede'],'mirolindo')
 def test_rechazo_no_cambia_sede(self):
  p=self.activar(self.perfil());t=self.c.post(self.url+'/traslados',headers=self.h,json={'empleado_id':p['id'],'destino':'cali','motivo':'Prueba traslado'}).json()
  self.assertEqual(self.c.put(self.url+'/traslados/'+t['id'],headers=self.h,json={'aprobar':False,'motivo':'No se necesita'}).status_code,200)
  with Session(self.bind) as db:self.assertEqual(db.scalar(select(equipo.c.sede).where(equipo.c.id==p['id'])),'el-carmen')
 def test_cedula_duplicada_y_revision_obsoleta(self):
  p=self.perfil();self.payload['email']='segundo@example.test';p2=self.crear();d=p['datos']|{'revision':p2['revision'],'motivo':'Completar duplicado'}
  self.assertEqual(self.c.put(self.url+'/empleados/'+p2['id']+'/ficha',headers=self.h,json=d).status_code,409)
  self.assertEqual(self.c.put(self.url+'/empleados/'+p['id']+'/ficha',headers=self.h,json=d|{'revision':1}).status_code,409)
 def test_archivos_privados_tipo_validado(self):
  p=self.perfil();path=self.url+'/empleados/'+p['id']+'/archivos/'
  for kind,content in [('foto',b'%PDF-test'),('contrato',b'<html>evil</html>')]:
   r=self.c.put(path+kind,headers=self.h,json={'revision':p['revision'],'contenido':base64.b64encode(content).decode()});self.assertEqual(r.status_code,422)
  r=self.c.put(path+'contrato',headers=self.h,json={'revision':p['revision'],'contenido':base64.b64encode(b'%PDF-test').decode()});self.assertEqual(r.status_code,200,r.text)
  r=self.c.get(path+'contrato',headers=self.h);self.assertEqual(r.status_code,200);self.assertEqual(r.headers['cache-control'],'no-store')
  from app.core.auth import get_current_identity
  del app.dependency_overrides[get_current_identity]
  self.assertEqual(self.c.get(path+'contrato').status_code,401)
 def test_activo_no_se_mueve_por_edicion_antigua(self):
  p=self.activar(self.perfil())
  r=self.c.put(self.base+'/empleados/'+p['id'],headers=self.h,json=self.payload|{'revision':p['revision'],'motivo':'Saltar traslado','sede':'cali'})
  self.assertEqual(r.status_code,409)
 def test_aprobacion_operativa_exige_ficha_completa_en_sede(self):
  from app.api.v1.mi_trabajo import get_db
  from app.api.v1.soporte import get_soporte_db
  app.dependency_overrides[get_db]=app.dependency_overrides[get_soporte_db]
  h=self.h|{'X-Sede':'el-carmen'}
  ruta='/api/v1/gerencia/instaladores'
  payload={'nombre':'Trabajador QA','email':self.payload['email'],'activo':True}
  self.assertEqual(self.c.post(ruta,headers=h,json=payload).status_code,422)
  self.payload['perfil']='instalador';p=self.perfil()
  self.assertEqual(self.c.post(ruta,headers=h,json=payload).status_code,422)
  p=self.activar(p)
  self.assertEqual(self.c.post(ruta,headers=h|{'X-Sede':'mirolindo'},json=payload).status_code,422)
  from app.db.registro_tables import trabajadores,trabajador_auditoria
  trabajadores.create(self.bind);trabajador_auditoria.create(self.bind)
  from unittest.mock import patch
  with patch('app.services.personal.sincronizar_instalador'):
   r=self.c.post(ruta,headers=h,json=payload);self.assertEqual(r.status_code,200,r.text)
  with Session(self.bind) as db:self.assertTrue(db.scalar(select(trabajadores.c.activo)))
