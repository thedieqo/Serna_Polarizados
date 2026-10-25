import { useState } from 'react'
import type { VehiculoCreate } from '../types/vehiculo'
import { vehiculosService } from '../services/vehiculos'

export default function VehiculoForm({ onVehiculoCreado }: { onVehiculoCreado?: () => void }) {
  const [formData, setFormData] = useState<VehiculoCreate>({
    placa: '',
    descripcion: '',
    cliente_id: 0,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      await vehiculosService.create({ ...formData, cliente_id: Number(formData.cliente_id) })
      setSuccess(true)
      setFormData({ placa: '', descripcion: '', cliente_id: 0 })
      if (onVehiculoCreado) onVehiculoCreado()
      setTimeout(() => setSuccess(false), 3000)
    } catch (err: any) {
      setError(err.detail || 'Error al crear vehículo')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Registrar Vehículo</h2>

      {success && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md">
          <p className="text-sm text-green-800">Vehículo creado exitosamente</p>
        </div>
      )}

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Placa</label>
          <input
            type="text"
            required
            value={formData.placa}
            onChange={(e) => setFormData({ ...formData, placa: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Descripción (opcional)</label>
          <input
            type="text"
            value={formData.descripcion || ''}
            onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">ID Cliente</label>
          <input
            type="number"
            required
            value={formData.cliente_id || ''}
            onChange={(e) => setFormData({ ...formData, cliente_id: parseInt(e.target.value) || 0 })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-3 py-2 border"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {loading ? 'Guardando...' : 'Registrar Vehículo'}
        </button>
      </form>
    </div>
  )
}
