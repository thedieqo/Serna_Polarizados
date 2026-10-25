import { useState, useEffect } from 'react'
import type { VehiculoRead } from '../types/vehiculo'
import { vehiculosService } from '../services/vehiculos'
import VehiculoForm from '../components/VehiculoForm'

export default function VehiculosPage() {
  const [vehiculos, setVehiculos] = useState<VehiculoRead[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchVehiculos = async () => {
    try {
      setLoading(true)
      const data = await vehiculosService.getAll()
      setVehiculos(data)
      setError(null)
    } catch (err: any) {
      setError(err.detail || 'Error al cargar vehículos')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchVehiculos()
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Gestión de Vehículos</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <VehiculoForm onVehiculoCreado={fetchVehiculos} />
        </div>
        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Lista de Vehículos</h3>
            </div>

            {loading && (
              <div className="p-6 text-center text-gray-500">Cargando...</div>
            )}

            {error && (
              <div className="p-6">
                <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              </div>
            )}

            {!loading && !error && vehiculos.length === 0 && (
              <div className="p-6 text-center text-gray-500">No hay vehículos registrados</div>
            )}

            {!loading && !error && vehiculos.length > 0 && (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Placa</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID Cliente</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {vehiculos.map((vehiculo) => (
                      <tr key={vehiculo.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{vehiculo.id}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{vehiculo.placa}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{vehiculo.descripcion || '-'}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{vehiculo.cliente_id}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
