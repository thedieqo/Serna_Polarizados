from datetime import datetime, timezone
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.db.base import Base
from app.models.cliente import Cliente
from app.models.vehiculo import Vehiculo
from app.models.instalacion import Instalacion
from app.services.ventas import resumen_ventas


class VentasTests(TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        Base.metadata.create_all(self.engine)
        from app.db.registro_tables import metadata
        metadata.create_all(self.engine)
        self.db = Session(self.engine)
        cliente = Cliente(nombre='Prueba', documento='1', contacto='3000000000')
        self.db.add(cliente); self.db.flush()
        vehiculo = Vehiculo(placa='TEST01', cliente_id=cliente.id)
        self.db.add(vehiculo); self.db.flush()
        self.vehiculo = vehiculo.id

    def tearDown(self):
        self.db.close(); self.engine.dispose()

    def venta(self, fecha, estado='programado', historica=False):
        datos = None if historica else {
            'cobro': {'descuento_cop': 50000, 'pagado_cop': 200000, 'saldo_cop':0,
                      'comision_admin_cop':4000, 'pagos':[
                          {'medio':'efectivo','monto_cop':50000},
                          {'medio':'tarjeta_credito','monto_cop':150000}]},
            'mano_obra':[{'instalador_id':'daniel_mira','instalador':'Daniel Mira',
                         'vidrio':'Parabrisas','panel':None,'valor_cop':25000}]}
        self.db.add(Instalacion(vehiculo_id=self.vehiculo, fecha=datetime.fromisoformat(fecha),
            estado=estado, tipo_servicio='polarizado', zonas=[], asignaciones_instaladores=[],
            precio_total_cop=None if historica else 200000, desglose_precios=datos))
        self.db.commit()

    def test_limites_colombia_y_conciliacion_de_cortes(self):
        # UTC 05:00 is midnight in Colombia.
        for fecha in ['2026-11-01T04:59:59', '2026-11-01T05:00:00',
                      '2026-11-16T04:59:59', '2026-11-16T05:00:00',
                      '2026-12-01T04:59:59', '2026-12-01T05:00:00']:
            self.venta(fecha)
        self.venta('2026-11-20T12:00:00', estado='anulado')
        mes = resumen_ventas(self.db, 2026, 11, 'mes')
        primera = resumen_ventas(self.db, 2026, 11, 'primera')
        segunda = resumen_ventas(self.db, 2026, 11, 'segunda')
        self.assertEqual([mes['cantidad'], primera['cantidad'], segunda['cantidad']], [4,2,2])
        self.assertEqual(mes['totales']['ventas_cop'], 800000)
        self.assertEqual(mes['totales']['administrador_cop'], 16000)
        self.assertEqual(mes['instaladores'][0]['total_cop'],100000)
        self.assertEqual(mes['medios'], {'efectivo':200000,'tarjeta_credito':600000})
        for key in mes['totales']:
            self.assertEqual(mes['totales'][key], primera['totales'][key]+segunda['totales'][key])

    def test_ganado_mensual_excluye_futuras_anuladas_y_otros_meses(self):
        for fecha in ['2026-10-31T15:00:00', '2026-11-01T15:00:00',
                      '2026-11-16T15:00:00', '2026-11-20T16:00:00',
                      '2026-11-20T18:00:00', '2026-11-30T15:00:00']:
            self.venta(fecha)
        self.venta('2026-11-18T15:00:00', estado='anulado')
        ahora = datetime(2026,11,20,17,0,tzinfo=timezone.utc)
        acumulado = resumen_ventas(self.db,2026,11,'mes',acumulado=True,ahora=ahora)
        self.assertEqual(acumulado['cantidad'],3)
        self.assertEqual(acumulado['totales']['ventas_cop'],600000)
        self.assertEqual(acumulado['totales']['administrador_cop'],12000)
        self.assertEqual(acumulado['instaladores'][0]['total_cop'],75000)
        self.assertEqual(acumulado['instaladores'][0]['instalaciones'],3)
        self.assertEqual(acumulado['actualizado_en'],ahora)
        completo = resumen_ventas(self.db,2026,11,'mes')
        self.assertEqual(completo['cantidad'],5)

    def test_fin_de_mes_31_y_febrero_bisiesto(self):
        self.venta('2026-08-01T04:59:59')
        self.assertEqual(resumen_ventas(self.db,2026,7,'segunda')['cantidad'],1)
        self.venta('2028-03-01T04:59:59')
        febrero = resumen_ventas(self.db,2028,2,'segunda')
        self.assertEqual(str(febrero['hasta']),'2028-02-29')
        self.assertEqual(febrero['cantidad'],1)

    def test_historico_sin_importes_no_inventa_comisiones(self):
        self.venta('2026-11-20T12:00:00',historica=True)
        reporte = resumen_ventas(self.db,2026,11,'mes')
        self.assertEqual(reporte['sin_precio'],1)
        self.assertEqual(reporte['sin_liquidacion'],1)
        self.assertEqual(reporte['totales']['administrador_cop'],0)
        self.assertEqual(reporte['instaladores'],[])

    def test_pagos_por_fila_concuerdan_con_totales_y_no_estiman_historicos(self):
        self.venta('2026-11-20T12:00:00')
        self.venta('2026-11-21T12:00:00', historica=True)
        fila = self.db.query(Instalacion).order_by(Instalacion.id).first()
        datos = dict(fila.desglose_precios)
        datos['cobro'] = {**datos['cobro'], 'pagos': [
            {'medio': 'efectivo', 'monto_cop': 50000},
            {'medio': 'transferencia', 'monto_cop': 150000}]}
        fila.desglose_precios = datos
        self.db.commit()
        reporte = resumen_ventas(self.db, 2026, 11, 'mes')
        mixta, historica = reporte['registros']
        self.assertEqual(mixta['id'], fila.id)
        self.assertEqual(mixta['pagos'], datos['cobro']['pagos'])
        self.assertEqual(sum(p['monto_cop'] for p in mixta['pagos']), mixta['pagado_cop'])
        self.assertEqual(mixta['saldo_cop'], 0)
        self.assertEqual(reporte['medios'], {'efectivo': 50000, 'transferencia': 150000})
        self.assertEqual(historica['pagos'], [])
        self.assertIsNone(historica['pagado_cop'])
        self.assertIsNone(historica['saldo_cop'])
