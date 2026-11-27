import PersonalPage from './pages/PersonalPage'
import GerenciaPage from './pages/GerenciaPage'
import SoporteChat, {abrirSoporte} from './components/soporte/SoporteChat'
import MensajesPage from './pages/MensajesPage'
import TrabajoPage from './pages/TrabajoPage'
import InstaladoresPage from './pages/InstaladoresPage'
import { sedes } from './lib/sedes'
import InventarioPage from './pages/InventarioPage'
import { useState } from 'react'
import InstalacionForm from './components/InstalacionForm'
import VentasPage from './pages/VentasPage'
import InstalacionesPage from './pages/InstalacionesPage'
import LoginScreen from './components/LoginScreen'
import { AuthProvider, useAuth } from './context/AuthContext'

type Tab = 'personal' | 'gerencia' | 'nueva' | 'registro' | 'inventario' | 'ventas' | 'mi-trabajo' | 'instaladores' | 'mensajes'

const navItems: Array<{ id: Tab; label: string }> = [
  { id: 'gerencia', label: 'Gerencia' },
  { id: 'personal', label: 'Empleados' },
  { id: 'nueva', label: 'Nueva instalación' },
  { id: 'registro', label: 'Registro de instalaciones' },
  { id: 'ventas', label: 'Ventas y liquidación' },
  { id: 'inventario', label: 'Inventario' },
  { id: 'mensajes', label: 'Mensajes del equipo' },
  { id: 'instaladores', label: 'Instaladores' },
  { id: 'mi-trabajo', label: 'Mi trabajo' },
]

function AppShell() {
  const [activeTab, setActiveTab] = useState<Tab>('gerencia')
  const [sedeGerencia,setSedeGerencia] = useState<string|null>(null)
  const { loading, authorized, email, signOut, rol, entrar, perfiles } = useAuth()

  const permitidas = rol === 'propietario' ? ['ventas'] : rol === 'instalador' ? ['mi-trabajo'] : rol === 'administrador' ? ['nueva','registro','inventario','personal'] : ['gerencia','mensajes']
  const tab = permitidas.includes(activeTab) ? activeTab : permitidas[0]

  const [cambioError,setCambioError] = useState('')
  const [cambiando,setCambiando] = useState(false)
  async function abrir(tab:string,sede?:string){setCambioError('');setCambiando(true);try{if(sede&&sede!==sessionStorage.getItem('serna-sede'))await entrar(rol!,sede);setActiveTab(tab as Tab)}catch{setCambioError('No se pudo cambiar de sede. Intenta nuevamente.')}finally{setCambiando(false)}}

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
                <p className="text-xs sm:text-sm text-slate-500">{sedes.find(s => s.id === sessionStorage.getItem('serna-sede'))?.nombre} · {rol}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-xs text-slate-600">{email}</span>{rol!=='gerencia'&&<button className="text-xs text-blue-700" onClick={abrirSoporte}>Contacta a Gerencia</button>}
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
            {navItems.filter(item => permitidas.includes(item.id)).map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-all duration-200 border-b-2 ${
                  tab === item.id
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
        {rol!=='gerencia'&&perfiles.find(p=>p.rol===rol)?.sedes.length!>1&&<div className="flex flex-wrap items-center justify-end gap-3 mb-6"><label className="text-sm" htmlFor="gerencia-sede">Sede de trabajo</label><select id="gerencia-sede" disabled={cambiando} className="rounded-lg border px-3 py-2 text-sm" value={sessionStorage.getItem('serna-sede')||''} onChange={e=>void abrir(tab,e.target.value)}>{perfiles.find(p=>p.rol===rol)?.sedes.map(s=><option key={s.id} value={s.id}>{s.nombre}</option>)}</select></div>}
        {cambioError&&<p role="alert">{cambioError}</p>}
        {tab === 'gerencia' && <GerenciaPage sedeInicial={sedeGerencia} seleccionarSede={async s=>{if(sessionStorage.getItem('serna-sede')!==s)await entrar('gerencia',s);setSedeGerencia(s)}} />}
        <div key={sessionStorage.getItem('serna-sede')}>
        {tab === 'personal' && <PersonalPage sedeInicial={sessionStorage.getItem('serna-sede')||''} />}
        {tab === 'nueva' && <InstalacionForm />}
        {tab === 'ventas' && <VentasPage />}
        {tab === 'registro' && <InstalacionesPage />}
        {tab === 'inventario' && <InventarioPage />}
        {tab === 'mi-trabajo' && <TrabajoPage />}
        {tab === 'mensajes' && <MensajesPage />}
        {tab === 'instaladores' && <InstaladoresPage />}
        </div>
        {rol === 'propietario' && <p className="mt-5 text-sm text-slate-500">Reportes disponibles: ventas, descuentos y remuneraciones. Los gastos operativos y la utilidad neta aún no están registrados en el sistema.</p>}
      </main>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AppShell />
      <SoporteChat />
    </AuthProvider>
  )
}
