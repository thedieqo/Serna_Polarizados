from unittest import TestCase
from types import SimpleNamespace
from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import Session
from app.db.registro_tables import metadata, inventario, inventario_movimientos
from app.services.inventario import inicializar, consumos, descontar, InventarioError

class InventarioTests(TestCase):
    def setUp(self):
        self.engine=create_engine('sqlite://')
        metadata.create_all(self.engine)
        self.db=Session(self.engine)
        inicializar(self.db);self.db.commit()
    def tearDown(self):
        self.db.close();self.engine.dispose()
    def detalle(self,vidrio,seguridad=False):
        return SimpleNamespace(vidrio_id=vidrio,tecnologia_id='ultra_hd',opacidad_id='20',pelicula_seguridad=seguridad)
    def test_24_combinaciones_idempotente(self):
        inicializar(self.db)
        self.assertEqual(self.db.execute(select(func.count()).select_from(inventario)).scalar(),24)
        self.assertEqual(self.db.execute(select(func.count()).select_from(inventario_movimientos)).scalar(),24)
    def test_medidas_y_pelicula_solo(self):
        plan=consumos([self.detalle(v) for v in ['parabrisas','laterales_delanteros','laterales_traseros','luneta','sunroof_simple','sunroof_doble','sunroof_doble']])
        self.assertEqual(plan,{'ultra_hd:20:polarizado':680})
        self.assertEqual(consumos([self.detalle('laterales_delanteros',True),self.detalle('laterales_traseros',True)]),{'ultra_hd:20:pelicula_seguridad':160})
    def test_descuento_y_movimiento(self):
        descontar(self.db,1,[self.detalle('parabrisas')]);self.db.commit()
        self.assertEqual(self.db.execute(select(inventario.c.disponible_cm).where(inventario.c.sku=='ultra_hd:20:polarizado')).scalar(),19850)
        self.assertEqual(self.db.execute(select(inventario_movimientos.c.cantidad_cm).where(inventario_movimientos.c.instalacion_id==1)).scalar(),-150)
    def test_sin_stock_revierte_todo(self):
        self.db.execute(update(inventario).where(inventario.c.sku=='ultra_hd:20:polarizado').values(disponible_cm=10));self.db.commit()
        with self.assertRaises(InventarioError):
            try: descontar(self.db,1,[self.detalle('parabrisas'),self.detalle('laterales_delanteros',True)])
            except InventarioError:
                self.db.rollback();raise
        self.assertEqual(self.db.execute(select(inventario.c.disponible_cm).where(inventario.c.sku=='ultra_hd:20:pelicula_seguridad')).scalar(),20000)
        self.assertEqual(self.db.execute(select(func.count()).select_from(inventario_movimientos).where(inventario_movimientos.c.instalacion_id==1)).scalar(),0)
