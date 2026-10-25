import { useState, useEffect } from 'react'
import type { InstalacionCreate } from '../types/instalacion'
import { instalacionesService } from '../services/instalaciones'
import { vehiculosService } from '../services/vehiculos'
import type { VehiculoRead } from '../types/vehiculo'

type ZonaItem = {
  zona: string
  opacidad_aplicada: string
}

type AsignacionItem = {
  zona: string
  instalador: string
}

export default function InstalacionForm({ onInstalacionCreada }: { onInstalacionCreada?: () => void }) {
  const [vehiculos, setVehiculos] = useState<VehiculoRead[]>([])
  const [formData, setFormData] = useState<Partial<InstalacionCreate>>({
    vehiculo_id: 0,
    tipo_servicio: 'polarizado',
    estado: 'programado',
    retiro_material_anterior: false,
    observaciones: '',
    opacidad: '',
    fecha: '',
  })
  const [zonas, setZonas] = useState<ZonaItem[]>([{ zona: 'parabrisas', opacidad_aplicada: '' }])
  const [asignaciones, setAsignaciones] = useState<AsignacionItem[]>([{ zona: 'parabrisas', instalador: '' }])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    const fetchVehiculos = async () => {
      try {
        const data = await vehiculosService.getAll()
        setVehiculos(data)
      } catch (err) {
        // ignore
      }
    }
    fetchVehiculos()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      if (!formData.vehiculo_id) throw new Error('Seleccione un vehículo')
      if (zonas.length === 0) throw new Error('Debe agregar al menos una zona')
      if (asignaciones.length === 0) throw new Error('Debe agregar al menos una asignación')

      const payload: InstalacionCreate = {
        vehiculo_id: Number(formData.vehiculo_id),
        tipo_servicio: formData.tipo_servicio as any,
        estado: formData.estado as any,
        zonas: zonas as any,
        asignaciones_instaladores: asignaciones as any,
        retiro_material_anterior: formData.retiro_material_anterior || false,
        observaciones: formData.observaciones || null,
        opacidad: formData.opacidad || null,
        fecha: formData.fecha ? new Date(formData.fecha).toISOString() : undefined,
      }

      await instalacionesService.create(payload)
      setSuccess(true)
      setFormData({ vehiculo_id: 0, tipo_servicio: 'polarizado', estado: 'programado', retiro_material_anterior: false, observaciones: '', opacidad: '', fecha: '' })
      setZonas([{ zona: 'parabrisas', opacidad_aplicada: '' }])
      setAsignaciones([{ zona: 'parabrisas', instalador: '' }])
      if (onInstalacionCreada) onInstalacionCreada()
      setTimeout(() => setSuccess(false), 3000)
    } catch (err: any) {
      setError(err.detail || err.message || 'Error al crear instalación')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Registrar Instalación</h2>

      {success && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md">
          <p className="text-sm text-green-800">Instalación creada exitosamente</p>
        </div>
      )}

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Vehículo</label>
          <select
            required
            value={formData.vehiculo_id || 0}
            onChange={(e) => setFormData({ ...formData, vehiculo_id: parseInt(e.target.value) })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
          >
            <option value={0}>Seleccionar vehículo</option>
            {vehiculos.map((v) => (
              <option key={v.id} value={v.id}>{v.placa} - Cliente {v.cliente_id}</option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Tipo de servicio</label>
            <select
              required
              value={formData.tipo_servicio}
              onChange={(e) => setFormData({ ...formData, tipo_servicio: e.target.value as any })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            >
              <option value="polarizado">Polarizado</option>
              <option value="pelicula_seguridad">Película de seguridad</option>
              <option value="ambos">Ambos</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Estado</label>
            <select
              required
              value={formData.estado}
              onChange={(e) => setFormData({ ...formData, estado: e.target.value as any })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            >
              <option value="programado">Programado</option>
              <option value="en_proceso">En proceso</option>
              <option value="finalizado">Finalizado</option>
              <option value="anulado">Anulado</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Fecha</label>
            <input
              type="datetime-local"
              value={formData.fecha || ''}
              onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Opacidad (global)</label>
            <input
              type="text"
              value={formData.opacidad || ''}
              onChange={(e) => setFormData({ ...formData, opacidad: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            />
          </div>
        </div>

        <div>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={formData.retiro_material_anterior || false}
              onChange={(e) => setFormData({ ...formData, retiro_material_anterior: e.target.checked })}
              className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
            <span className="text-sm font-medium text-gray-700">Retiro de material anterior</span>
          </label>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Zonas intervenidas</label>
          {zonas.map((z, idx) => (
            <div key={idx} className="flex space-x-2 mb-2">
              <select
                value={z.zona}
                onChange={(e) => {
                  const newZonas = [...zonas]
                  newZonas[idx].zona = e.target.value
                  setZonas(newZonas)
                }}
                className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              >
                <option value="parabrisas">Parabrisas</option>
                <option value="laterales delanteros">Laterales delanteros</option>
                <option value="laterales traseros">Laterales traseros</option>
                <option value="luneta">Luneta</option>
              </select>
              <input
                type="text"
                placeholder="Opacidad"
                value={z.opacidad_aplicada}
                onChange={(e) => {
                  const newZonas = [...zonas]
                  newZonas[idx].opacidad_aplicada = e.target.value
                  setZonas(newZonas)
                }}
                className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
              <button type="button" onClick={() => setZonas(zonas.filter((_, i) => i !== idx))} className="px-2 py-1 text-red-600">-</button>
            </div>
          ))}
          <button type="button" onClick={() => setZonas([...zonas, { zona: 'parabrisas', opacidad_aplicada: '' }])} className="text-sm text-blue-600">+ Agregar zona</button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Asignaciones de instaladores</label>
          {asignaciones.map((a, idx) => (
            <div key={idx} className="flex space-x-2 mb-2">
              <select
                value={a.zona}
                onChange={(e) => {
                  const newAsig = [...asignaciones]
                  newAsig[idx].zona = e.target.value
                  setAsignaciones(newAsig)
                }}
                className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              >
                <option value="parabrisas">Parabrisas</option>
                <option value="laterales delanteros">Laterales delanteros</option>
                <option value="laterales traseros">Laterales traseros</option>
                <option value="luneta">Luneta</option>
              </select>
              <input
                type="text"
                placeholder="Instalador"
                value={a.instalador}
                onChange={(e) => {
                  const newAsig = [...asignaciones]
                  newAsig[idx].instalador = e.target.value
                  setAsignaciones(newAsig)
                }}
                className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
              />
              <button type="button" onClick={() => setAsignaciones(asignaciones.filter((_, i) => i !== idx))} className="px-2 py-1 text-red-600">-</button>
            </div>
          ))}
          <button type="button" onClick={() => setAsignaciones([...asignaciones, { zona: 'parabrisas', instalador: '' }])} className="text-sm text-blue-600">+ Agregar asignación</button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Observaciones</label>
          <textarea
            value={formData.observaciones || ''}
            onChange={(e) => setFormData({ ...formData, observaciones: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
            rows={3}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {loading ? 'Guardando...' : 'Registrar Instalación'}
        </button>
      </form>
    </div>
  )
}
