from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import patch

import app.api.v1.instalaciones as instalaciones_api
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.instalaciones import create_novedad_garantia
from app.db.registro_tables import clientes, instalaciones, instalacion_novedades, metadata, vehiculos
from app.schemas.garantia import NovedadGarantiaCreate
from app.services.garantias import guardar_novedad


class GarantiaTests(TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        with self.Session() as db:
            cliente_id = db.execute(
                insert(clientes).values(
                    documento="CC-100",
                    nombre="Propietario",
                    contacto="3001234567",
                    telefono="3001234567",
                    email="prop@example.com",
                )
            ).inserted_primary_key[0]
            vehiculo_id = db.execute(
                insert(vehiculos).values(
                    placa="ABC123",
                    descripcion="Corolla",
                    cliente_id=cliente_id,
                    marca="Toyota",
                )
            ).inserted_primary_key[0]
            db.execute(
                insert(instalaciones).values(
                    vehiculo_id=vehiculo_id,
                    tipo_servicio="polarizado",
                    zonas=[],
                    asignaciones_instaladores=[],
                    retiro_material_anterior=False,
                    estado="programado",
                    tipo_factura="normal",
                )
            )
            db.commit()

    def tearDown(self):
        self.engine.dispose()

    def _payload(self):
        return NovedadGarantiaCreate(
            instalacion_id=1,
            fecha_atencion=datetime(2026, 11, 20, 10, 0, tzinfo=timezone.utc),
            motivo="Ajuste de borde",
            descripcion="Se ajustó el radical sin modificar la instalación original",
        )

    def test_varias_novedades_sin_sobrescribir_la_original(self):
        payload = self._payload()
        with self.Session() as db:
            primera = guardar_novedad(db, payload, "admin@example.com")
            segunda = guardar_novedad(
                db,
                NovedadGarantiaCreate(
                    instalacion_id=1,
                    fecha_atencion=datetime(2026, 11, 21, 10, 0, tzinfo=timezone.utc),
                    motivo="Revisión",
                    descripcion="Se verificó el trabajo anterior",
                ),
                "admin@example.com",
            )
            filas = db.execute(select(instalacion_novedades)).mappings().all()
            original = db.execute(
                select(instalaciones).where(instalaciones.c.id == 1)
            ).mappings().one()

        self.assertNotEqual(primera.id, segunda.id)
        self.assertEqual(len(filas), 2)
        self.assertEqual({fila["registrado_por"] for fila in filas}, {"admin@example.com"})
        self.assertEqual(original["tipo_servicio"], "polarizado")
        self.assertEqual(original["estado"], "programado")

    def test_no_acepta_administrador_del_cuerpo(self):
        with self.assertRaises(ValidationError):
            NovedadGarantiaCreate(
                instalacion_id=1,
                fecha_atencion=datetime(2026, 11, 20, 10, 0, tzinfo=timezone.utc),
                motivo="Ajuste",
                descripcion="Trabajo realizado",
                registrado_por="atacante@example.com",
            )

    def test_endpoint_de_novedad_permanece_cerrado(self):
        with self.assertRaises(HTTPException) as contexto, patch.object(
            instalaciones_api.settings, "REGISTRO_WRITE_ENABLED", False
        ):
            create_novedad_garantia(
                1, self._payload(), db=None, administrador="admin@example.com"
            )
        self.assertEqual(contexto.exception.status_code, 503)
        self.assertEqual(
            contexto.exception.detail["code"], "ESCRITURA_NO_HABILITADA"
        )


if __name__ == "__main__":
    pass
