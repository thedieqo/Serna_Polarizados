import {useState} from 'react'
import {useAuth} from '../context/AuthContext'
import PortalAcceso from './acceso/PortalAcceso'
const nombres:Record<string,string>={gerencia:'Gerencia',propietario:'Dueño',administrador:'Administración',instalador:'Instalador'}
export default function LoginScreen(){
 const {loading,configured,session,email,error,perfiles,signIn,signOut,entrar,reintentar}=useAuth()
 const [elegido,setElegido]=useState(''),[sedeElegida,setSedeElegida]=useState('')
 const perfil=perfiles.find(p=>p.rol===elegido)||(perfiles.length===1?perfiles[0]:undefined)
 const sede=perfil?.sedes.some(s=>s.id===sedeElegida)?sedeElegida:perfil?.sedes.length===1?perfil.sedes[0].id:''
 return <PortalAcceso>
  {error&&<div className="welcome-error" role="alert">{error}</div>}
  {loading?<p role="status" className="welcome-status">Preparando tu espacio…</p>:!configured?<p role="alert" className="welcome-error">El acceso no está disponible en este momento. Contacta a Gerencia.</p>:!session?<>
   <button className="welcome-signin" onClick={()=>void signIn()}>Haz clic aquí para ingresar</button>
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
