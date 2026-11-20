from datetime import datetime
from unittest import TestCase
from pydantic import ValidationError
from app.schemas.registro_instalacion import RegistroInstalacionCreate, desglose_registro
from app.core.pricing import tarifas_aplicadas
from test_registro_persistence import _payload


class CobrosTests(TestCase):
    def test_formulario_actual_acepta_campos_nuevos_y_pago_de_la_captura(self):
        from unittest.mock import patch
        from app.api.v1.instalaciones import preview_registro
        data = _payload()
        data.update(tipo_descuento='agenda', referido_placa=None, pagos=[
            {'medio':'efectivo','monto_cop':620000},
            {'medio':'transferencia','monto_cop':1000000}])
        base = data['detalles'][0]
        data['detalles'] = [dict(base, vidrio_id=vidrio, tecnologia_id=tecnologia,
                                  pelicula_seguridad=False, grupo=None)
                            for vidrio, tecnologia in [
                                ('parabrisas','ceramic_ir'), ('luneta','ceramic_ir'),
                                ('laterales_delanteros','ultra_hd'), ('laterales_traseros','ultra_hd')]]
        payload = RegistroInstalacionCreate(**data)
        with patch('app.api.v1.instalaciones.get_schema_status', return_value={'save_enabled':True,'reasons':[]}):
            preview = preview_registro(payload)
        self.assertTrue(preview.guardado_habilitado)
        self.assertEqual(preview.desglose.cobro['subtotal_cop'],1800000)
        self.assertEqual(preview.desglose.cobro['descuento_cop'],180000)
        self.assertEqual(preview.desglose.total_cop,1620000)
        self.assertEqual(preview.desglose.cobro['saldo_cop'],0)

    def test_pago_dividido_descuento_comision_y_garantia(self):
        data = _payload()
        data.update(tipo_descuento='agenda', motivo_descuento='Convenio', fecha='2028-02-29T15:00:00Z', pagos=[
            {'medio': 'sistecredito', 'monto_cop': 1000000},
            {'medio': 'efectivo', 'monto_cop': 305000}])
        result = desglose_registro(RegistroInstalacionCreate(**data))
        self.assertEqual(result['total_cop'], 1305000)
        self.assertEqual(result['cobro']['saldo_cop'], 0)
        self.assertEqual(result['cobro']['comision_admin_cop'], 26100)
        self.assertEqual(sum(i['valor_cop'] for i in result['mano_obra']), 75000)
        self.assertEqual(result['garantia']['hasta'], '2043-02-28')

    def test_cuatro_laterales_con_pelicula_y_tarifa_conservada(self):
        data = _payload()
        data['detalles'] = data['detalles'][1:]
        for d in data['detalles']:
            d.update(grupo='cuatro_laterales', pelicula_seguridad=True)
        data['pagos'] = [{'medio': 'addi', 'monto_cop': 1300000}]
        payload = RegistroInstalacionCreate(**data)
        result = desglose_registro(payload)
        self.assertEqual(result['total_cop'], 1300000)
        self.assertEqual(len(result['conceptos']), 1)
        self.assertEqual(result['conceptos'][0]['concepto'], 'Cuatro laterales')
        self.assertEqual(sum(i['valor_cop'] for i in result['mano_obra']), 50000)
        self.assertEqual(tarifas_aplicadas(result, payload.detalles)['por_tecnologia'], {'ceramic_ir':550000})

    def test_rechaza_importes_invalidos(self):
        for changes in [
            {'pagos':[{'medio':'efectivo','monto_cop':1450001}]},
            {'pagos':[{'medio':'efectivo','monto_cop':-1}]},
            {'pagos':[{'medio':'efectivo','monto_cop':1.5}]},
            {'descuento_cop':1450001,'motivo_descuento':'Prueba','pagos':[]},
            {'descuento_cop':100,'pagos':[]},
        ]:
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                RegistroInstalacionCreate(**(_payload() | changes))
