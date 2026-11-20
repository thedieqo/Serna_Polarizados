import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import type { CatalogosResponse } from '../types/catalogos'
import type {
  DetalleVidrioInput,
  Referido,
  RegistroInstalacionCreate,
  RegistroInstalacionPreview,
  RegistroInstalacionResult,
} from '../types/instalacion'
import CobroResumen, { mediosPago } from './CobroResumen'
import { instalacionesService } from '../services/instalaciones'
import api from '../services/api'
import { cobroEnVivo } from '../lib/cobroEnVivo'
import { motivoBloqueoGuardado } from '../lib/estadoGuardado'

function emptyDetalle(): DetalleVidrioInput {
  return {
    vidrio_id: '',
    panel: null,
    tecnologia_id: '',
    opacidad_id: '',
    instalador_id: '',
  }
}

function getErrorMessage(err: any): string {
  const detail = err?.response?.data?.detail ?? err?.detail
  if (typeof detail === 'string') return detail
  if (typeof detail?.message === 'string') return detail.message
  if (Array.isArray(detail)) {
    if (detail.some((item: any) => item.type === 'extra_forbidden')) return 'El servidor no reconoce los campos nuevos de este formulario. Actualiza el servidor y vuelve a generar el resumen. Tus datos siguen en pantalla.'
    return detail.map((item: any) => item.msg || JSON.stringify(item)).join('; ')
  }
  return err?.message || 'Error inesperado'
}

function formatearCOP(valor: number | null): string {
  if (valor === null) return 'Precio pendiente de definir'
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(valor)
}

export default function InstalacionForm({ onCancel }: { onCancel?: () => void }) {
  const [catalogos, setCatalogos] = useState<CatalogosResponse | null>(null)
  const [cliente, setCliente] = useState({
    documento: '',
    nombre: '',
    telefono: '',
    email: '',
  })
  const [vehiculo, setVehiculo] = useState({
    placa: '',
    marca: '',
    descripcion: '',
  })
  const [pagos, setPagos] = useState([{ medio: 'efectivo', monto: '' }])
  const [tipoDescuento, setTipoDescuento] = useState<'ninguno' | 'referido' | 'agenda' | 'especial'>('ninguno')
  const [placaReferido, setPlacaReferido] = useState('')
  const [referido, setReferido] = useState<Referido | null>(null)
  const [consultandoReferido, setConsultandoReferido] = useState(false)
  const [motivoDescuento, setMotivoDescuento] = useState('')
  const [tipoFactura, setTipoFactura] = useState('normal')
  const [fecha, setFecha] = useState('')
  const [retiroMaterial, setRetiroMaterial] = useState(false)
  const [observaciones, setObservaciones] = useState('')
  const [detalles, setDetalles] = useState<DetalleVidrioInput[]>([emptyDetalle()])
  const [loadingCatalogos, setLoadingCatalogos] = useState(true)
  const [loadingPreview, setLoadingPreview] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [preview, setPreview] = useState<RegistroInstalacionPreview | null>(null)
  const [guardando, setGuardando] = useState(false)
  const [resultado, setResultado] = useState<RegistroInstalacionResult | null>(null)
  const guardandoRef = useRef(false)

  const cobroActual = cobroEnVivo(detalles, catalogos?.tarifas, tipoDescuento, pagos.map(p => Number(p.monto || 0)))
  useEffect(() => {
    let activo = true
    setReferido(null)
    if (tipoDescuento !== 'referido' || !placaReferido.trim()) { setConsultandoReferido(false); return }
    setConsultandoReferido(true)
    const timer = setTimeout(() => {
      api.get<Referido>(`/instalaciones/referidos/${encodeURIComponent(placaReferido.trim())}`)
        .then(r => { if (activo) setReferido(r.data) })
        .catch(() => { if (activo) setReferido({disponible:false, placa:placaReferido, motivo:'No se pudo verificar el referido. Revisa la conexión.'}) })
        .finally(() => { if (activo) setConsultandoReferido(false) })
    }, 400)
    return () => { activo = false; clearTimeout(timer) }
  }, [tipoDescuento, placaReferido])

  useEffect(() => {
    let activo = true

    const cargar = async () => {
      const [catalogosResult] = await Promise.allSettled([
        instalacionesService.getCatalogos(),
      ])

      if (!activo) return

      if (catalogosResult.status === 'fulfilled') {
        const data = catalogosResult.value
        setCatalogos(data)
        setDetalles([
          {
            vidrio_id: data.vidrios[0]?.id || '',
            panel: null,
            tecnologia_id: data.tecnologias[0]?.id || '',
            opacidad_id: data.opacidades[0]?.id || '',
            instalador_id: data.instaladores[0]?.id || '',
          },
        ])
      } else {
        setError(getErrorMessage(catalogosResult.reason))
      }

      setLoadingCatalogos(false)
    }

    cargar()
    return () => {
      activo = false
    }
  }, [])

  const catalogosListos = Boolean(
    catalogos &&
      catalogos.vidrios.length &&
      catalogos.tecnologias.length &&
      catalogos.opacidades.length &&
      catalogos.instaladores.length &&
      catalogos.tipos_factura.length,
  )
  const campoDeshabilitado = !catalogosListos || loadingPreview || guardando

  const panelesPara = (vidrioId: string): string[] =>
    catalogos?.vidrios.find((vidrio) => vidrio.id === vidrioId)?.paneles || []

  const limpiarResumen = () => {
    setPreview(null)
    setResultado(null)
  }

  const updateDetalle = (indice: number, patch: Partial<DetalleVidrioInput>) => {
    setDetalles((prev) =>
      prev.map((detalle, i) => (i === indice ? { ...detalle, ...patch } : detalle)),
    )
    limpiarResumen()
  }

  const agregarDetalle = () => {
    setDetalles((prev) => [
      ...prev,
      {
        vidrio_id: catalogos?.vidrios[0]?.id || '',
        panel: null,
        tecnologia_id: catalogos?.tecnologias[0]?.id || '',
        opacidad_id: catalogos?.opacidades[0]?.id || '',
        instalador_id: catalogos?.instaladores[0]?.id || '',
      },
    ])
    limpiarResumen()
  }

  const buildPayload = (): RegistroInstalacionCreate => ({
    cliente: {
      documento: cliente.documento,
      nombre: cliente.nombre,
      telefono: cliente.telefono || null,
      email: cliente.email || null,
    },
    vehiculo: {
      placa: vehiculo.placa,
      marca: vehiculo.marca,
      descripcion: vehiculo.descripcion || null,
    },
    tipo_factura: tipoFactura,
    tipo_descuento: tipoDescuento,
    referido_placa: tipoDescuento === 'referido' ? placaReferido : null,
    motivo_descuento: tipoDescuento === 'especial' ? motivoDescuento : null,
    pagos: pagos.filter(p => Number(p.monto) > 0).map(p => ({ medio: p.medio, monto_cop: Number(p.monto) })),
    fecha: fecha ? new Date(fecha).toISOString() : null,
    retiro_material_anterior: retiroMaterial,
    observaciones: observaciones || null,
    estado: 'programado',
    detalles: detalles.flatMap<DetalleVidrioInput>((detalle) => detalle.vidrio_id === 'cuatro_laterales'
      ? ['laterales_delanteros', 'laterales_traseros'].map(vidrio => ({ ...detalle, vidrio_id: vidrio, panel: null, grupo: 'cuatro_laterales' as const }))
      : [{ ...detalle, panel: detalle.panel || null, grupo: null }]),
  })

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    if (guardandoRef.current || loadingPreview) return
    if (resultado) {
      setError('Esta instalación ya está guardada. Modifica el formulario para registrar otra.')
      return
    }
    setError(null)
    limpiarResumen()

    if (!catalogosListos) {
      setError('Los catálogos de la instalación no están disponibles.')
      return
    }

    const payload = buildPayload()

    setLoadingPreview(true)
    try {
      setPreview(await instalacionesService.preview(payload))
    } catch (err: any) {
      setError(getErrorMessage(err))
    } finally {
      setLoadingPreview(false)
    }
  }

  const handleGuardar = async () => {
    if (
      guardandoRef.current ||
      resultado ||
      Boolean(razonesGuardado)
    ) {
      return
    }
    guardandoRef.current = true
    setError(null)
    setGuardando(true)
    try {
      setResultado(await instalacionesService.registrar(buildPayload()))
    } catch (err: any) {
      setError(getErrorMessage(err))
    } finally {
      guardandoRef.current = false
      setGuardando(false)
    }
  }

  const razonesGuardado = motivoBloqueoGuardado(preview, loadingPreview, guardando, Boolean(resultado))

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Nueva instalación</h3>
          <p className="text-sm text-gray-500 mt-1">Polarizado - resumen y guardado cuando esté habilitado.</p>
        </div>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="self-start text-sm text-blue-700 hover:text-blue-900"
          >
            Cerrar
          </button>
        )}
      </div>

      {loadingCatalogos && (
        <div className="mt-4 p-3 bg-slate-50 border border-slate-200 rounded-md">
          <p className="text-sm text-slate-600">Cargando catálogos...</p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} onChange={limpiarResumen} className="mt-6 space-y-6">
        <fieldset disabled={loadingPreview || guardando} className="space-y-6">
        <section>
          <h4 className="text-sm font-semibold text-gray-900 mb-3">Propietario</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Documento</label>
              <input
                required
                value={cliente.documento}
                onChange={(e) => setCliente({ ...cliente, documento: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Nombre</label>
              <input
                required
                value={cliente.nombre}
                onChange={(e) => setCliente({ ...cliente, nombre: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Teléfono</label>
              <input
                value={cliente.telefono}
                onChange={(e) => setCliente({ ...cliente, telefono: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Correo electrónico</label>
              <input
                type="email"
                value={cliente.email}
                onChange={(e) => setCliente({ ...cliente, email: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>

          </div>
        </section>

        <section className="border-t border-gray-200 pt-6">
          <h4 className="text-sm font-semibold text-gray-900 mb-3">Vehículo</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Placa</label>
              <input
                required
                value={vehiculo.placa}
                onChange={(e) => setVehiculo({ ...vehiculo, placa: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Marca</label>
              <input
                required
                value={vehiculo.marca}
                onChange={(e) => setVehiculo({ ...vehiculo, marca: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Descripción</label>
              <input
                value={vehiculo.descripcion}
                onChange={(e) => setVehiculo({ ...vehiculo, descripcion: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
          </div>
        </section>

        <section className="border-t border-gray-200 pt-6">
          <div className="flex items-center justify-between gap-3 mb-3">
            <h4 className="text-sm font-semibold text-gray-900">Vidrios, tecnologías e instaladores</h4>
            <button
              type="button"
              onClick={agregarDetalle}
              disabled={campoDeshabilitado}
              className="text-sm text-blue-700 hover:text-blue-900 disabled:text-gray-400"
            >
              + Agregar vidrio
            </button>
          </div>
          <p className="text-xs text-gray-500 mb-3">
            Cada vidrio admite una tecnología; una instalación puede combinar tecnologías distintas.
            El techo solar doble requiere panel delantero y trasero.
          </p>

          <div className="space-y-3">
            {detalles.map((detalle, indice) => {
              const paneles = panelesPara(detalle.vidrio_id)
              return (
                <div key={indice} className="grid grid-cols-1 md:grid-cols-5 gap-2">
                  <select
                    required
                    disabled={campoDeshabilitado}
                    value={detalle.vidrio_id}
                    onChange={(e) => updateDetalle(indice, { vidrio_id: e.target.value, panel: null, pelicula_seguridad: false })}
                    className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border disabled:bg-gray-100"
                  >
                    <option value="">Vidrio</option>
                    <option value="cuatro_laterales">Cuatro laterales</option>
                    {catalogos?.vidrios.map((vidrio) => (
                      <option key={vidrio.id} value={vidrio.id}>{vidrio.label}</option>
                    ))}
                  </select>

                  {paneles.length > 0 ? (
                    <select
                      required
                      disabled={campoDeshabilitado}
                      value={detalle.panel || ''}
                      onChange={(e) => updateDetalle(indice, { panel: e.target.value || null })}
                      className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border disabled:bg-gray-100"
                    >
                      <option value="">Panel</option>
                      {paneles.map((panel) => (
                        <option key={panel} value={panel}>{panel}</option>
                      ))}
                    </select>
                  ) : (
                    ['cuatro_laterales', 'laterales_delanteros', 'laterales_traseros'].includes(detalle.vidrio_id) ?
                    <select aria-label="Película de seguridad" value={detalle.pelicula_seguridad ? 'si' : 'no'} onChange={e => updateDetalle(indice, { pelicula_seguridad: e.target.value === 'si' })} className="rounded-md border border-gray-300 px-3 py-2 text-sm">
                      <option value="no">Sin película de seguridad</option>
                      <option value="si">Con película (+{detalle.vidrio_id === 'cuatro_laterales' ? '$200.000' : '$100.000'})</option>
                    </select> : <div className="hidden md:block" />
                  )}

                  <select
                    required
                    disabled={campoDeshabilitado}
                    value={detalle.tecnologia_id}
                    onChange={(e) => updateDetalle(indice, { tecnologia_id: e.target.value })}
                    className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border disabled:bg-gray-100"
                  >
                    <option value="">Tecnología</option>
                    {catalogos?.tecnologias.map((tecnologia) => (
                      <option key={tecnologia.id} value={tecnologia.id}>{tecnologia.label}</option>
                    ))}
                  </select>

                  <select
                    required
                    disabled={campoDeshabilitado}
                    value={detalle.opacidad_id}
                    onChange={(e) => updateDetalle(indice, { opacidad_id: e.target.value })}
                    className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border disabled:bg-gray-100"
                  >
                    <option value="">Opacidad</option>
                    {catalogos?.opacidades.map((opacidad) => (
                      <option key={opacidad.id} value={opacidad.id}>{opacidad.label}</option>
                    ))}
                  </select>

                  <div className="flex gap-2">
                    <select
                      required
                      disabled={campoDeshabilitado}
                      value={detalle.instalador_id}
                      onChange={(e) => updateDetalle(indice, { instalador_id: e.target.value })}
                      className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border disabled:bg-gray-100"
                    >
                      <option value="">Instalador</option>
                      {catalogos?.instaladores.map((instalador) => (
                        <option key={instalador.id} value={instalador.id}>{instalador.label}</option>
                      ))}
                    </select>
                    <button
                      type="button"
                      disabled={detalles.length === 1 || campoDeshabilitado}
                      onClick={() => {
                        setDetalles((prev) => prev.filter((_, i) => i !== indice))
                        limpiarResumen()
                      }}
                      className="px-2 text-red-600 disabled:text-gray-300"
                    >
                      -
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        <section className="border-t border-gray-200 pt-6">
          <h4 className="text-sm font-semibold text-gray-900 mb-3">Datos adicionales</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Fecha</label>
              <input
                type="datetime-local"
                value={fecha}
                onChange={(e) => {
                  setFecha(e.target.value)
                  limpiarResumen()
                }}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
            </div>
            <div className="flex items-end">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={retiroMaterial}
                  onChange={(e) => {
                    setRetiroMaterial(e.target.checked)
                    limpiarResumen()
                  }}
                  className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <span className="text-sm font-medium text-gray-700">Retiro de material anterior</span>
              </label>
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700">Observaciones</label>
            <textarea
              rows={3}
              value={observaciones}
              onChange={(e) => {
                setObservaciones(e.target.value)
                limpiarResumen()
              }}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            />
          </div>
        </section>

        <section className="border-t border-gray-200 pt-6 space-y-4">
          <h4 className="text-sm font-semibold text-gray-900">Pago y facturación</h4>
          <p className="text-sm text-gray-500">Combina medios de pago. La suma debe cubrir el valor final para guardar. Los importes se registran en pesos colombianos.</p>
          <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={tipoDescuento !== 'ninguno'} onChange={e => setTipoDescuento(e.target.checked ? 'referido' : 'ninguno')} />Aplicar descuento</label>
          {tipoDescuento !== 'ninguno' && <div className="space-y-3">
            <label className="block text-sm">Tipo de descuento<select value={tipoDescuento} onChange={e => setTipoDescuento(e.target.value as typeof tipoDescuento)} className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"><option value="referido">Referido · 5 %</option><option value="agenda">Agenda · 10 %</option><option value="especial">Fecha especial · 15 %</option></select></label>
            <p className="text-xs text-gray-500">Se aplica un solo descuento sobre el subtotal.</p>
            {tipoDescuento === 'referido' && <div>
              <label className="text-sm">Placa de quien refiere<input required maxLength={20} value={placaReferido} onChange={e => setPlacaReferido(e.target.value.toUpperCase())} className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2" /></label>
              <p role="status" className="text-sm mt-2">{consultandoReferido ? 'Verificando placa…' : referido ? `${referido.nombre ? referido.nombre + ' · ' : ''}${referido.motivo}` : 'Ingresa una placa con una instalación previa de polarizado.'}</p>
              <p className="text-xs text-gray-500 mt-1">Un referido por cliente. Se consume al guardar la instalación, no al consultar.</p>
            </div>}
            {tipoDescuento === 'especial' && <label className="block text-sm">Ocasión de la promoción<input required maxLength={250} value={motivoDescuento} onChange={e => setMotivoDescuento(e.target.value)} placeholder="Ejemplo: Navidad" className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2" /></label>}
          </div>}
          <div className="rounded-lg border border-gray-300 p-4 grid grid-cols-1 sm:grid-cols-3 gap-3" aria-live="polite">
            <div><p className="text-sm">Total de la instalación</p><strong>{formatearCOP(cobroActual.completo ? cobroActual.subtotal : null)}</strong></div>
            <div><p className="text-sm">Descuento</p><strong>{formatearCOP(cobroActual.completo ? cobroActual.descuento : null)}</strong></div>
            <div><p className="text-sm">Total a pagar</p><strong>{formatearCOP(cobroActual.completo ? cobroActual.total : null)}</strong></div>
            <div><p className="text-sm">Pagos registrados</p><strong>{formatearCOP(cobroActual.pagado)}</strong></div>
            <div><p className="text-sm">{cobroActual.saldo < 0 ? 'Exceso en pagos' : 'Falta por pagar'}</p><strong>{formatearCOP(cobroActual.completo ? Math.abs(cobroActual.saldo) : null)}</strong></div>
          </div>
          {tipoDescuento === 'referido' && !referido?.disponible && <p className="text-xs text-gray-500">El total con 5 % está sujeto a validar el referido al guardar.</p>}
          {pagos.map((p, i) => <div key={i} className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <label className="text-sm">Medio de pago<select value={p.medio} onChange={e => setPagos(prev => prev.map((v, n) => n === i ? { ...v, medio: e.target.value } : v))} className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2">{Object.entries(mediosPago).map(([id, label]) => <option key={id} value={id}>{label}</option>)}</select></label>
            <label className="text-sm">Monto en COP<input type="number" min="0" max="1000000000" step="1" value={p.monto} onChange={e => setPagos(prev => prev.map((v, n) => n === i ? { ...v, monto: e.target.value } : v))} className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2" /></label>
            <button type="button" disabled={pagos.length === 1} onClick={() => { setPagos(prev => prev.filter((_, n) => n !== i)); limpiarResumen() }} className="text-sm text-red-800 disabled:opacity-50">Quitar pago</button>
            <p className="text-sm sm:col-span-3">Después de este pago: {formatearCOP(cobroActual.completo ? Math.max(0, cobroActual.total - pagos.slice(0, i + 1).reduce((sum, pago) => sum + Number(pago.monto || 0), 0)) : null)} por cubrir.</p>
          </div>)}
          <button type="button" disabled={pagos.length >= 20} onClick={() => { setPagos(prev => [...prev, { medio: 'transferencia', monto: '' }]); limpiarResumen() }} className="text-sm text-blue-700">+ Agregar medio de pago</button>
            <div>
              <label className="block text-sm font-medium text-gray-700">Tipo de factura</label>
              <select
                required
                disabled={campoDeshabilitado}
                value={tipoFactura}
                onChange={(e) => setTipoFactura(e.target.value)}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border disabled:bg-gray-100"
              >
                <option value="">Seleccionar tipo</option>
                {catalogos?.tipos_factura.map((tipo) => (
                  <option key={tipo.id} value={tipo.id}>{tipo.label}</option>
                ))}
              </select>
            </div>
          <p className="text-xs text-gray-500">Se registra el tipo de factura solicitado. La emisión electrónica se realiza por fuera de esta aplicación.</p>
          <p className="text-sm text-slate-600">Garantía de las tecnologías instaladas: 15 años desde la fecha de instalación.</p>
        </section>

        <div className="flex flex-col sm:flex-row gap-3 border-t border-gray-200 pt-6">
          <button
            type="submit"
            disabled={campoDeshabilitado || Boolean(resultado)}
            className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600 disabled:opacity-50"
          >
            {loadingPreview ? 'Generando resumen...' : 'Generar resumen'}
          </button>
          <button
            type="button"
            onClick={handleGuardar}
            disabled={Boolean(razonesGuardado)}
            title={razonesGuardado || 'Guardar instalación'}
            aria-describedby="estado-guardado"
            className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {guardando ? 'Guardando...' : resultado ? 'Guardado' : 'Guardar instalación'}
          </button>
        </div>
        <p id="estado-guardado" role="status" className="text-sm text-slate-600">
          {razonesGuardado || 'Resumen validado. Puedes guardar la instalación.'}
        </p>
        {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
        </fieldset>
      </form>

      {preview && (
        <div className="mt-6 border-t border-gray-200 pt-6">
          <h4 className="text-base font-semibold text-gray-900">Resumen de la instalación</h4>
          <p className="text-sm text-gray-600 mt-1">Vista previa generada; no se guardó información.</p>

          <dl className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div>
              <dt className="font-medium text-gray-700">Cliente</dt>
              <dd className="text-gray-900">{preview.cliente.nombre} - {preview.cliente.documento}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">Vehículo</dt>
              <dd className="text-gray-900">{preview.vehiculo.placa} - {preview.vehiculo.marca}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">Tipo de factura</dt>
              <dd className="text-gray-900">{preview.tipo_factura}</dd>
            </div>
            <div>
              <dt className="font-medium text-gray-700">Vidrios</dt>
              <dd className="text-gray-900">{preview.cantidad_vidrios}</dd>
            </div>
          </dl>

          <div className="mt-4 overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Vidrio</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Panel</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Tecnología</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Opacidad</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Instalador</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {preview.detalles.map((detalle, indice) => (
                  <tr key={indice}>
                    <td className="px-3 py-2">{detalle.vidrio}</td>
                    <td className="px-3 py-2">{detalle.panel || '-'}</td>
                    <td className="px-3 py-2">{detalle.tecnologia}</td>
                    <td className="px-3 py-2">{detalle.opacidad}</td>
                    <td className="px-3 py-2">{detalle.instalador}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="mt-4">
            <h4 className="text-sm font-semibold text-gray-900">Desglose de precios</h4>
            <table className="mt-2 min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Concepto</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Detalle</th>
                  <th className="px-3 py-2 text-left font-medium text-gray-600">Importe</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {preview.desglose.conceptos.map((concepto, indice) => (
                  <tr key={indice}>
                    <td className="px-3 py-2">{concepto.concepto}</td>
                    <td className="px-3 py-2">{concepto.detalle}</td>
                    <td className="px-3 py-2">{formatearCOP(concepto.importe_cop)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="mt-2 text-sm font-semibold text-gray-900">
              {preview.desglose.total_cop === null
                ? preview.desglose.etiqueta_total
                : `${preview.desglose.etiqueta_total}: ${formatearCOP(preview.desglose.total_cop)}`}
            </p>
            <p className="mt-1 text-xs text-gray-500">
              Tarifas en COP, calculadas por el backend. Los casos pendientes no generan un total definitivo.
            </p>
          </div>

          <CobroResumen desglose={preview.desglose} />
          <div className="mt-4 p-3 bg-slate-50 border border-slate-200 rounded-md text-sm text-slate-700">
            <p>Tecnologías: {preview.tecnologias_utilizadas.join(', ')}</p>
            <p>
              Guardado:{' '}
              {razonesGuardado || 'habilitado'}
            </p>
          </div>
        </div>
      )}

      {resultado && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md text-sm text-green-900">
          <p className="font-semibold">Instalación guardada correctamente.</p>
          <p>
            Código de instalación: SP{resultado.instalacion_id} · Vidrios guardados:{' '}
            {resultado.detalles_guardados}
          </p>
          <p>
            Cliente {resultado.cliente_reutilizado ? 'reutilizado' : 'creado'} · Vehículo{' '}
            {resultado.vehiculo_reutilizado ? 'reutilizado' : 'creado'}.
          </p>
        </div>
      )}
    </div>
  )
}
