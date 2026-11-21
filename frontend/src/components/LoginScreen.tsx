import {useState} from 'react'
import {useAuth} from '../context/AuthContext'
import PortalAcceso from './acceso/PortalAcceso'
const nombres:Record<string,string>={gerencia:'Gerencia',propietario:'Dueño',administrador:'Administración',instalador:'Instalador'}
function GoogleIcon(){return <svg viewBox="0 0 48 48" aria-hidden="true"><path fill="#4285F4" d="M43.6 24.5c0-1.4-.1-2.8-.4-4.1H24v7.8h11a9.4 9.4 0 0 1-4.1 6.2v5.1h6.6c3.9-3.5 6.1-8.7 6.1-15Z"/><path fill="#34A853" d="M24 44c5.5 0 10.1-1.8 13.5-4.9l-6.6-5.1c-1.8 1.2-4.1 1.9-6.9 1.9-5.3 0-9.8-3.6-11.4-8.4H5.8v5.3A20.4 20.4 0 0 0 24 44Z"/><path fill="#FBBC05" d="M12.6 27.5a12.4 12.4 0 0 1 0-7V15H5.8a20 20 0 0 0 0 18l6.8-5.5Z"/><path fill="#EA4335" d="M24 12.1c3 0 5.6 1 7.7 3l5.7-5.7A19.5 19.5 0 0 0 24 4 20.4 20.4 0 0 0 5.8 15l6.8 5.5c1.6-4.8 6.1-8.4 11.4-8.4Z"/></svg>}
export default function LoginScreen(){
 const {loading,configured,session,email,error,perfiles,signIn,signOut,entrar,reintentar}=useAuth()
 const [elegido,setElegido]=useState(''),[sedeElegida,setSedeElegida]=useState('')
 const perfil=perfiles.find(p=>p.rol===elegido)||(perfiles.length===1?perfiles[0]:undefined)
 const sede=perfil?.sedes.some(s=>s.id===sedeElegida)?sedeElegida:perfil?.sedes.length===1?perfil.sedes[0].id:''
 return <PortalAcceso>
  {error&&<div className="welcome-error" role="alert">{error}</div>}
  {loading?<p role="status" className="welcome-status">Preparando tu espacio…</p>:!configured?<p role="alert" className="welcome-error">El acceso no está disponible en este momento. Contacta a Gerencia.</p>:!session?<>
   <button className="welcome-google" onClick={()=>void signIn()}><GoogleIcon/>Continuar con Google</button>
   <p className="welcome-explanation">Ingresa con tu cuenta autorizada. Abriremos el espacio que te corresponde.</p>
  </>:<>
   <div className="welcome-account"><p><small>Sesión iniciada</small>{email||session.user.email}</p><button className="welcome-link" onClick={()=>void signOut()}>Cambiar cuenta</button></div>
   {!!perfiles.length&&<form onSubmit={e=>{e.preventDefault();if(perfil&&sede)void entrar(perfil.rol,sede)}}>
    <div className="welcome-fields">
     {perfiles.length>1?<label>Tu espacio<select required value={perfil?.rol||''} onChange={e=>{setElegido(e.target.value);setSedeElegida('')}}><option value="">Selecciona un espacio</option>{perfiles.map(p=><option key={p.rol} value={p.rol}>{nombres[p.rol]||p.rol}</option>)}</select></label>:<label>Tu espacio<span className="welcome-field-static">{nombres[perfil!.rol]||perfil!.rol}</span></label>}
     {perfil&&(perfil.sedes.length>1?<label>Sede<select required value={sede} onChange={e=>setSedeElegida(e.target.value)}><option value="">Selecciona una sede</option>{perfil.sedes.map(s=><option key={s.id} value={s.id}>{s.nombre}</option>)}</select></label>:<label>Sede<span className="welcome-field-static">{perfil.sedes[0]?.nombre}</span></label>)}
    </div><button className="welcome-submit" disabled={!perfil||!sede}>Entrar a mi espacio</button>
   </form>}
   {error&&<button className="welcome-link welcome-retry" onClick={()=>void reintentar()}>Volver a verificar acceso</button>}
  </>}
 </PortalAcceso>
}
