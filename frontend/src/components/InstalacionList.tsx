import { useEffect, useState } from 'react'
import type { InstalacionRead } from '../types/instalacion'
import type { VehiculoRead } from '../types/vehiculo'
import { instalacionesService } from '../services/instalaciones'
import { vehiculosService } from '../services/vehiculos'

export default function InstalacionList({ refreshKey }: { refreshKey?: number }) {
  const [instalaciones, setInstalaciones] = useState<InstalacionRead[]>([])
  const [vehiculos, setVehiculos] = useState<VehiculoRead[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      const [instData, vehData] = await Promise.all([
        instalacionesService.getAll(),
        vehiculosService.getAll(),
      ])
      setInstalaciones(instData)
      setVehiculos(vehData)
      setError(null)
    } catch (err: any) {
      setError(err.detail || err.message || 'Error al cargar instalaciones')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [refreshKey])

  const getVehiculoInfo = (vehiculoId: number) => {
    const v = vehiculos.find((veh) => veh.id === vehiculoId)
    if (!v) return `Vehículo #${vehiculoId}`
    return `${v.placa} - Cliente ${v.cliente_id}`
  }

  const formatDate = (fecha: string) => {
    try {
      return new Date(fecha).toLocaleString()
    } catch {
      return fecha
    }
  }

  if (loading) {
    return <div className="p-4 text-center text-gray-500">Cargando...</div>
  }

  if (error) {
    return (
      <div className="p-4">
        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      </div>
    )
  }

  if (instalaciones.length === 0) {
    return <div className="p-4 text-center text-gray-500">No hay instalaciones registradas</div>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vehículo</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Servicio</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Zonas</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Instaladores</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Observaciones</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {instalaciones.map((inst) => (
            <tr key={inst.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{inst.id}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{getVehiculoInfo(inst.vehiculo_id)}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{inst.tipo_servicio}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{inst.estado}</td>
              <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{formatDate(inst.fecha)}</td>
              <td className="px-4 py-3 text-sm text-gray-900">
                {Array.isArray(inst.zonas) && inst.zonas.length > 0
                  ? inst.zonas.map((z: any, idx: number) => (
                      <div key={idx}>
                        {z.zona || z.nombre || '-'} {z.opacidad_aplicada ? `(${z.opacidad_aplicada})` : ''}
                      </div>
                    ))
                  : '-'}
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">
                {Array.isArray(inst.asignaciones_instaladores) && inst.asignaciones_instaladores.length > 0
                  ? inst.asignaciones_instaladores.map((a: any, idx: number) => (
                      <div key={idx}>
                        {a.zona || '-'}: {a.instalador || '-'}
                      </div>
                    ))
                  : '-'}
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">{inst.observaciones || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
