"""Metros lineales almacenados como centímetros enteros, sin errores de coma flotante."""
from collections import defaultdict
from sqlalchemy import select, insert, update
from app.db.registro_tables import inventario, inventario_movimientos
from app.core.catalogs import TECNOLOGIAS_POLARIZADO, OPACIDADES_POLARIZADO, label_for

CONSUMO_CM = {'parabrisas':150,'laterales_delanteros':80,'laterales_traseros':80,'luneta':110,'sunroof_simple':110,'sunroof_doble':75}

class InventarioError(ValueError):
    pass


def inicializar(db):
    """Solo para preparación explícita: nunca reponer stock durante una consulta."""
    existentes=set(db.execute(select(inventario.c.sku)).scalars())
    for tecnologia in TECNOLOGIAS_POLARIZADO:
        for opacidad in OPACIDADES_POLARIZADO:
            for material in ['polarizado','pelicula_seguridad']:
                sku=f"{tecnologia['id']}:{opacidad['id']}:{material}"
                if sku in existentes: continue
                db.execute(insert(inventario).values(sku=sku,tecnologia_id=tecnologia['id'],opacidad_id=opacidad['id'],material=material,disponible_cm=20000))
                db.execute(insert(inventario_movimientos).values(sku=sku,cantidad_cm=20000,motivo='Existencia inicial · 1 rollo de 200 m'))


def consumos(detalles):
    resultado=defaultdict(int)
    for d in detalles:
        material='pelicula_seguridad' if d.pelicula_seguridad else 'polarizado'
        sku=f'{d.tecnologia_id}:{d.opacidad_id}:{material}'
        resultado[sku]+=CONSUMO_CM[d.vidrio_id]
    return dict(resultado)


def descontar(db, instalacion_id, detalles):
    plan=consumos(detalles)
    # Orden estable evita interbloqueos. El UPDATE condicional impide saldos negativos
    # incluso ante solicitudes concurrentes. Todo comparte la transacción de instalación.
    for sku, cm in sorted(plan.items()):
        resultado=db.execute(update(inventario).where(inventario.c.sku==sku,inventario.c.disponible_cm>=cm).values(disponible_cm=inventario.c.disponible_cm-cm))
        if resultado.rowcount!=1:
            tecnologia,opacidad,material=sku.split(':')
            raise InventarioError(f"Material insuficiente: {label_for('tecnologias',tecnologia)}, {opacidad} %, {'película de seguridad' if material=='pelicula_seguridad' else 'polarizado'}. Se necesitan {cm/100:.2f} m.")
        db.execute(insert(inventario_movimientos).values(sku=sku,instalacion_id=instalacion_id,cantidad_cm=-cm,motivo='Consumo de instalación'))


def consultar(db):
    items=[]
    for r in db.execute(select(inventario).order_by(inventario.c.tecnologia_id,inventario.c.opacidad_id,inventario.c.material)).mappings():
        items.append(dict(r)|{'tecnologia':label_for('tecnologias',r['tecnologia_id']), 'disponible_m':r['disponible_cm']/100})
    movimientos=[dict(r) for r in db.execute(select(inventario_movimientos).order_by(inventario_movimientos.c.id.desc()).limit(100)).mappings()]
    return {'items':items,'movimientos':movimientos,'unidad':'metros lineales','rollo_m':200}
