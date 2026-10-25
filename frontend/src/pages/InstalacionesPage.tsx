import { useState } from 'react'
import InstalacionForm from '../components/InstalacionForm'
import InstalacionList from '../components/InstalacionList'

export default function InstalacionesPage() {
  const [refreshKey, setRefreshKey] = useState(0)

  const handleInstalacionCreada = () => {
    setRefreshKey((prev) => prev + 1)
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Gestión de Instalaciones</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <InstalacionForm onInstalacionCreada={handleInstalacionCreada} />
        </div>
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Listado de Instalaciones</h3>
          </div>
          <InstalacionList refreshKey={refreshKey} />
        </div>
      </div>
    </div>
  )
}
