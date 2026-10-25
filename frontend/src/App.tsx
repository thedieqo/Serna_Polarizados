import { useState } from 'react'
import ClientesPage from './pages/ClientesPage'
import VehiculosPage from './pages/VehiculosPage'
import InstalacionesPage from './pages/InstalacionesPage'

type Tab = 'clientes' | 'vehiculos' | 'instalaciones'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('clientes')

  const navItems = [
    { id: 'clientes' as Tab, label: 'Clientes' },
    { id: 'vehiculos' as Tab, label: 'Vehículos' },
    { id: 'instalaciones' as Tab, label: 'Instalaciones' },
  ]

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center py-4 sm:py-6 gap-2">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-blue-800 flex items-center justify-center">
                <span className="text-white font-bold text-sm">SP</span>
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Serna Polarizados</h1>
                <p className="text-xs sm:text-sm text-slate-500">Sistema de Gestión de Instalaciones</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex overflow-x-auto space-x-1 sm:space-x-2">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-all duration-200 border-b-2 ${
                  activeTab === item.id
                    ? 'border-blue-800 text-blue-800'
                    : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {activeTab === 'clientes' && <ClientesPage />}
        {activeTab === 'vehiculos' && <VehiculosPage />}
        {activeTab === 'instalaciones' && <InstalacionesPage />}
      </main>
    </div>
  )
}

export default App
