import DetalleInstalacion from './DetalleInstalacion'
import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { instalacionesService } from '../services/instalaciones'
import type { HistorialResponse, InstalacionDetalle } from '../types/instalacion'

const PAGE_SIZE = 10

function formatearFecha(fecha: string): string {
  try {
    return new Date(fecha).toLocaleString()
  } catch {
    return fecha
  }
}

export default function InstalacionList() {
  const [termino, setTermino] = useState('')
  const [busqueda, setBusqueda] = useState('')
  const [skip, setSkip] = useState(0)
  const [historial, setHistorial] = useState<HistorialResponse | null>(null)
  const [detalle, setDetalle] = useState<InstalacionDetalle | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let activo = true
    setLoading(true)
    instalacionesService
      .getHistorial(busqueda, skip, PAGE_SIZE)
      .then((data) => {
        if (!activo) return
        setHistorial(data)
        setError(null)
      })
      .catch((err: any) => {
        if (!activo) return
        setError(err?.response?.data?.detail || err?.message || 'Error al cargar el historial')
      })
      .finally(() => {
        if (activo) setLoading(false)
      })
    return () => {
      activo = false
    }
  }, [busqueda, skip])

  const buscar = (event: FormEvent) => {
    event.preventDefault()
    setBusqueda(termino.trim())
    setSkip(0)
    setDetalle(null)
  }

  const abrirDetalle = async (id: number) => {
    try {
      setError(null)
      setDetalle(await instalacionesService.getDetalle(id))
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Error al cargar el detalle')
    }
  }

  const total = historial?.total || 0
  const pagina = Math.floor(skip / PAGE_SIZE) + 1
  const totalPaginas = Math.max(1, Math.ceil(total / PAGE_SIZE))

  return (
    <div>
      <form onSubmit={buscar} className="flex flex-col sm:flex-row gap-3 p-4 border-b border-gray-200">
        <input
          value={termino}
          onChange={(event) => setTermino(event.target.value)}
          placeholder="Cédula del propietario o placa del vehículo"
          className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
        />
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-800 rounded-md hover:bg-blue-900"
        >
          Buscar
        </button>
        {busqueda && (
          <button
            type="button"
            onClick={() => {
              setTermino('')
              setBusqueda('')
              setSkip(0)
              setDetalle(null)
            }}
            className="px-4 py-2 text-sm font-medium text-slate-700 border border-slate-300 rounded-md hover:bg-slate-50"
          >
            Limpiar
          </button>
        )}
      </form>

      {error && (
        <div className="p-4">
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        </div>
      )}

      {loading ? (
        <div className="p-4 text-center text-gray-500">Cargando...</div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Propietario</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Documento</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Placa</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>

                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Servicio</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Detalle</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {(historial?.items || []).map((instalacion) => (
                  <tr key={instalacion.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm text-gray-900">SP{instalacion.id}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{instalacion.cliente_nombre}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{instalacion.cliente_documento}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{instalacion.vehiculo_placa}</td>
                    <td className="px-4 py-3 text-sm text-gray-900">{formatearFecha(instalacion.fecha)}</td>

                    <td className="px-4 py-3 text-sm text-gray-900">{instalacion.tipo_servicio}</td>
                    <td className="px-4 py-3 text-sm">
                      <button
                        type="button"
                        onClick={() => abrirDetalle(instalacion.id)}
                        className="text-blue-700 hover:text-blue-900"
                      >
                        Ver detalle
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {(historial?.items.length || 0) === 0 && (
              <p className="p-6 text-center text-sm text-gray-500">
                No hay instalaciones que coincidan con la búsqueda.
              </p>
            )}
          </div>

          <div className="flex items-center justify-between gap-3 px-4 py-3 border-t border-gray-200">
            <span className="text-sm text-gray-600">
              Página {pagina} de {totalPaginas} · {total} registro(s)
            </span>
            <div className="flex gap-2">
              <button
                type="button"
                disabled={skip === 0}
                onClick={() => setSkip(Math.max(0, skip - PAGE_SIZE))}
                className="px-3 py-1.5 text-sm border border-slate-300 rounded-md disabled:opacity-40"
              >
                Anterior
              </button>
              <button
                type="button"
                disabled={skip + PAGE_SIZE >= total}
                onClick={() => setSkip(skip + PAGE_SIZE)}
                className="px-3 py-1.5 text-sm border border-slate-300 rounded-md disabled:opacity-40"
              >
                Siguiente
              </button>
            </div>
          </div>
        </>
      )}

      {detalle && <DetalleInstalacion detalle={detalle} onClose={()=>setDetalle(null)}/>}
    </div>
  )
}
