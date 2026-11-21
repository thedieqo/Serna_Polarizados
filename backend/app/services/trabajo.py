"""Ejecución real: identidad aprobada, vidrio único y stock en una transacción."""
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import hashlib
import json
from sqlalchemy import select, insert, update, func
from app.db.registro_tables import (trabajadores, instalaciones, vehiculos,
    confirmaciones_trabajo as confirmaciones, vidrios_realizados as realizados,
    inventario, inventario_movimientos)

BOGOTA = ZoneInfo('America/Bogota')

class TrabajoError(ValueError):
    pass


def trabajador(db, email, bloquear=False):
    q = select(trabajadores).where(trabajadores.c.email == email.lower(), trabajadores.c.activo.is_(True))
    if bloquear: q = q.with_for_update()
    return db.execute(q).mappings().first()


def opciones(desglose):
    if not desglose or desglose.get('ejecucion_version') != 1:
        return []
    resultado = []
    for i, d in enumerate(desglose['plan_vidrios']):
        tipo = d['vidrio_id']
        material = 'pelicula_seguridad' if d['pelicula_seguridad'] else 'polarizado'
        sku = f"{d['tecnologia_id']}:{d['opacidad_id']}:{material}"
        if tipo in ('laterales_delanteros', 'laterales_traseros'):
            zona = 'delantero' if tipo == 'laterales_delanteros' else 'trasero'
            partes = [(f'lateral_{lado}', f'Lateral {lado} {zona}', 12500, False) for lado in ('derecho','izquierdo')]
            partes += [(f'custodia_{lado}', f'Custodia {lado} {zona}', 6250, True) for lado in ('derecho','izquierdo')]
        else:
            label = {'parabrisas':'Parabrisas', 'luneta':'Panorámico trasero', 'sunroof_simple':'Sunroof sencillo', 'sunroof_doble':f"Sunroof doble · {d.get('panel')}"}[tipo]
            partes = [('unico', label, 25000, False)]
        for key, label, tarifa, opcional in partes:
            resultado.append({'slot':f'{i}:{key}', 'vidrio':label,'tipo':tipo, 'sku':sku,
                'tecnologia_id':d['tecnologia_id'], 'opacidad':d['opacidad_id'], 'material':material,
                'valor_cop':tarifa,'opcional':opcional})
    return resultado


def buscar(db, placa):
    normal = ''.join(placa.upper().split())
    q = select(instalaciones.c.id, instalaciones.c.fecha, instalaciones.c.desglose_precios, vehiculos.c.placa).join(vehiculos, instalaciones.c.vehiculo_id == vehiculos.c.id).where(func.replace(func.upper(vehiculos.c.placa), ' ', '') == normal).order_by(instalaciones.c.id.desc()).limit(30)
    resultados = []
    for row in db.execute(q).mappings():
        slots = opciones(row['desglose_precios'])
        if not slots: continue  # Histórico anterior al cambio: nunca descontar por segunda vez.
        hechos = set(db.execute(select(realizados.c.slot).where(realizados.c.instalacion_id == row['id'])).scalars())
        resultados.append({'id':row['id'], 'placa':row['placa'], 'fecha':row['fecha'],
                           'vidrios':[v | {'realizado':v['slot'] in hechos} for v in slots]})
    return resultados


def confirmar(db, email, solicitud):
    """El llamador hace commit; cualquier error revierte todo, incluido el inventario."""
    persona = trabajador(db, email, bloquear=True)
    if not persona: raise TrabajoError('Gerencia debe aprobar tu cuenta en esta sede antes de registrar trabajos.')
    datos = solicitud.model_dump(mode='json')
    huella = hashlib.sha256(json.dumps(datos, sort_keys=True).encode()).hexdigest()
    anterior = db.execute(select(confirmaciones).where(confirmaciones.c.id == str(solicitud.id))).mappings().first()
    if anterior:
        if anterior['trabajador_id'] != persona['id'] or anterior['solicitud_hash'] != huella:
            raise TrabajoError('La confirmación ya existe con otros datos.')
        return {'confirmado':True, 'repetido':True}
    venta = db.execute(select(instalaciones).where(instalaciones.c.id == solicitud.instalacion_id).with_for_update()).mappings().first()
    if not venta: raise TrabajoError('La instalación no existe en esta sede.')
    if venta['estado'] == 'anulado': raise TrabajoError('Esta instalación está anulada.')
    slots = {v['slot']:v for v in opciones(venta['desglose_precios'])}
    if not slots: raise TrabajoError('Este registro es anterior al nuevo control de trabajo; no puede descontarse nuevamente.')
    hechos = set(db.execute(select(realizados.c.slot).where(realizados.c.instalacion_id == venta['id'])).scalars())
    nuevos = []
    consumos = defaultdict(int)
    for corte in solicitud.vidrios:
        if corte.slot not in slots or corte.slot in hechos:
            raise TrabajoError('Uno de los vidrios ya fue confirmado o no pertenece a esta instalación. Actualiza la búsqueda.')
        hechos.add(corte.slot)
        slot = slots[corte.slot]
        if corte.tipo_parabrisas != 'normal' and slot['tipo'] != 'parabrisas':
            raise TrabajoError('La categoría camión/buseta solo se aplica al parabrisas delantero.')
        tarifa = 35000 if corte.tipo_parabrisas != 'normal' else slot['valor_cop']
        label = slot['vidrio'] + (f' · {corte.tipo_parabrisas}' if corte.tipo_parabrisas != 'normal' else '')
        cm = int(corte.metros * 100)
        consumos[slot['sku']] += cm
        nuevos.append({'confirmacion_id':str(solicitud.id),'instalacion_id':venta['id'], 'slot':corte.slot,
                       'vidrio':label, 'sku':slot['sku'],'cortado_cm':cm,'valor_cop':tarifa})
    ahora = datetime.now(timezone.utc)
    db.execute(insert(confirmaciones).values(id=str(solicitud.id), instalacion_id=venta['id'], trabajador_id=persona['id'], solicitud_hash=huella, created_at=ahora))
    for sku, cm in sorted(consumos.items()):
        r = db.execute(update(inventario).where(inventario.c.sku == sku, inventario.c.disponible_cm >= cm).values(disponible_cm=inventario.c.disponible_cm-cm))
        if r.rowcount != 1: raise TrabajoError('No hay material suficiente para los metros ingresados. Revisa el corte y el inventario.')
        db.execute(insert(inventario_movimientos).values(sku=sku, instalacion_id=venta['id'], confirmacion_id=str(solicitud.id), cantidad_cm=-cm, motivo=f'Corte confirmado · {persona["nombre"]}'))
    db.execute(insert(realizados), nuevos)
    desglose = dict(venta['desglose_precios'])
    desglose['mano_obra'] = list(desglose.get('mano_obra', [])) + [
        {'instalador_id':persona['id'],'instalador':persona['nombre'],'vidrio':n['vidrio'],'panel':None,
         'valor_cop':n['valor_cop'],'confirmado_en':ahora.isoformat(),'confirmacion_id':str(solicitud.id)} for n in nuevos]
    estado = 'finalizado' if all(v['opcional'] or key in hechos for key,v in slots.items()) else 'en_proceso'
    db.execute(update(instalaciones).where(instalaciones.c.id == venta['id']).values(desglose_precios=desglose, estado=estado))
    return {'confirmado':True,'ganado_cop':sum(n['valor_cop'] for n in nuevos),'metros':sum(consumos.values())/100}


def resumen(db, email):
    persona = trabajador(db, email)
    if not persona:
        return {'asignado':False, 'mensaje':'Gerencia debe crear y aprobar tu cuenta de instalador en esta sede.'}
    ahora = datetime.now(BOGOTA)
    inicio = ahora.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    fin = inicio.replace(year=inicio.year+1,month=1) if inicio.month == 12 else inicio.replace(month=inicio.month+1)
    corte = inicio.replace(day=16)
    base = realizados.join(confirmaciones, realizados.c.confirmacion_id == confirmaciones.c.id)
    filtro = (confirmaciones.c.trabajador_id == persona['id'], confirmaciones.c.created_at >= inicio, confirmaciones.c.created_at < fin)
    def suma(extra=()):
        return db.execute(select(func.coalesce(func.sum(realizados.c.valor_cop),0)).select_from(base).where(*filtro,*extra)).scalar_one()
    filas = db.execute(select(realizados.c.vidrio, realizados.c.cortado_cm, realizados.c.valor_cop,
        confirmaciones.c.created_at, confirmaciones.c.instalacion_id).select_from(base).where(*filtro).order_by(confirmaciones.c.created_at.desc(),realizados.c.id.desc()).limit(100)).mappings()
    return {'asignado':True,'nombre':persona['nombre'],'mes':ahora.strftime('%Y-%m'),
            'ganado_mes_cop':suma(), 'primera_quincena_cop':suma((confirmaciones.c.created_at < corte,)),
            'segunda_quincena_cop':suma((confirmaciones.c.created_at >= corte,)), 'trabajos':[dict(f) for f in filas]}
