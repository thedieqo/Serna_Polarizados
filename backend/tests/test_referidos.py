from datetime import datetime, timezone
from unittest import TestCase
from pydantic import ValidationError
from sqlalchemy import create_engine, select, update, insert
from sqlalchemy.orm import Session
from app.db.registro_tables import metadata, instalaciones, clientes, vehiculos
from app.schemas.registro_instalacion import RegistroInstalacionCreate, desglose_registro
from app.services.registro_instalacion import guardar_registro, RegistroConflictError
from app.services.referidos import consultar_referido
from test_registro_persistence import _payload, _seed_catalogos


class ReferidosTests(TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        metadata.create_all(self.engine)
        self.db = Session(self.engine)
        _seed_catalogos(self.db)
        data = _payload()
        data['fecha'] = '2020-01-01T15:00:00Z'
        self.original = guardar_registro(self.db, RegistroInstalacionCreate(**data))

    def tearDown(self):
        self.db.close(); self.engine.dispose()

    def receptor(self, documento='NEW-1', placa='NEW111'):
        data = _payload()
        data['cliente'].update(documento=documento, nombre='Nuevo cliente')
        data['vehiculo']['placa'] = placa
        data.update(tipo_descuento='referido', referido_placa=' abc 123 ', pagos=[{'medio':'efectivo','monto_cop':1377500}])
        return RegistroInstalacionCreate(**data)

    def test_consultar_no_consume_guardar_si_y_segundo_canje_se_rechaza(self):
        for _ in range(2):
            self.assertTrue(consultar_referido(self.db,'ABC123')['disponible'])
        guardado = guardar_registro(self.db,self.receptor())
        consulta = consultar_referido(self.db,'ABC123')
        self.assertFalse(consulta['disponible'])
        self.assertEqual(consulta['usado_en'],f'SP{guardado.instalacion_id}')
        with self.assertRaises(RegistroConflictError):
            guardar_registro(self.db,self.receptor('NEW-2','NEW222'))
        filas = self.db.execute(select(instalaciones)).mappings().all()
        self.assertEqual(len(filas),2)
        self.assertEqual(filas[-1]['desglose_precios']['cobro']['referido']['cliente_id'],self.original.cliente_id)
        self.assertEqual(filas[-1]['precio_total_cop'],1377500)

    def test_un_solo_canje_por_cliente_aunque_tenga_dos_placas(self):
        segunda = _payload();segunda['vehiculo']['placa']='XYZ987';segunda['fecha']='2020-01-02T15:00:00Z'
        guardar_registro(self.db,RegistroInstalacionCreate(**segunda))
        guardar_registro(self.db,self.receptor())
        self.assertFalse(consultar_referido(self.db,'XYZ987')['disponible'])

    def test_no_autorreferido_placa_inexistente_o_instalacion_anulada(self):
        with self.assertRaises(RegistroConflictError):
            guardar_registro(self.db,self.receptor('CC-100','NEW111'))
        self.assertFalse(consultar_referido(self.db,'NO123')['disponible'])
        self.db.execute(update(instalaciones).values(estado='anulado'));self.db.commit()
        self.assertFalse(consultar_referido(self.db,'ABC123')['disponible'])

    def test_transaccion_fallida_no_consume_referido(self):
        # El vehículo de origen pertenece a otra persona: falla después de bloquear el referido.
        with self.assertRaises(RegistroConflictError):
            guardar_registro(self.db,self.receptor(placa='ABC123'))
        self.assertTrue(consultar_referido(self.db,'ABC123')['disponible'])

    def test_porcentajes_del_servidor_no_acumulables_y_comision_neta(self):
        for tipo, porcentaje in [('referido',5),('agenda',10),('especial',15)]:
            data=_payload();data.update(tipo_descuento=tipo,pagos=[],motivo_descuento='Navidad')
            if tipo=='referido':data['referido_placa']='ABC123'
            cobro=desglose_registro(RegistroInstalacionCreate(**data))['cobro']
            self.assertEqual(cobro['descuento_cop'],1450000*porcentaje//100)
            self.assertEqual(cobro['total_cop'],1450000-cobro['descuento_cop'])
            self.assertEqual(cobro['comision_admin_cop'],cobro['total_cop']*2//100)
        for cambios in [{'tipo_descuento':'referido'}, {'tipo_descuento':'especial'},
                        {'tipo_descuento':'agenda','descuento_cop':1},
                        {'tipo_descuento':['agenda','especial']}]:
            data=_payload();data.update(pagos=[],**cambios)
            with self.assertRaises(ValidationError):RegistroInstalacionCreate(**data)
