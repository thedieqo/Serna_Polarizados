"""Importes enteros en COP y condiciones guardadas por venta."""
from calendar import monthrange
from datetime import datetime
from zoneinfo import ZoneInfo

BOGOTA = ZoneInfo('America/Bogota')
MEDIOS_PAGO = {'efectivo', 'transferencia', 'tarjeta_credito', 'sistecredito', 'addi'}


def calcular_cobro(subtotal, descuento, motivo, pagos):
    if descuento and not (motivo or '').strip():
        raise ValueError('Indica el motivo del descuento')
    pagado = sum(p.monto_cop for p in pagos)
    if subtotal is None:
        if descuento or pagado:
            raise ValueError('Define el precio de todos los vidrios antes de registrar descuentos o pagos')
        total = saldo = comision = None
    else:
        if descuento > subtotal:
            raise ValueError('El descuento no puede superar el valor de la instalación')
        total = subtotal - descuento
        if pagado > total:
            raise ValueError('La suma de pagos supera el valor final de la instalación')
        saldo = total - pagado
        comision = (total * 2 + 50) // 100  # Redondeo al peso más cercano.
    return {
        'subtotal_cop': subtotal, 'descuento_cop': descuento,
        'motivo_descuento': motivo if descuento else None,
        'total_cop': total, 'pagado_cop': pagado, 'saldo_cop': saldo,
        'comision_admin_cop': comision, 'porcentaje_admin': 2,
        'pagos': [p.model_dump() for p in pagos],
    }


def garantia_instalacion(fecha, detalles):
    inicio = fecha or datetime.now(BOGOTA)
    if inicio.tzinfo is None:
        inicio = inicio.replace(tzinfo=BOGOTA)
    inicio = inicio.astimezone(BOGOTA).date()
    anio = inicio.year + 15
    fin = inicio.replace(year=anio, day=min(inicio.day, monthrange(anio, inicio.month)[1]))
    return {'anos': 15, 'desde': inicio.isoformat(), 'hasta': fin.isoformat(),
            'tecnologias': sorted({d.tecnologia_id for d in detalles})}
