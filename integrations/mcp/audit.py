"""Comprobaciones financieras deterministas; no modifican datos."""
from decimal import Decimal, ROUND_HALF_UP


def revisar(codigo, total, desglose):
    hallazgos = []
    def agregar(regla, detalle):
        hallazgos.append(dict(codigo=codigo, regla=regla, detalle=detalle))
    cobro = (desglose or {}).get('cobro') or {}
    if total is None or not cobro:
        agregar('DATOS_INCOMPLETOS', 'Falta valor final o información de cobro; no se puede verificar.')
        return hallazgos
    pagos = cobro.get('pagos')
    if not isinstance(pagos, list) or any(not isinstance(p, dict) or not isinstance(p.get('monto_cop'), (int, float)) for p in pagos):
        agregar('PAGOS_INCOMPLETOS', 'Falta un desglose válido de pagos.')
    else:
        suma = sum(Decimal(str(p['monto_cop'])) for p in pagos)
        if suma != Decimal(str(total)):
            agregar('PAGO_NO_COINCIDE', f'Pagos: {suma} COP; valor final: {total} COP.')
        if any(p['monto_cop'] <= 0 for p in pagos):
            agregar('PAGO_INVALIDO', 'Hay montos de pago iguales o menores que cero.')
        if cobro.get('pagado_cop') != suma:
            agregar('TOTAL_PAGADO_INCONSISTENTE', 'El total pagado no coincide con sus medios de pago.')
    esperado = int((Decimal(str(total)) * Decimal('0.02')).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    if cobro.get('comision_admin_cop') != esperado:
        agregar('COMISION_ADMIN', f"Comisión registrada: {cobro.get('comision_admin_cop')}; esperada: {esperado} COP.")
    if cobro.get('saldo_cop') != 0:
        agregar('SALDO_PENDIENTE', 'El registro no tiene saldo cero.')
    return hallazgos
