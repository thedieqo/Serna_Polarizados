import { useState } from 'react'
import { sedes } from '../lib/sedes'
import { useAuth } from '../context/AuthContext'
import PortalAcceso, { type RolAcceso } from './acceso/PortalAcceso'

export default function LoginScreen() {
  const { loading, configured, session, email, error, signIn, signOut } = useAuth()
  const [sede,setSede] = useState(sessionStorage.getItem('serna-sede')||'')
  const [rol,setRol] = useState<RolAcceso|null>((sessionStorage.getItem('serna-rol') as RolAcceso)||null)
  return <PortalAcceso rol={rol} onSeleccionar={r=>{setRol(r);sessionStorage.setItem('serna-rol',r)}}>
    {loading?<p role="status">Verificando acceso…</p>:<>
      {!rol?<p className="text-sm">Selecciona un perfil para iniciar sesión.</p>:<>
      <label className="block text-sm">Sede<select className="block w-full mt-2 mb-4 rounded-md p-3 border" value={sede} onChange={e=>{setSede(e.target.value);sessionStorage.setItem('serna-sede',e.target.value)}}><option value="">Selecciona una sede</option>{sedes.map(s=><option key={s.id} value={s.id}>{s.nombre}</option>)}</select></label>
      {error&&<p role="alert" className="text-sm text-red-800 mb-3">No se pudo autorizar el acceso. Comprueba el perfil, la sede y la cuenta seleccionados.</p>}
      {!configured&&<p className="text-sm mb-3">El acceso no está disponible en este momento.</p>}
      {session?<><p className="text-sm mb-3">Cuenta: {email||'Google'}</p><button type="button" disabled={!sede} onClick={()=>window.location.reload()} className="w-full bg-blue-700 rounded-md p-3 text-white disabled:opacity-40">Entrar con este perfil</button><button type="button" onClick={()=>void signOut()} className="w-full mt-2 p-2 text-sm">Usar otra cuenta</button></>:<button type="button" disabled={!sede||!configured} onClick={()=>void signIn()} className="w-full bg-blue-700 rounded-md p-3 text-white disabled:opacity-40">Continuar con Google</button>}
      </>}
    </>}
  </PortalAcceso>
}
