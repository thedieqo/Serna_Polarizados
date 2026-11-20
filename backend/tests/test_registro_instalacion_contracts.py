from unittest import TestCase
from unittest.mock import patch

from pydantic import ValidationError

from app.core.catalogs import (
    INSTALADORES,
    OPACIDADES_POLARIZADO,
    TECNOLOGIAS_POLARIZADO,
    TIPOS_FACTURA,
    VIDRIOS_POLARIZADO,
    catalogos_response,
    label_for,
)
from app.core.config import Settings
from app.db.schema_status import EXPECTED_COLUMNS, EXPECTED_TABLES, missing_requirements
from app.schemas.registro_instalacion import RegistroInstalacionCreate, build_preview


class FakeInspector:
    def __init__(self, tables, columns):
        self.tables = set(tables)
        self.columns = columns

    def get_table_names(self):
        return list(self.tables)

    def get_columns(self, table):
        return [{"name": column} for column in self.columns.get(table, ())]


def cliente_data():
    return {
        "documento": "CC-TEST",
        "nombre": "Cliente Prueba",
        "contacto": "3000000000",
        "telefono": "3000000001",
        "email": "cliente@example.com",
    }


def vehiculo_data():
    return {
        "placa": "TEST123",
        "marca": "Marca Prueba",
        "descripcion": "Modelo Prueba",
    }


def detalle_data(**overrides):
    data = {
        "vidrio_id": "parabrisas",
        "panel": None,
        "tecnologia_id": "ultra_hd",
        "opacidad_id": "20",
        "instalador_id": "daniel_mira",
    }
    data.update(overrides)
    return data


def registro_data(**overrides):
    data = {
        "cliente": cliente_data(),
        "vehiculo": vehiculo_data(),
        "tipo_factura": "normal",
        "detalles": [detalle_data()],
    }
    data.update(overrides)
    return data


class CatalogosTests(TestCase):
    def test_catalogos_confirmados(self):
        self.assertEqual(
            [item["label"] for item in TECNOLOGIAS_POLARIZADO],
            ["High Definition Premium", "Ultra HD", "Color Stable", "Ceramic IR"],
        )
        self.assertEqual([item["label"] for item in OPACIDADES_POLARIZADO], ["5 %", "20 %", "35 %"])
        self.assertEqual([item["label"] for item in INSTALADORES], ["Daniel Mira", "Joseth Mora"])
        self.assertEqual([item["id"] for item in TIPOS_FACTURA], ["normal", "electronica"])
        solar = next(item for item in VIDRIOS_POLARIZADO if item["id"] == "sunroof_doble")
        self.assertEqual(solar["paneles"], ["delantero", "trasero"])

        response = catalogos_response()
        self.assertEqual(response["servicio"], "polarizado")
        self.assertEqual(len(response["vidrios"]), len(VIDRIOS_POLARIZADO))

    def test_admin_allowlist_empty_by_default(self):
        with patch.dict("os.environ", {}, clear=True):
            settings = Settings(_env_file=None)
        self.assertEqual(settings.admin_emails, frozenset())

    def test_admin_allowlist_normalizes_configured_emails(self):
        with patch.dict(
            "os.environ",
            {"ADMIN_EMAILS": " Admin@Example.COM , diego@example.com "},
            clear=True,
        ):
            settings = Settings(_env_file=None)
        self.assertEqual(
            settings.admin_emails,
            frozenset({"admin@example.com", "diego@example.com"}),
        )


class RegistroContractsTests(TestCase):
    def test_preview_permite_tecnologias_distintas_por_vidrio(self):
        payload = RegistroInstalacionCreate(
            **registro_data(
                detalles=[
                    detalle_data(vidrio_id="parabrisas", tecnologia_id="ultra_hd"),
                    detalle_data(vidrio_id="luneta", tecnologia_id="ceramic_ir"),
                ]
            )
        )
        preview = build_preview(payload)

        self.assertEqual(preview.cantidad_vidrios, 2)
        self.assertEqual(
            preview.tecnologias_utilizadas,
            ["Ceramic IR", "Ultra HD"],
        )
        self.assertFalse(preview.guardado_habilitado)
        self.assertEqual(preview.detalles[0].opacidad, "20 %")
        self.assertEqual(preview.detalles[0].instalador, "Daniel Mira")
        self.assertEqual(label_for("tipos_factura", payload.tipo_factura), "Normal")

    def test_rechaza_vidrio_repetido(self):
        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(
                **registro_data(
                    detalles=[
                        detalle_data(vidrio_id="parabrisas", tecnologia_id="ultra_hd"),
                        detalle_data(vidrio_id="parabrisas", tecnologia_id="ceramic_ir"),
                    ]
                )
            )

    def test_sunroof_doble_requiere_ambos_paneles(self):
        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(
                **registro_data(
                    detalles=[
                        detalle_data(vidrio_id="sunroof_doble", panel="delantero"),
                    ]
                )
            )

        payload = RegistroInstalacionCreate(
            **registro_data(
                detalles=[
                    detalle_data(vidrio_id="sunroof_doble", panel="delantero"),
                    detalle_data(vidrio_id="sunroof_doble", panel="trasero"),
                ]
            )
        )
        self.assertEqual(len(payload.detalles), 2)

    def test_rechaza_valores_no_confirmados(self):
        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(
                **registro_data(
                    detalles=[detalle_data(tecnologia_id="no_confirmada")]
                )
            )

        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(**registro_data(tipo_factura="dian"))

        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(
                **registro_data(detalles=[detalle_data(vidrio_id="puerta")])
            )

    def test_estado_programado_unico_en_preview(self):
        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(**registro_data(estado="finalizado"))


class SchemaStatusTests(TestCase):
    def test_detecta_tablas_y_columnas_ausentes(self):
        inspector = FakeInspector(
            tables=["clientes", "vehiculos", "instalaciones"],
            columns={"clientes": ["id"], "vehiculos": ["id"], "instalaciones": ["id"]},
        )
        missing = missing_requirements(inspector)

        self.assertIn("clientes.telefono", missing)
        self.assertIn("clientes.email", missing)
        self.assertIn("vehiculos.marca", missing)
        self.assertIn("instalaciones.tipo_factura", missing)
        for table in EXPECTED_TABLES:
            self.assertIn(f"tabla:{table}", missing)

    def test_sin_requisitos_faltantes_cuando_esquema_esta_listo(self):
        tables = ["clientes", "vehiculos", "instalaciones", *EXPECTED_TABLES]
        columns = {table: list(values) for table, values in EXPECTED_COLUMNS.items()}
        inspector = FakeInspector(tables=tables, columns=columns)
        self.assertEqual(missing_requirements(inspector), [])


if __name__ == "__main__":
    pass
