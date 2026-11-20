import { useEffect, useState } from 'react'
import api from '../services/api'
import { cop, mediosPago } from '../components/CobroResumen'
interface Reporte {
  acumulado_mes?: Reporte; actualizado_en: string;
  desde: string; hasta: string; cantidad: number; sin_precio: number; sin_liquidacion: number;
  totales: { ventas_cop: number; descuentos_cop: number; pagos_registrados_cop: number; saldo_cop: number; administrador_cop: number; instaladores_cop: number };
  medios: Record<string, number>;
  instaladores: Array<{ nombre: string; instalaciones: number; secciones: number; total_cop: number; trabajos: Array<{ codigo: string; vidrio: string; panel: string | null; valor_cop: number }> }>;
  registros: Array<{ codigo: string; fecha: string; valor_cop: number | null; administrador_cop: number | null }>;
}
export default function VentasPage() {
  const hoy = new Intl.DateTimeFormat('sv-SE', { timeZone: 'America/Bogota', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date())
  const [mes, setMes] = useState(hoy.slice(0, 7))
  const [corte, setCorte] = useState('mes')
  const [reporte, setReporte] = useState<Reporte | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [revision, setRevision] = useState(0)
  useEffect(() => {
    let activo = true
    setLoading(true); setError(''); setReporte(null)
    const [anio, numeroMes] = mes.split('-').map(Number)
    api.get<Reporte>('/instalaciones/ventas/resumen', { params: { anio, mes: numeroMes, corte } })
      .then(r => { if (activo) setReporte(r.data) })
      .catch(e => { if (activo) setError(typeof e?.detail === 'string' ? e.detail : 'No se pudo consultar el reporte. Intenta actualizar.') })
      .finally(() => { if (activo) setLoading(false) })
    return () => { activo = false }
  }, [mes, corte, revision])
  return <div className="space-y-6">
    <div><h2 className="text-xl font-semibold text-gray-900">Ventas y liquidación</h2><p className="mt-2 text-sm text-gray-500">Ventas por fecha de instalación, en hora de Colombia. Cortes del 1 al 15 y del 16 al último día del mes.</p></div>
    <div className="flex flex-wrap items-end gap-4 bg-white p-4 rounded-lg">
      <label className="text-sm">Mes<input type="month" min="2000-01" max="2100-12" value={mes} onChange={e => { if (e.target.value) setMes(e.target.value) }} className="block mt-1 border border-gray-300 rounded-md px-3 py-2" /></label>
      <label className="text-sm">Periodo<select value={corte} onChange={e => setCorte(e.target.value)} className="block mt-1 border border-gray-300 rounded-md px-3 py-2"><option value="mes">Mes completo</option><option value="primera">Primer corte · 1 al 15</option><option value="segunda">Segundo corte · 16 al fin de mes</option></select></label>
      <button onClick={() => setRevision(r => r + 1)} className="bg-blue-700 text-white rounded-md px-4 py-2">Actualizar</button>
    </div>
    {loading && <p role="status">Consultando ventas…</p>}
    {error && <p role="alert" className="text-red-800">{error}</p>}
    {reporte?.acumulado_mes && <section className="bg-white rounded-lg p-5 space-y-4">
      <div><h3 className="text-lg font-semibold">Lo ganado en el mes</h3><p className="text-sm text-gray-500 mt-1">Acumulado de {mes}, hasta {new Date(reporte.acumulado_mes.actualizado_en).toLocaleString('es-CO', {timeZone:'America/Bogota'})}. Incluye únicamente instalaciones guardadas con fecha ya transcurrida, sin anuladas.</p></div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div><p className="text-sm">Ventas acumuladas</p><strong className="text-xl">{cop(reporte.acumulado_mes.totales.ventas_cop)}</strong><p className="text-sm">{reporte.acumulado_mes.cantidad} instalaciones</p></div>
        <div><p className="text-sm">Ganado por el administrador · 2 %</p><strong className="text-xl">{cop(reporte.acumulado_mes.totales.administrador_cop)}</strong></div>
        <div><p className="text-sm">Ganado por los instaladores</p><strong className="text-xl">{cop(reporte.acumulado_mes.totales.instaladores_cop)}</strong></div>
      </div>
      <div className="overflow-x-auto"><table className="min-w-full text-sm"><thead><tr><th className="text-left py-2">Instalador</th><th className="text-left py-2">Instalaciones</th><th className="text-left py-2">Secciones</th><th className="text-left py-2">Ganado en el mes</th></tr></thead><tbody>{reporte.acumulado_mes.instaladores.map(p => <tr key={p.nombre} className="border-t border-gray-200"><td className="py-2">{p.nombre}</td><td>{p.instalaciones}</td><td>{p.secciones}</td><td className="font-semibold">{cop(p.total_cop)}</td></tr>)}</tbody></table></div>
      {!reporte.acumulado_mes.instaladores.length && <p className="text-sm">Todavía no hay honorarios registrados en este mes.</p>}
      {(reporte.acumulado_mes.sin_precio > 0 || reporte.acumulado_mes.sin_liquidacion > 0) && <p className="text-sm text-amber-800">Acumulado parcial: {reporte.acumulado_mes.sin_precio} instalaciones sin precio y {reporte.acumulado_mes.sin_liquidacion} sin liquidación completa.</p>}
      <p className="text-xs text-gray-500">Este acumulado siempre abarca el mes seleccionado, aunque consultes una quincena. Muestra lo ganado; no confirma que ya se haya pagado al personal.</p>
    </section>}
    {reporte && <>
      <p className="text-sm">{reporte.desde} a {reporte.hasta} · {reporte.cantidad} instalaciones · {hoy < reporte.desde ? 'Periodo futuro' : hoy <= reporte.hasta ? 'Periodo en curso: liquidación provisional' : 'Periodo terminado: liquidación consultable'}</p>
      {(reporte.sin_precio > 0 || reporte.sin_liquidacion > 0) && <p className="p-3 bg-amber-50 text-amber-800 border border-amber-200 rounded-md">Datos históricos incompletos: {reporte.sin_precio} registros sin precio y {reporte.sin_liquidacion} sin liquidación completa. Los importes desconocidos no se estiman; los totales pueden ser parciales.</p>}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">{[
        ['Ventas después de descuentos', reporte.totales.ventas_cop], ['Descuentos', reporte.totales.descuentos_cop], ['Pagos registrados', reporte.totales.pagos_registrados_cop], ['Comisión administrador · 2 %', reporte.totales.administrador_cop], ['Total instaladores', reporte.totales.instaladores_cop],
      ].map(([label, monto]) => <div key={String(label)} className="bg-white p-5 rounded-lg"><p className="text-sm text-gray-500">{label}</p><p className="text-xl font-semibold mt-2">{cop(Number(monto))}</p></div>)}</div>
      <section className="bg-white p-5 rounded-lg"><h3 className="font-semibold mb-3">Medios de pago</h3>{Object.entries(reporte.medios).map(([medio, valor]) => <p key={medio} className="text-sm py-1">{mediosPago[medio] || medio}: {cop(valor)}</p>)}{!Object.keys(reporte.medios).length && <p className="text-sm text-gray-500">Sin pagos registrados para este periodo.</p>}</section>
      <section className="space-y-4"><h3 className="font-semibold">Pago por instalador</h3>{reporte.instaladores.map(persona => <details key={persona.nombre} className="bg-white p-5 rounded-lg"><summary className="cursor-pointer">{persona.nombre} · {persona.secciones} secciones · <strong>{cop(persona.total_cop)}</strong></summary><ul className="mt-3 space-y-2 text-sm">{persona.trabajos.map((t, i) => <li key={i}>{t.codigo} · {t.vidrio}{t.panel && ` (${t.panel})`} · {cop(t.valor_cop)}</li>)}</ul></details>)}{!reporte.instaladores.length && <p className="text-sm text-gray-500">Sin honorarios registrados para este periodo.</p>}</section>
      <section className="bg-white rounded-lg p-5 overflow-x-auto"><h3 className="font-semibold mb-3">Ventas incluidas en el corte</h3><table className="min-w-full text-sm"><thead><tr><th className="text-left py-2">Código</th><th className="text-left py-2">Fecha y hora</th><th className="text-left py-2">Venta</th><th className="text-left py-2">Administrador</th></tr></thead><tbody>{reporte.registros.map(r => <tr key={r.codigo} className="border-t border-gray-200"><td className="py-2">{r.codigo}</td><td>{new Date(r.fecha).toLocaleString('es-CO', {timeZone:'America/Bogota'})}</td><td>{cop(r.valor_cop)}</td><td>{cop(r.administrador_cop)}</td></tr>)}</tbody></table></section>
      <p className="text-xs text-gray-500">Liquidación calculada sobre los registros del periodo. Consultar el corte no registra una transferencia ni marca honorarios como pagados.</p>
    </>}
  </div>
}
