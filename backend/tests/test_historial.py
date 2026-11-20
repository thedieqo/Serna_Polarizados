from datetime import datetime, timezone
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.instalaciones import read_detalle, read_historial
from app.db.base import Base
from app.models.cliente import Cliente
from app.models.instalacion import Instalacion
from app.models.vehiculo import Vehiculo


class HistorialTests(TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

        with self.Session() as db:
            cliente_uno = Cliente(
                nombre="Propietario Uno", documento="CC-111", contacto="3001111111", email="prueba@example.com"
            )
            cliente_dos = Cliente(
                nombre="Propietario Dos", documento="CC-222", contacto="3002222222"
            )
            db.add_all([cliente_uno, cliente_dos])
            db.flush()
            vehiculo_uno = Vehiculo(
                placa="ABC111", descripcion="Corolla", cliente_id=cliente_uno.id
            )
            vehiculo_dos = Vehiculo(
                placa="XYZ222", descripcion="Mazda", cliente_id=cliente_dos.id
            )
            db.add_all([vehiculo_uno, vehiculo_dos])
            db.flush()
            db.add_all(
                [
                    Instalacion(
                        vehiculo_id=vehiculo_uno.id,
                        fecha=datetime(2026, 1, 1, tzinfo=timezone.utc),
                        tipo_servicio="polarizado",
                        zonas=[{"zona": "parabrisas", "opacidad_aplicada": "20"}],
                        asignaciones_instaladores=[
                            {"zona": "parabrisas", "instalador": "Daniel"}
                        ],
                        retiro_material_anterior=False,
                        estado="programado",
                    ),
                    Instalacion(
                        vehiculo_id=vehiculo_uno.id,
                        fecha=datetime(2026, 3, 1, tzinfo=timezone.utc),
                        tipo_servicio="polarizado",
                        zonas=[
                            {
                                "vidrio": "laterales_delanteros",
                                "tecnologia": "Ultra HD",
                                "opacidad": "5 %",
                            }
                        ],
                        asignaciones_instaladores=[
                            {"instalador": "Joseth Mora"}
                        ],
                        retiro_material_anterior=True,
                        estado="finalizado",
                    ),
                    Instalacion(
                        vehiculo_id=vehiculo_dos.id,
                        fecha=datetime(2026, 3, 1, tzinfo=timezone.utc),
                        tipo_servicio="ambos",
                        zonas=[{"zona": "luneta", "opacidad_aplicada": "35"}],
                        asignaciones_instaladores=[
                            {"zona": "luneta", "instalador": "Daniel"}
                        ],
                        retiro_material_anterior=False,
                        estado="programado",
                    ),
                ]
            )
            db.commit()

    def tearDown(self):
        self.engine.dispose()

    def test_orden_fecha_descendente_y_desempate_id_descendente(self):
        with self.Session() as db:
            historial = read_historial(q=None, skip=0, limit=10, db=db)
        self.assertEqual([item.id for item in historial.items], [3, 2, 1])
        self.assertEqual(historial.total, 3)

    def test_paginacion(self):
        with self.Session() as db:
            primera = read_historial(q=None, skip=0, limit=2, db=db)
            segunda = read_historial(q=None, skip=2, limit=2, db=db)
        self.assertEqual([item.id for item in primera.items], [3, 2])
        self.assertEqual([item.id for item in segunda.items], [1])
        self.assertEqual(primera.total, 3)

    def test_busqueda_en_base_por_documento_y_placa(self):
        with self.Session() as db:
            por_documento = read_historial(q="CC-111", skip=0, limit=10, db=db)
            por_placa = read_historial(q="XYZ222", skip=0, limit=10, db=db)
        self.assertEqual([item.id for item in por_documento.items], [2, 1])
        self.assertEqual([item.id for item in por_placa.items], [3])

    def test_detalle_muestra_datos_de_propietario_vehiculo_y_trabajo(self):
        with self.Session() as db:
            detalle = read_detalle(instalacion_id=2, db=db)
        self.assertEqual(detalle.cliente_documento, "CC-111")
        self.assertEqual(detalle.cliente_nombre, "Propietario Uno")
        self.assertEqual(detalle.vehiculo_placa, "ABC111")
        self.assertEqual(detalle.vidrios, ["laterales_delanteros"])
        self.assertEqual(detalle.tecnologias, ["Ultra HD"])
        self.assertEqual(detalle.opacidades, ["5 %"])
        self.assertEqual(detalle.instaladores, ["Joseth Mora"])
        self.assertIsNone(detalle.desglose_precios)

    def test_detalle_incluye_correo_y_no_inventa_datos_historicos(self):
        with self.Session() as db:
            detalle = read_detalle(instalacion_id=1, db=db)
        self.assertEqual(detalle.cliente_email, "prueba@example.com")
        self.assertIsNone(detalle.precio_total_cop)
        self.assertIsNone(detalle.detalles_vidrios[0].tecnologia)
        self.assertEqual(detalle.detalles_vidrios[0].instaladores, ["Daniel"])

    def test_detalle_conserva_asociacion_de_panel_tecnologia_opacidad_e_instalador(self):
        with self.Session() as db:
            fila = db.get(Instalacion, 2)
            fila.zonas = [
                {"vidrio": "Techo", "panel": "Delantero", "tecnologia": "Ultra HD", "opacidad": "5 %"},
                {"vidrio": "Techo", "panel": "Trasero", "tecnologia": "Ceramic IR", "opacidad": "20 %"},
            ]
            fila.asignaciones_instaladores = [
                {"vidrio": "Techo", "panel": "Trasero", "instalador": "Daniel"},
                {"vidrio": "Techo", "panel": "Delantero", "instalador": "Joseth"},
            ]
            fila.precio_total_cop = 500000
            fila.vehiculo.marca = "Mazda"
            fila.vehiculo.cliente.telefono = "3001234567"
            fila.tipo_factura = "electronica"
            db.commit()
            db.expunge_all()
            detalle = read_detalle(instalacion_id=2, db=db)
        self.assertEqual(detalle.vehiculo_marca, "Mazda")
        self.assertEqual(detalle.cliente_telefono, "3001234567")
        self.assertEqual(detalle.tipo_factura, "electronica")
        self.assertEqual(detalle.precio_total_cop, 500000)
        self.assertEqual(detalle.detalles_vidrios[0].instaladores, ["Joseth"])
        self.assertEqual(detalle.detalles_vidrios[1].instaladores, ["Daniel"])
        self.assertEqual(detalle.detalles_vidrios[1].tecnologia, "Ceramic IR")
        self.assertEqual(detalle.detalles_vidrios[1].opacidad, "20 %")

    def test_asignacion_sin_vidrio_no_se_atribuye_arbitrariamente(self):
        with self.Session() as db:
            detalle = read_detalle(instalacion_id=2, db=db)
        self.assertEqual(detalle.detalles_vidrios[0].instaladores, [])
        self.assertEqual(detalle.instaladores, ["Joseth Mora"])


if __name__ == "__main__":
    pass
