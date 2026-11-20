from unittest import TestCase
from types import SimpleNamespace
from app.core.liquidacion import liquidar_instaladores

class LiquidacionTests(TestCase):
    def detalle(self, vidrio, panel=None, instalador='daniel_mira'):
        return SimpleNamespace(vidrio_id=vidrio, panel=panel, instalador_id=instalador)

    def test_cuatro_laterales_y_panoramicos_son_cuatro_secciones(self):
        filas = liquidar_instaladores([self.detalle(v) for v in [
            'parabrisas', 'laterales_delanteros', 'laterales_traseros', 'luneta']])
        self.assertEqual(sum(f['valor_cop'] for f in filas), 100000)

    def test_sunroof_doble_paga_cada_panel_a_su_instalador(self):
        filas = liquidar_instaladores([
            self.detalle('sunroof_doble', 'delantero'),
            self.detalle('sunroof_doble', 'trasero', 'joseth_mora')])
        self.assertEqual([f['valor_cop'] for f in filas], [25000, 25000])
        self.assertEqual([f['instalador_id'] for f in filas], ['daniel_mira', 'joseth_mora'])

    def test_simple_paga_una_seccion(self):
        self.assertEqual(liquidar_instaladores([self.detalle('sunroof_simple')])[0]['valor_cop'], 25000)
