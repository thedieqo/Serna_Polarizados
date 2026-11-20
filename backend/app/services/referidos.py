"""Consulta y consumo de referidos en la transacción de la nueva instalación."""
from datetime import datetime, timezone
from sqlalchemy import select, func
from app.db.registro_tables import clientes, vehiculos, instalaciones


def normalizar_placa(placa):
    return ''.join(placa.upper().split()).replace('-', '')


def consultar_referido(db, placa, bloquear=False, documento_receptor=None):
    normal = normalizar_placa(placa)
    expr = func.replace(func.replace(func.upper(vehiculos.c.placa), ' ', ''), '-', '')
    propietarios = db.execute(select(vehiculos.c.cliente_id).where(expr == normal)).scalars().all()
    if len(set(propietarios)) != 1:
        return {'disponible':False, 'placa':normal, 'motivo':'No se encontró una placa única registrada.'}
    cliente_id = propietarios[0]
    consulta = select(clientes).where(clientes.c.id == cliente_id)
    if bloquear:
        # Serializa dos canjes simultáneos, también cuando usan placas distintas del mismo cliente.
        consulta = consulta.with_for_update()
    cliente = db.execute(consulta).mappings().one()
    base = {'placa':normal, 'cliente_id':cliente_id, 'nombre':cliente['nombre']}
    if documento_receptor and cliente['documento'].strip().casefold() == documento_receptor.strip().casefold():
        return base | {'disponible':False, 'motivo':'El referido debe ser otro cliente.'}
    usada = db.execute(select(instalaciones.c.id).where(
        instalaciones.c.desglose_precios['cobro']['referido']['cliente_id'].as_integer() == cliente_id
    ).limit(1)).scalar()
    if usada is not None:
        return base | {'disponible':False, 'usado_en':f'SP{usada}', 'motivo':f'Referido ya utilizado en SP{usada}.'}
    anterior = db.execute(select(instalaciones.c.id).join(vehiculos, instalaciones.c.vehiculo_id == vehiculos.c.id).where(
        vehiculos.c.cliente_id == cliente_id, expr == normal,
        instalaciones.c.tipo_servicio.in_(['polarizado','ambos']),
        instalaciones.c.estado != 'anulado',
        instalaciones.c.fecha <= datetime.now(timezone.utc),
    ).limit(1)).scalar()
    if anterior is None:
        return base | {'disponible':False, 'motivo':'Esta placa no tiene un polarizado previo vigente a la fecha.'}
    return base | {'disponible':True, 'motivo':'Referido disponible: 5 % para un nuevo cliente.'}
