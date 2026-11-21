from unittest import TestCase
from unittest.mock import patch
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import create_engine, insert, select, update, func, event
from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.db.registro_tables import metadata, trabajadores, instalaciones, inventario, inventario_movimientos, vidrios_realizados, confirmaciones_trabajo
from app.services.trabajo import confirmar, resumen, buscar, TrabajoError
from app.api.v1.mi_trabajo import Confirmacion
from app.schemas.registro_instalacion import RegistroInstalacionCreate
from app.services.registro_instalacion import guardar_registro
from app.services.ventas import resumen_ventas
from test_registro_persistence import _payload, _seed_catalogos

class TrabajoTests(TestCase):
    def setUp(self):
        self.engine=create_engine('sqlite://')
        @event.listens_for(self.engine,'connect')
        def f(conn,_): conn.execute('PRAGMA foreign_keys=ON')
        metadata.create_all(self.engine)
        self.db=Session(self.engine)
        _seed_catalogos(self.db)
        self.db.execute(insert(trabajadores).values(id='uno',nombre='Trabajador Uno',email='uno@example.com',activo=True,aprobado_por='gerente@example.com'))
        self.db.execute(insert(trabajadores).values(id='dos',nombre='Trabajador Dos',email='dos@example.com',activo=True,aprobado_por='gerente@example.com'))
        self.db.commit()
        self.venta=guardar_registro(self.db,RegistroInstalacionCreate(**_payload())).instalacion_id
    def tearDown(self): self.db.close();self.engine.dispose()
    def solicitud(self,slot='0:unico',**kw):
        return Confirmacion(id=uuid4(),instalacion_id=self.venta,vidrios=[{'slot':slot,'metros':'1.55',**kw}])
    def ejecutar(self,p,email='uno@example.com'):
        try: r=confirmar(self.db,email,p);self.db.commit();return r
        except Exception: self.db.rollback();raise
    def stock(self,sku='ultra_hd:35:polarizado'):
        return self.db.execute(select(inventario.c.disponible_cm).where(inventario.c.sku==sku)).scalar_one()
    def test_real_idempotente_y_privacidad(self):
        p=self.solicitud()
        self.assertEqual(self.ejecutar(p)['ganado_cop'],25000)
        self.assertEqual(self.stock(),19845)
        self.assertTrue(self.ejecutar(p)['repetido'])
        self.assertEqual(self.stock(),19845)
        self.assertEqual(resumen(self.db,'uno@example.com')['ganado_mes_cop'],25000)
        self.assertEqual(resumen(self.db,'dos@example.com')['ganado_mes_cop'],0)
        self.assertNotIn('email',str(buscar(self.db,'ABC 123')))
    def test_otro_instalador_no_duplica_vidrio(self):
        self.ejecutar(self.solicitud())
        with self.assertRaises(TrabajoError): self.ejecutar(self.solicitud(),'dos@example.com')
        self.assertEqual(self.stock(),19845)
    def test_ambos_instaladores_mismo_sku_distintos_vidrios(self):
        self.ejecutar(self.solicitud('1:lateral_derecho'))
        self.ejecutar(self.solicitud('1:lateral_izquierdo'),'dos@example.com')
        self.assertEqual(self.stock('ceramic_ir:20:polarizado'),19690)
    def test_tarifas_y_custodia(self):
        self.assertEqual(self.ejecutar(self.solicitud(tipo_parabrisas='camion'))['ganado_cop'],35000)
        self.assertEqual(self.ejecutar(self.solicitud('1:lateral_derecho'))['ganado_cop'],12500)
        self.assertEqual(self.ejecutar(self.solicitud('1:custodia_derecho'))['ganado_cop'],6250)
    def test_material_insuficiente_revierte_incluso_consumo_previo(self):
        self.db.execute(update(inventario).where(inventario.c.sku=='ultra_hd:35:polarizado').values(disponible_cm=1));self.db.commit()
        p=Confirmacion(id=uuid4(),instalacion_id=self.venta,vidrios=[{'slot':'1:lateral_derecho','metros':'1.20'},{'slot':'0:unico','metros':'1.50'}])
        with self.assertRaises(TrabajoError): self.ejecutar(p)
        self.assertEqual(self.stock('ceramic_ir:20:polarizado'),20000)
        self.assertEqual(self.db.execute(select(func.count()).select_from(confirmaciones_trabajo)).scalar(),0)
        self.assertEqual(resumen(self.db,'uno@example.com')['ganado_mes_cop'],0)
    def test_inactivo_y_vidrio_ajeno_y_categoria(self):
        with self.assertRaises(TrabajoError): self.ejecutar(self.solicitud('otro'))
        with self.assertRaises(TrabajoError): self.ejecutar(self.solicitud('1:lateral_derecho',tipo_parabrisas='camion'))
        self.db.execute(update(trabajadores).where(trabajadores.c.id=='uno').values(activo=False));self.db.commit()
        with self.assertRaises(TrabajoError): self.ejecutar(self.solicitud())
    def test_medidas_invalidas_y_duplicado_en_peticion(self):
        for metros in ['0','-1','1.001','201','NaN']:
            with self.assertRaises(ValidationError): self.solicitud(metros=metros)
        p=self.solicitud();p.vidrios.append(p.vidrios[0])
        with self.assertRaises(TrabajoError): self.ejecutar(p)
    def test_historico_no_se_descuenta(self):
        self.db.execute(update(instalaciones).values(desglose_precios={}));self.db.commit()
        with self.assertRaises(TrabajoError): self.ejecutar(self.solicitud())
        self.assertEqual(buscar(self.db,'ABC123'),[])
    def test_ganancias_fecha_confirmacion_no_fecha_venta(self):
        self.db.execute(update(instalaciones).values(fecha=datetime(2020,1,1)));self.db.commit()
        self.ejecutar(self.solicitud())
        now=datetime.now(timezone.utc)
        r=resumen_ventas(self.db,now.year,now.month,'mes')
        self.assertEqual(r['totales']['instaladores_cop'],25000)
        self.assertEqual(r['totales']['ventas_cop'],0)
    def test_http_aprobacion_solo_gerencia_y_sede_autorizada(self):
        from fastapi.testclient import TestClient
        from app.main import app
        from app.core.auth import get_current_identity
        from app.core.config import Settings, get_settings
        from app.core.roles import CUENTA_PRUEBAS
        from app.core.token_verifier import VerifiedIdentity
        app.dependency_overrides[get_current_identity]=lambda:VerifiedIdentity(email=CUENTA_PRUEBAS,email_verified=True,subject='test',role='authenticated')
        app.dependency_overrides[get_settings]=lambda:Settings(ADMIN_EMAILS=CUENTA_PRUEBAS,SUPABASE_URL='https://example.test',SUPABASE_PUBLISHABLE_KEY='test',REGISTRO_WRITE_ENABLED=True)
        try:
            with TestClient(app) as client:
                for rol in ['administrador','propietario','instalador']:
                    self.assertEqual(client.post('/api/v1/gerencia/instaladores',headers={'X-Rol':rol,'X-Sede':'el-carmen'},json={}).status_code,403)
                with patch('app.core.auth.acceso_sede',return_value=False):
                    self.assertEqual(client.get('/api/v1/mi-trabajo/buscar?placa=ABC123',headers={'X-Rol':'instalador','X-Sede':'cali'}).status_code,403)
        finally: app.dependency_overrides.clear()
