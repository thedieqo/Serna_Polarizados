import type { DesglosePrecios } from '../types/instalacion'
export const mediosPago: Record<string, string> = { efectivo: 'Efectivo', transferencia: 'Transferencia', tarjeta_credito: 'Tarjeta de crédito', sistecredito: 'Sistecrédito', addi: 'Addi' }
export const cop = (n: number | null | undefined) => n == null ? 'Pendiente de definir' : new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(n)
export default function CobroResumen({ desglose }: { desglose?: DesglosePrecios | null }) {
  if (!desglose) return null
  const cobro = desglose.cobro
  const garantia = desglose.garantia
  return <div className="mt-4 space-y-4 text-sm">
    {cobro && <section className="border-t border-gray-200 pt-4">
      <h4 className="font-semibold text-gray-900 mb-3">Pago y descuento</h4>
      <dl className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div><dt>Subtotal</dt><dd>{cop(cobro.subtotal_cop)}</dd></div>
        <div><dt>Descuento</dt><dd>{cop(cobro.descuento_cop)}{cobro.motivo_descuento && ` · ${cobro.motivo_descuento}`}</dd></div>
        <div><dt>Valor final</dt><dd className="font-semibold">{cop(cobro.total_cop)}</dd></div>
        <div><dt>Total pagado</dt><dd>{cop(cobro.pagado_cop)}</dd></div>
        <div><dt>Por registrar en pagos</dt><dd>{cop(cobro.saldo_cop)}</dd></div>
      </dl>
      <ul className="mt-3 space-y-2">{cobro.pagos.map((p, i) => <li key={i}>{mediosPago[p.medio]}: <strong>{cop(p.monto_cop)}</strong>{p.referencia && ` · Ref. ${p.referencia}`}</li>)}</ul>
      <p className="mt-3">Comisión del administrador (2 % del valor final): {cop(cobro.comision_admin_cop)}</p>
    </section>}
    {!!desglose.mano_obra?.length && <section className="border-t border-gray-200 pt-4">
      <h4 className="font-semibold text-gray-900 mb-3">Liquidación de instaladores</h4>
      <ul className="space-y-2">{desglose.mano_obra.map((m, i) => <li key={i}>{m.instalador} · {m.vidrio}{m.panel && ` (${m.panel})`}: <strong>{cop(m.valor_cop)}</strong></li>)}</ul>
    </section>}
    {garantia && <section className="border-t border-gray-200 pt-4"><h4 className="font-semibold text-gray-900">Garantía de las tecnologías instaladas</h4><p>{garantia.anos} años · Desde {garantia.desde} hasta {garantia.hasta}</p></section>}
  </div>
}
