import {cuentaPruebas} from '../lib/accesoInicial'
import {useAuth} from '../context/AuthContext'
import PortalAcceso from './acceso/PortalAcceso'
const nombres:Record<string,string>={gerencia:'Gerencia',propietario:'Soy Serna',administrador:'Administrador',instalador:'Instalador'}
export default function LoginScreen(){
 const {loading,configured,session,email,error,perfiles,signIn,signOut,entrar,reintentar}=useAuth()
 return <PortalAcceso>
  {error&&<div className="welcome-error" role="alert">{error}</div>}
  {loading?<p role="status" className="welcome-status">Preparando tu espacio…</p>:!configured?<p role="alert" className="welcome-error">El acceso no está disponible en este momento. Contacta a Gerencia.</p>:!session?<>
   <button className="welcome-signin" onClick={()=>void signIn()}>Haz clic aquí para ingresar</button>
   <p className="welcome-explanation">Ingresa con tu cuenta autorizada. Abriremos el espacio que te corresponde.</p>
  </>:<>
   <div className="welcome-account"><p><small>Sesión iniciada</small>{email||session.user.email}</p><button className="welcome-link" onClick={()=>void signOut()}>Cambiar cuenta</button></div>
   {(email||session.user.email||'').toLowerCase()===cuentaPruebas&&!!perfiles.length&&<div className="welcome-test-profiles" aria-label="Perfiles de prueba">
    <p className="welcome-explanation">Elige el espacio que quieres probar.</p>
    <div className="welcome-profile-grid">{['propietario','gerencia','administrador','instalador'].map(id=>{const p=perfiles.find(p=>p.rol===id);return p?.sedes.length?<button key={id} type="button" onClick={()=>void entrar(id,p.sedes.find(s=>s.id==='el-carmen')?.id||p.sedes[0].id)}>{nombres[id]}</button>:null})}</div>
   </div>}
   {error&&<button className="welcome-link welcome-retry" onClick={()=>void reintentar()}>Volver a verificar acceso</button>}
  </>}
 </PortalAcceso>
}
