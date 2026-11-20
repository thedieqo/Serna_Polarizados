import { useState } from 'react'
import InstalacionForm from './components/InstalacionForm'
import InstalacionesPage from './pages/InstalacionesPage'
import LoginScreen from './components/LoginScreen'
import { AuthProvider, useAuth } from './context/AuthContext'

type Tab = 'nueva' | 'registro' | 'inventario'

const navItems: Array<{ id: Tab; label: string }> = [
  { id: 'nueva', label: 'Nueva instalación' },
  { id: 'registro', label: 'Registro de instalaciones' },
  { id: 'inventario', label: 'Inventario' },
]

function AppShell() {
  const [activeTab, setActiveTab] = useState<Tab>('nueva')
  const { loading, authorized, email, signOut } = useAuth()

  if (loading || !authorized) {
    return <LoginScreen />
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center py-4 sm:py-6 gap-2">
            <div className="flex items-center gap-3">
              <img src="/serna-logo.jpg" alt="Logotipo Serna Polarizados" className="h-10 w-10 rounded-lg object-contain shrink-0" />
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Serna Polarizados</h1>
                <p className="text-xs sm:text-sm text-slate-500">Sistema de Gestión de Instalaciones</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-xs text-slate-600">{email}</span>
              <button
                type="button"
                onClick={() => void signOut()}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50"
              >
                Cerrar sesión
              </button>
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
        {activeTab === 'nueva' && <InstalacionForm />}
        {activeTab === 'registro' && <InstalacionesPage />}
        {activeTab === 'inventario' && (
          <div className="bg-white shadow rounded-lg p-10 text-center">
            <h2 className="text-xl font-semibold text-gray-900">Inventario</h2>
            <p className="text-sm text-gray-500 mt-2">Próximamente</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  )
}
