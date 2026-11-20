import { useEffect, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import type { CatalogosResponse, SchemaStatusResponse } from '../types/catalogos'
import type {
  DetalleVidrioInput,
  RegistroInstalacionCreate,
  RegistroInstalacionPreview,
  RegistroInstalacionResult,
} from '../types/instalacion'
import { instalacionesService } from '../services/instalaciones'

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
  const detail = err?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
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
  const [schemaStatus, setSchemaStatus] = useState<SchemaStatusResponse | null>(null)
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

  useEffect(() => {
    let activo = true

    const cargar = async () => {
      const [catalogosResult, schemaResult] = await Promise.allSettled([
        instalacionesService.getCatalogos(),
        instalacionesService.getSchemaStatus(),
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

      if (schemaResult.status === 'fulfilled') {
        setSchemaStatus(schemaResult.value)
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
  const campoDeshabilitado = !catalogosListos || loadingPreview

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
    fecha: fecha ? new Date(fecha).toISOString() : null,
    retiro_material_anterior: retiroMaterial,
    observaciones: observaciones || null,
    estado: 'programado',
    detalles: detalles.map((detalle) => ({
      ...detalle,
      panel: detalle.panel || null,
    })),
  })

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
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
      !preview?.guardado_habilitado ||
      !schemaStatus?.save_enabled
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

  const razonesGuardado = schemaStatus?.reasons.join(', ') || 'validación pendiente'

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

      {schemaStatus && !schemaStatus.save_enabled && (
        <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-md">
          <p className="text-sm text-amber-800">Guardado deshabilitado: {razonesGuardado}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-6 space-y-6">
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
                    onChange={(e) => updateDetalle(indice, { vidrio_id: e.target.value, panel: null })}
                    className="rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border disabled:bg-gray-100"
                  >
                    <option value="">Vidrio</option>
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
                    <div className="hidden md:block" />
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

        <div className="flex flex-col sm:flex-row gap-3 border-t border-gray-200 pt-6">
          <button
            type="submit"
            disabled={campoDeshabilitado}
            className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600 disabled:opacity-50"
          >
            {loadingPreview ? 'Generando resumen...' : 'Generar resumen'}
          </button>
          <button
            type="button"
            onClick={handleGuardar}
            disabled={
              !preview?.guardado_habilitado ||
              !schemaStatus?.save_enabled ||
              guardando ||
              Boolean(resultado)
            }
            title={razonesGuardado}
            className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {guardando ? 'Guardando...' : resultado ? 'Guardado' : 'Guardar instalación'}
          </button>
        </div>
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

          <div className="mt-4 p-3 bg-slate-50 border border-slate-200 rounded-md text-sm text-slate-700">
            <p>Tecnologías: {preview.tecnologias_utilizadas.join(', ')}</p>
            <p>
              Guardado:{' '}
              {preview.guardado_habilitado
                ? 'habilitado'
                : `deshabilitado (${preview.motivos.join(', ')})`}
            </p>
          </div>
        </div>
      )}

      {resultado && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md text-sm text-green-900">
          <p className="font-semibold">Instalación guardada correctamente.</p>
          <p>
            ID de instalación: {resultado.instalacion_id} · Vidrios guardados:{' '}
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
