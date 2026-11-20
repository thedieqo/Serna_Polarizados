from calendar import monthrange
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from app.models.instalacion import Instalacion

BOGOTA = ZoneInfo('America/Bogota')


def resumen_ventas(db: Session, anio: int, mes: int, corte: str):
    ultimo = monthrange(anio, mes)[1]
    desde = 16 if corte == 'segunda' else 1
    hasta = 15 if corte == 'primera' else ultimo
    inicio = datetime(anio, mes, desde, tzinfo=BOGOTA)
    fin = datetime(anio + (mes == 12), 1 if mes == 12 else mes + 1, 1, tzinfo=BOGOTA) if hasta == ultimo else datetime(anio, mes, 16, tzinfo=BOGOTA)
    filas = db.query(Instalacion).filter(Instalacion.fecha >= inicio.astimezone(timezone.utc), Instalacion.fecha < fin.astimezone(timezone.utc), Instalacion.estado != 'anulado').order_by(Instalacion.fecha, Instalacion.id).all()
    totales = dict(ventas_cop=0, descuentos_cop=0, pagos_registrados_cop=0, saldo_cop=0, administrador_cop=0, instaladores_cop=0)
    instaladores = {}
    medios = {}
    registros = []
    sin_precio = sin_liquidacion = 0
    for fila in filas:
        desglose = fila.desglose_precios or {}
        cobro = desglose.get('cobro') or {}
        mano_obra = desglose.get('mano_obra')
        if fila.precio_total_cop is None:
            sin_precio += 1
        else:
            totales['ventas_cop'] += fila.precio_total_cop
        if not cobro or mano_obra is None:
            sin_liquidacion += 1
        totales['descuentos_cop'] += cobro.get('descuento_cop') or 0
        totales['pagos_registrados_cop'] += cobro.get('pagado_cop') or 0
        totales['saldo_cop'] += cobro.get('saldo_cop') or 0
        totales['administrador_cop'] += cobro.get('comision_admin_cop') or 0
        for pago in cobro.get('pagos', []):
            medios[pago['medio']] = medios.get(pago['medio'], 0) + pago['monto_cop']
        for item in mano_obra or []:
            persona = instaladores.setdefault(item['instalador_id'], {'nombre': item['instalador'], 'secciones': 0, 'total_cop': 0, 'trabajos': []})
            persona['secciones'] += 1
            persona['total_cop'] += item['valor_cop']
            totales['instaladores_cop'] += item['valor_cop']
            persona['trabajos'].append({'codigo': f'SP{fila.id}', 'vidrio': item['vidrio'], 'panel': item['panel'], 'valor_cop': item['valor_cop']})
        registros.append({'codigo': f'SP{fila.id}', 'fecha': fila.fecha, 'valor_cop': fila.precio_total_cop, 'administrador_cop': cobro.get('comision_admin_cop')})
    return {'desde': inicio.date(), 'hasta': datetime(anio, mes, hasta).date(), 'cantidad': len(filas), 'totales': totales, 'instaladores': list(instaladores.values()), 'medios': medios, 'registros': registros, 'sin_precio': sin_precio, 'sin_liquidacion': sin_liquidacion}
