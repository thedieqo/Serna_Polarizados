from datetime import datetime
from unittest import TestCase
from pydantic import ValidationError
from app.schemas.registro_instalacion import RegistroInstalacionCreate, desglose_registro
from app.core.pricing import tarifas_aplicadas
from test_registro_persistence import _payload


class CobrosTests(TestCase):
    def test_pago_dividido_descuento_comision_y_garantia(self):
        data = _payload()
        data.update(descuento_cop=50000, motivo_descuento='Convenio', fecha='2028-02-29T15:00:00Z', pagos=[
            {'medio': 'sistecredito', 'monto_cop': 1000000},
            {'medio': 'efectivo', 'monto_cop': 400000}])
        result = desglose_registro(RegistroInstalacionCreate(**data))
        self.assertEqual(result['total_cop'], 1400000)
        self.assertEqual(result['cobro']['saldo_cop'], 0)
        self.assertEqual(result['cobro']['comision_admin_cop'], 28000)
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
