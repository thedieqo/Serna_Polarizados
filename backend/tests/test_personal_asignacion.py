from unittest import TestCase
from unittest.mock import patch
from sqlalchemy import create_engine,MetaData,insert,select,text
from sqlalchemy.orm import Session
from app.db.registro_tables import trabajadores,trabajador_auditoria
from app.services.personal import sincronizar_instalador

class AsignacionTests(TestCase):
 def test_traslado_preserva_ids_revoca_anterior_y_no_concede_cuenta_nueva(self):
  engine=create_engine('sqlite://')
  with engine.connect() as c:
   c.execute(text("ATTACH DATABASE ':memory:' AS origen"));c.execute(text("ATTACH DATABASE ':memory:' AS destino"))
   tablas={}
   for schema in ('origen','destino'):
    meta=MetaData();t=trabajadores.to_metadata(meta,schema=schema);audit=trabajador_auditoria.to_metadata(meta,schema=schema);meta.create_all(c);tablas[schema]=t
   c.commit()
   with Session(c) as db,patch('app.services.personal.SEDES',{'a':{'schema':'origen'},'b':{'schema':'destino'}}):
    p={'nombre':'Trabajador QA','email':'qa@example.test','perfil':'instalador'}
    sincronizar_instalador(db,p,'b',True,'gerencia@example.test')
    self.assertEqual(list(db.execute(select(tablas['destino']))),[])
    db.execute(insert(tablas['origen']).values(id='original',nombre=p['nombre'],email=p['email'],activo=True,aprobado_por='gerencia'))
    sincronizar_instalador(db,p,'b',True,'gerencia@example.test')
    viejo=db.execute(select(tablas['origen'])).mappings().one();nuevo=db.execute(select(tablas['destino'])).mappings().one()
    self.assertEqual(viejo['id'],'original');self.assertFalse(viejo['activo']);self.assertTrue(nuevo['activo'])
    sincronizar_instalador(db,p,'a',True,'gerencia@example.test')
    self.assertEqual(db.execute(select(tablas['origen'])).mappings().one()['id'],'original')
    self.assertFalse(db.execute(select(tablas['destino'])).mappings().one()['activo'])
    sincronizar_instalador(db,p,'a',False,'gerencia@example.test')
    self.assertFalse(db.execute(select(tablas['origen'])).mappings().one()['activo'])
  engine.dispose()
