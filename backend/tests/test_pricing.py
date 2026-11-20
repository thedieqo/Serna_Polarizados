from unittest import TestCase

from pydantic import ValidationError

from app.core.catalogs import catalogos_response
from app.core.pricing import (
    INCREMENTO_SEGURIDAD_LATERALES_COP,
    PRECIO_PENDIENTE,
    TARIFAS_TECNOLOGIA_COP,
    calcular_desglose,
)
from app.schemas.registro_instalacion import RegistroInstalacionCreate, build_preview


class FakeDetalle:
    def __init__(self, vidrio_id: str, tecnologia_id: str, panel: str | None = None):
        self.vidrio_id = vidrio_id
        self.tecnologia_id = tecnologia_id
        self.panel = panel


def registro_data(**overrides):
    data = {
        "cliente": {
            "documento": "CC-100",
            "nombre": "Propietario",
            "telefono": "3001234567",
            "email": "prop@example.com",
        },
        "vehiculo": {"placa": "ABC123", "marca": "Toyota"},
        "tipo_factura": "normal",
        "detalles": [
            {
                "vidrio_id": "parabrisas",
                "tecnologia_id": "ultra_hd",
                "opacidad_id": "35",
                "instalador_id": "daniel_mira",
            }
        ],
    }
    data.update(overrides)
    return data


class PricingTests(TestCase):
    def test_tarifas_confirmadas_en_cop(self):
        self.assertEqual(
            TARIFAS_TECNOLOGIA_COP,
            {
                "high_definition_premium": 250000,
                "ultra_hd": 350000,
                "color_stable": 400000,
                "ceramic_ir": 550000,
            },
        )
        tarifas = catalogos_response()["tarifas"]
        self.assertEqual(tarifas["moneda"], "COP")
        self.assertEqual(tarifas["incremento_seguridad_laterales_cop"], 100000)
        self.assertEqual(
            tarifas["incremento_seguridad_laterales_unidad"], "Por pareja; $200.000 por los cuatro laterales"
        )

    def test_seciones_confirmadas_y_pares_no_se_cobran_por_vidrio(self):
        desglose = calcular_desglose(
            [
                FakeDetalle("parabrisas", "ultra_hd"),
                FakeDetalle("luneta", "ceramic_ir"),
                FakeDetalle("laterales_delanteros", "color_stable"),
            ]
        )
        self.assertEqual(desglose["estado"], "definido")
        self.assertEqual(desglose["total_cop"], 1300000)
        self.assertEqual(desglose["moneda"], "COP")
        self.assertEqual(
            [concepto["secciones"] for concepto in desglose["conceptos"]],
            [1, 1, 1],
        )
        self.assertIn("par/sección", desglose["conceptos"][2]["detalle"])

    def test_sunroof_sencillo_y_doble_tarifa_por_panel(self):
        for tecnologia, precio in TARIFAS_TECNOLOGIA_COP.items():
            with self.subTest(tecnologia=tecnologia):
                simple = calcular_desglose([FakeDetalle('sunroof_simple', tecnologia)])
                doble = calcular_desglose([
                    FakeDetalle('sunroof_doble', tecnologia, 'delantero'),
                    FakeDetalle('sunroof_doble', tecnologia, 'trasero')])
                self.assertEqual(simple['total_cop'], precio)
                self.assertEqual(doble['total_cop'], 2 * precio)
                self.assertEqual(doble['estado'], 'definido')

    def test_preview_usa_desglose_del_backend(self):
        payload = RegistroInstalacionCreate(**registro_data())
        preview = build_preview(payload)
        self.assertEqual(preview.desglose.total_cop, 350000)
        self.assertEqual(preview.desglose.conceptos[0].importe_cop, 350000)

    def test_no_acepta_totales_del_navegador(self):
        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(
                **registro_data(precio_total_cop=1, desglose={}, importe_cop=1)
            )

    def test_telefono_unico_se_adapta_al_contrato_existente(self):
        payload = RegistroInstalacionCreate(**registro_data())
        self.assertEqual(payload.cliente.telefono, "3001234567")
        self.assertEqual(payload.cliente.contacto, "3001234567")

        legacy = registro_data()
        legacy["cliente"] = {
            "documento": "CC-100",
            "nombre": "Propietario",
            "contacto": "3009999999",
        }
        adaptado = RegistroInstalacionCreate(**legacy)
        self.assertEqual(adaptado.cliente.telefono, "3009999999")
        self.assertEqual(adaptado.cliente.contacto, "3009999999")


if __name__ == "__main__":
    pass
