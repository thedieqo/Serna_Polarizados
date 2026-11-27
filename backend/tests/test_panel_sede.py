from datetime import datetime,timezone
from sqlalchemy import insert,select
from sqlalchemy.orm import Session
from app.main import app
from app.api.v1.soporte import get_soporte_db
from app.api.v1.panel_sede import get_db,resumen
from app.db.registro_tables import metadata,clientes,vehiculos,instalaciones,instalacion_novedades
from app.db.gerencia_tables import actividad
from test_gerencia import GerenciaTests

class PanelSedeTests(GerenciaTests):
 def setUp(self):
  super().setUp();metadata.create_all(self.bind)
  app.dependency_overrides[get_db]=app.dependency_overrides[get_soporte_db]
  self.h={'X-Rol':'gerencia','X-Sede':'el-carmen'}
 def test_pendientes_por_sede_resolucion_revision_y_auditoria(self):
  data={'titulo':'Internet de noviembre','categoria':'internet','vencimiento':'2026-11-30'}
  r=self.c.post('/api/v1/sede/pendientes',headers=self.h,json=data);self.assertEqual(r.status_code,200,r.text);p=r.json()
  self.assertEqual(len(self.c.get('/api/v1/sede/pendientes',headers=self.h).json()['registros']),1)
  otra=self.h|{'X-Sede':'mirolindo'}
  self.assertEqual(self.c.get('/api/v1/sede/pendientes',headers=otra).json()['registros'],[])
  url='/api/v1/sede/pendientes/'+p['id'];body={'revision':1,'completado':True}
  self.assertEqual(self.c.put(url,headers=otra,json=body).status_code,404)
  self.assertEqual(self.c.put(url,headers=self.h,json=body).status_code,200)
  self.assertEqual(self.c.put(url,headers=self.h,json=body).status_code,409)
  self.assertEqual(self.c.get('/api/v1/sede/resumen',headers=self.h).json()['pendientes'],0)
  self.assertEqual(self.c.put(url,headers=self.h,json={'revision':2,'completado':False}).status_code,200)
  self.assertEqual(self.c.get('/api/v1/sede/resumen',headers=self.h).json()['pendientes'],1)
  with Session(self.bind) as db:self.assertEqual(len(db.execute(select(actividad).where(actividad.c.empleado_id==p['id'])).all()),3)
 def test_resumen_excluye_futuros_anulados_y_limite_colombia(self):
  with Session(self.bind) as db:
   db.execute(insert(clientes).values(id=1,nombre='QA',documento='QA',contacto='QA'))
   db.execute(insert(vehiculos).values(id=1,placa='TEST01',cliente_id=1))
   rows=[('2026-11-01T04:59:59',100,'finalizado'),('2026-11-01T05:00:00',200,'finalizado'),('2026-11-20T10:00:00',300,'anulado'),('2026-11-20T18:00:00',400,'programado'),('2026-11-20T12:00:00',None,'programado')]
   for i,(fecha,valor,estado) in enumerate(rows,1):db.execute(insert(instalaciones).values(id=i,vehiculo_id=1,fecha=datetime.fromisoformat(fecha),tipo_servicio='polarizado',zonas=[],asignaciones_instaladores=[],estado=estado,precio_total_cop=valor))
   db.execute(insert(instalacion_novedades).values(instalacion_id=2,fecha_atencion=datetime(2026,11,2),motivo='QA',descripcion='QA',registrado_por='qa'))
   db.commit();r=resumen(db,datetime(2026,11,20,17,tzinfo=timezone.utc))
   self.assertEqual(r['ventas_cop'],200);self.assertEqual(r['sin_precio'],1);self.assertEqual(r['instalaciones_mes'],2);self.assertEqual(r['garantias_mes'],1)
 def test_direccion_y_enlace_seguro(self):
  url=self.base+'/sedes/el-carmen/direccion'
  self.assertEqual(self.c.get(url,headers=self.h).json()['revision'],0)
  data={'direccion':'Calle 22 # 5-35, El Carmen, Ibagué, Tolima','ubicacion':'https://maps.app.goo.gl/6yghnomFCeuq9RiZ7','revision':0}
  r=self.c.put(url,headers=self.h,json=data);self.assertEqual(r.status_code,200,r.text)
  self.assertEqual(self.c.put(url,headers=self.h,json=data).status_code,409)
  self.assertEqual(self.c.put(url,headers=self.h,json=data|{'revision':1,'ubicacion':'javascript:alert(1)'}).status_code,422)
  self.assertEqual(self.c.get(url,headers=self.h).json()['direccion'],data['direccion'])
 def test_solo_gerencia_y_sede_autorizada(self):
  for role in ['administrador','instalador','propietario']:
   self.assertEqual(self.c.get('/api/v1/sede/resumen',headers=self.h|{'X-Rol':role}).status_code,403)
  self.assertEqual(self.c.get('/api/v1/sede/resumen',headers=self.h|{'X-Sede':'inventada'}).status_code,400)
  self.assertEqual(self.c.get(self.base+'/sedes/el-carmen/direccion',headers=self.h|{'X-Rol':'administrador'}).status_code,403)
