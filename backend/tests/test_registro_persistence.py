from unittest import TestCase
from unittest.mock import patch

import app.api.v1.instalaciones as instalaciones_api
from pydantic import ValidationError
from fastapi import HTTPException
from sqlalchemy import create_engine, event, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.instalaciones import create_registro
from app.db.registro_tables import (
    catalogo_instaladores,
    catalogo_opacidades_polarizado,
    catalogo_tecnologias_polarizado,
    catalogo_tipos_factura,
    catalogo_vidrios_polarizado,
    clientes,
    instalacion_detalles,
    instalaciones,
    metadata,
    vehiculos,
)
from app.schemas.registro_instalacion import RegistroInstalacionCreate
from app.services.registro_instalacion import (
    RegistroConflictError,
    _map_integrity_error,
    guardar_registro,
)


def _payload() -> dict:
    return {
        "cliente": {
            "documento": "CC-100",
            "nombre": "Propietario Ejemplo",
            "contacto": "3001234567",
            "telefono": "3001234567",
            "email": "prop@example.com",
        },
        "vehiculo": {
            "vehiculo_id": None,
            "placa": "ABC123",
            "marca": "Toyota",
            "descripcion": "Corolla 2020",
        },
        "tipo_factura": "electronica",
        "fecha": None,
        "retiro_material_anterior": True,
        "observaciones": "Instalación de prueba",
        "estado": "programado",
        "detalles": [
            {
                "vidrio_id": "parabrisas",
                "panel": None,
                "tecnologia_id": "ultra_hd",
                "opacidad_id": "35",
                "instalador_id": "daniel_mira",
            },
            {
                "vidrio_id": "sunroof_doble",
                "panel": "delantero",
                "tecnologia_id": "ceramic_ir",
                "opacidad_id": "20",
                "instalador_id": "joseth_mora",
            },
            {
                "vidrio_id": "sunroof_doble",
                "panel": "trasero",
                "tecnologia_id": "ceramic_ir",
                "opacidad_id": "20",
                "instalador_id": "joseth_mora",
            },
        ],
    }


def _seed_catalogos(db: Session) -> None:
    db.execute(
        insert(catalogo_tecnologias_polarizado),
        [
            {"id": "high_definition_premium", "label": "High Definition Premium"},
            {"id": "ultra_hd", "label": "Ultra HD"},
            {"id": "color_stable", "label": "Color Stable"},
            {"id": "ceramic_ir", "label": "Ceramic IR"},
        ],
    )
    db.execute(
        insert(catalogo_opacidades_polarizado),
        [
            {"id": "5", "label": "5 %"},
            {"id": "20", "label": "20 %"},
            {"id": "35", "label": "35 %"},
        ],
    )
    db.execute(
        insert(catalogo_instaladores),
        [
            {"id": "daniel_mira", "label": "Daniel Mira"},
            {"id": "joseth_mora", "label": "Joseth Mora"},
        ],
    )
    db.execute(
        insert(catalogo_tipos_factura),
        [
            {"id": "normal", "label": "Normal"},
            {"id": "electronica", "label": "Electrónica"},
        ],
    )
    db.execute(
        insert(catalogo_vidrios_polarizado),
        [
            {"id": "parabrisas", "label": "Parabrisas"},
            {"id": "sunroof_doble", "label": "Techo solar doble"},
        ],
    )
    db.commit()


class RegistroPersistenceTests(TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        @event.listens_for(self.engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        metadata.create_all(self.engine)
        self.Session = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
        with self.Session() as db:
            _seed_catalogos(db)

    def tearDown(self):
        self.engine.dispose()

    def _guardar(self, data=None):
        payload = RegistroInstalacionCreate(**(data or _payload()))
        with self.Session() as db:
            return guardar_registro(db, payload)

    def _count(self, tabla) -> int:
        with self.Session() as db:
            return db.execute(select(func.count()).select_from(tabla)).scalar_one()

    def test_guarda_registro_completo_y_respeta_columnas_historicas(self):
        resultado = self._guardar()

        self.assertEqual(resultado.cliente_reutilizado, False)
        self.assertEqual(resultado.vehiculo_reutilizado, False)
        self.assertEqual(resultado.detalles_guardados, 3)
        self.assertEqual(resultado.desglose.estado, "pendiente")
        self.assertIsNone(resultado.desglose.total_cop)
        self.assertEqual(self._count(clientes), 1)
        self.assertEqual(self._count(vehiculos), 1)
        self.assertEqual(self._count(instalaciones), 1)
        self.assertEqual(self._count(instalacion_detalles), 3)

        with self.Session() as db:
            instalacion = db.execute(select(instalaciones)).mappings().one()
            self.assertEqual(instalacion["tipo_servicio"], "polarizado")
            self.assertEqual(instalacion["tipo_factura"], "electronica")
            self.assertEqual(instalacion["estado"], "programado")
            self.assertEqual(instalacion["zonas"][0]["vidrio"], "Parabrisas")
            self.assertEqual(instalacion["zonas"][2]["panel"], "Trasero")
            self.assertEqual(
                instalacion["asignaciones_instaladores"][0]["instalador"],
                "Daniel Mira",
            )
            self.assertEqual(instalacion["moneda"], "COP")
            self.assertEqual(instalacion["precio_estado"], "pendiente")
            self.assertIsNone(instalacion["precio_total_cop"])
            self.assertEqual(instalacion["desglose_precios"]["estado"], "pendiente")
            self.assertEqual(
                instalacion["tarifas_aplicadas"]["version"], "2026-11-18"
            )

    def test_reutiliza_cliente_y_vehiculo_por_documento_y_placa(self):
        with self.Session() as db:
            cliente = db.execute(
                insert(clientes).values(
                    documento="CC-100",
                    nombre="  PROPIETARIO EJEMPLO ",
                    contacto="3001234567",
                    telefono="3001234567",
                    email="PROP@EXAMPLE.COM",
                )
            ).inserted_primary_key[0]
            db.execute(
                insert(vehiculos).values(
                    placa="ABC123",
                    descripcion="Corolla 2020",
                    cliente_id=cliente,
                    marca="  Toyota ",
                )
            )
            db.commit()

        resultado = self._guardar()

        self.assertEqual(resultado.cliente_reutilizado, True)
        self.assertEqual(resultado.vehiculo_reutilizado, True)
        self.assertEqual(self._count(clientes), 1)
        self.assertEqual(self._count(vehiculos), 1)
        self.assertEqual(self._count(instalaciones), 1)

    def test_conflicto_cuando_vehiculo_pertenece_a_otro_propietario(self):
        with self.Session() as db:
            cliente_uno = db.execute(
                insert(clientes).values(
                    documento="CC-100",
                    nombre="Propietario Ejemplo",
                    contacto="3001234567",
                    telefono="3001234567",
                    email="prop@example.com",
                )
            ).inserted_primary_key[0]
            cliente_dos = db.execute(
                insert(clientes).values(
                    documento="CC-200",
                    nombre="Otro Propietario",
                    contacto="3009999999",
                    telefono="3009999999",
                    email="otro@example.com",
                )
            ).inserted_primary_key[0]
            db.execute(
                insert(vehiculos).values(
                    placa="ABC123",
                    descripcion="Corolla 2020",
                    cliente_id=cliente_dos,
                    marca="Toyota",
                )
            )
            db.commit()
            self.assertIsNotNone(cliente_uno)

        with self.assertRaises(RegistroConflictError) as contexto:
            self._guardar()

        self.assertEqual(contexto.exception.code, "VEHICULO_PERTENECE_A_OTRO_CLIENTE")
        self.assertEqual(self._count(instalaciones), 0)

    def test_conflicto_cuanto_cliente_tiene_datos_diferentes(self):
        with self.Session() as db:
            db.execute(
                insert(clientes).values(
                    documento="CC-100",
                    nombre="Nombre Distinto",
                    contacto="3001234567",
                    telefono="3001234567",
                    email="prop@example.com",
                )
            )
            db.commit()

        with self.assertRaises(RegistroConflictError) as contexto:
            self._guardar()

        self.assertEqual(contexto.exception.code, "DATOS_CLIENTE_DIFERENTES")
        self.assertIn("nombre del propietario", contexto.exception.fields)
        self.assertEqual(self._count(instalaciones), 0)

    def test_conflicto_cuando_vehiculo_tiene_datos_diferentes(self):
        with self.Session() as db:
            cliente = db.execute(
                insert(clientes).values(
                    documento="CC-100",
                    nombre="Propietario Ejemplo",
                    contacto="3001234567",
                    telefono="3001234567",
                    email="prop@example.com",
                )
            ).inserted_primary_key[0]
            db.execute(
                insert(vehiculos).values(
                    placa="ABC123",
                    descripcion="Corolla 2020",
                    cliente_id=cliente,
                    marca="Mazda",
                )
            )
            db.commit()

        with self.assertRaises(RegistroConflictError) as contexto:
            self._guardar()

        self.assertEqual(contexto.exception.code, "DATOS_VEHICULO_DIFERENTES")
        self.assertIn("marca del vehículo", contexto.exception.fields)
        self.assertEqual(self._count(instalaciones), 0)

    def test_rollback_completo_si_falla_detalle(self):
        with patch(
            "app.services.registro_instalacion._insert_detalles",
            side_effect=RuntimeError("fallo controlado"),
        ):
            with self.assertRaises(RuntimeError):
                self._guardar()

        self.assertEqual(self._count(clientes), 0)
        self.assertEqual(self._count(vehiculos), 0)
        self.assertEqual(self._count(instalaciones), 0)
        self.assertEqual(self._count(instalacion_detalles), 0)

    def test_duplicado_concurrente_se_mapea_a_conflicto(self):
        class FakeDiag:
            constraint_name = "clientes_documento_key"

        class FakeOriginal:
            pgcode = "23505"
            diag = FakeDiag()

        def __str__(self):
            return "duplicate key value violates unique constraint"

        original = FakeOriginal()
        error = IntegrityError("INSERT", {}, original)
        error.orig = original

        mapeado = _map_integrity_error(error)

        self.assertEqual(mapeado.code, "DUPLICADO_CONCURRENTE")
        self.assertIn("documento", mapeado.message)

    def test_endpoint_escritura_cerrado_por_defecto(self):
        payload = RegistroInstalacionCreate(**_payload())

        with self.assertRaises(HTTPException) as contexto, patch.object(
            instalaciones_api.settings, "REGISTRO_WRITE_ENABLED", False
        ):
            create_registro(payload, db=None, administrador="admin@example.com")

        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(
            contexto.exception.detail["code"], "ESCRITURA_NO_HABILITADA"
        )

    def test_no_acepta_identidad_ni_correo_del_frontend(self):
        data = _payload()
        data["admin_email"] = "atacante@example.com"
        data["cliente"]["user_id"] = "auth0|123"

        with self.assertRaises(ValidationError):
            RegistroInstalacionCreate(**data)
