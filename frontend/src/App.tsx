import { useState } from 'react'
import ClientesPage from './pages/ClientesPage'
import VehiculosPage from './pages/VehiculosPage'
import InstalacionesPage from './pages/InstalacionesPage'

type Tab = 'clientes' | 'vehiculos' | 'instalaciones'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('clientes')

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Serna Polarizados</h1>
              <span className="ml-4 text-sm text-gray-500">Sistema de Gestión</span>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('clientes')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'clientes'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Clientes
            </button>
            <button
              onClick={() => setActiveTab('vehiculos')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'vehiculos'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Vehículos
            </button>
            <button
              onClick={() => setActiveTab('instalaciones')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'instalaciones'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Instalaciones
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'clientes' && <ClientesPage />}
        {activeTab === 'vehiculos' && <VehiculosPage />}
        {activeTab === 'instalaciones' && <InstalacionesPage />}
      </main>
    </div>
  )
}

export default App
