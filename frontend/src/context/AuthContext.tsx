import {createContext,useCallback,useContext,useEffect,useMemo,useRef,useState,type ReactNode} from 'react'
import type {Session} from '@supabase/supabase-js'
import api from '../services/api'
import {supabase,supabaseConfigured} from '../lib/supabase'

export type PerfilAutorizado={rol:string;sedes:{id:string;nombre:string}[]}
type Accesos={email:string;perfiles:PerfilAutorizado[];authorization_code:string|null}
type SessionStatus={rol:string|null;authorized:boolean;authorization_code:string|null}
type AuthContextValue={rol:string|null;loading:boolean;configured:boolean;session:Session|null;email:string|null;authorized:boolean;error:string|null;perfiles:PerfilAutorizado[];signIn:()=>Promise<void>;signOut:()=>Promise<void>;entrar:(rol:string,sede:string)=>Promise<void>;reintentar:()=>Promise<void>}
const AuthContext=createContext<AuthContextValue|null>(null)
function describeError(e:unknown):string {
 const d=(e as {detail?:unknown})?.detail
 if(typeof d==='string')return d
 return (d as {message?:string})?.message||'No pudimos verificar tu acceso. Intenta nuevamente.'
}
export function AuthProvider({children}:{children:ReactNode}){
 const [rol,setRol]=useState<string|null>(null),[loading,setLoading]=useState(true),[session,setSession]=useState<Session|null>(null),[email,setEmail]=useState<string|null>(null),[authorized,setAuthorized]=useState(false),[error,setError]=useState<string|null>(null),[perfiles,setPerfiles]=useState<PerfilAutorizado[]>([])
 const revision=useRef(0)
 const loadAccesses=useCallback(async()=>{
  const actual=++revision.current
  setLoading(true);setError(null)
  try{
   const {data}=await api.get<Accesos>('/auth/accesos')
   if(actual!==revision.current)return
   setEmail(data.email);setPerfiles(data.perfiles);setAuthorized(false);setRol(null)
   if(!data.perfiles.length){setError(data.authorization_code==='CORREO_NO_VERIFICADO'?'Tu correo aún no está verificado.':'Tu cuenta no tiene acceso asignado. Contacta a Gerencia.');return}
   let r=sessionStorage.getItem('serna-rol'),s=sessionStorage.getItem('serna-sede')
   if(data.perfiles.length===1&&data.perfiles[0].sedes.length===1){r=data.perfiles[0].rol;s=data.perfiles[0].sedes[0].id}
   const permitido=data.perfiles.some(p=>p.rol===r&&p.sedes.some(v=>v.id===s))
   if(!permitido){sessionStorage.removeItem('serna-rol');sessionStorage.removeItem('serna-sede');return}
   sessionStorage.setItem('serna-rol',r!);sessionStorage.setItem('serna-sede',s!)
   const respuesta=await api.get<SessionStatus>('/auth/session')
   if(actual!==revision.current)return
   setAuthorized(respuesta.data.authorized&&Boolean(respuesta.data.rol));setRol(respuesta.data.rol)
   if(!respuesta.data.authorized)setError('Tu acceso cambió. Contacta a Gerencia o utiliza otra cuenta.')
  }catch(e){if(actual===revision.current){setAuthorized(false);setRol(null);setPerfiles([]);setError(describeError(e))}}
  finally{if(actual===revision.current)setLoading(false)}
 },[])
 useEffect(()=>{
  if(!supabase){setLoading(false);return}
  let active=true
  const client=supabase
  const reset=()=>{revision.current++;setSession(null);setEmail(null);setRol(null);setPerfiles([]);setAuthorized(false);setLoading(false);setError(null)}
  void client.auth.getSession().then(({data,error:e})=>{if(!active)return;if(e){setLoading(false);setError('No pudimos recuperar tu sesión. Intenta iniciar sesión nuevamente.');return}setSession(data.session);if(data.session)void loadAccesses();else setLoading(false)})
  const {data}=client.auth.onAuthStateChange((_event,next)=>{
   if(!active)return
   setSession(next)
   if(!next){reset();return}
   // Consultar fuera del callback evita bloquear la renovación de la sesión de Google.
   setTimeout(()=>{if(active)void loadAccesses()},0)
  })
  const expired=()=>{reset();setError('La sesión expiró. Inicia sesión nuevamente.')}
  window.addEventListener('auth:expired',expired)
  return()=>{active=false;revision.current++;data.subscription.unsubscribe();window.removeEventListener('auth:expired',expired)}
 },[loadAccesses])
 const signIn=useCallback(async()=>{
  if(!supabase)return
  sessionStorage.removeItem('serna-rol');sessionStorage.removeItem('serna-sede');setError(null);setLoading(true)
  try{const {error:e}=await supabase.auth.signInWithOAuth({provider:'google',options:{redirectTo:`${window.location.origin}/`,queryParams:{prompt:'select_account'}}});if(e){setError('No se pudo abrir Google. Intenta nuevamente.');setLoading(false)}}catch{setError('No se pudo abrir Google. Revisa tu conexión.');setLoading(false)}
 },[])
 const signOut=useCallback(async()=>{
  if(!supabase)return
  revision.current++
  const {error:e}=await supabase.auth.signOut()
  if(e){setError('No se pudo cerrar la sesión. Intenta nuevamente.');return}
  sessionStorage.removeItem('serna-rol');sessionStorage.removeItem('serna-sede')
  setSession(null);setEmail(null);setRol(null);setPerfiles([]);setAuthorized(false);setError(null)
 },[])
 const entrar=useCallback(async(r:string,s:string)=>{
  if(!perfiles.some(p=>p.rol===r&&p.sedes.some(v=>v.id===s)))return
  sessionStorage.setItem('serna-rol',r);sessionStorage.setItem('serna-sede',s);await loadAccesses()
 },[perfiles,loadAccesses])
 const value=useMemo(()=>({rol,loading,configured:supabaseConfigured,session,email,authorized,error,perfiles,signIn,signOut,entrar,reintentar:loadAccesses}),[rol,loading,session,email,authorized,error,perfiles,signIn,signOut,entrar,loadAccesses])
 return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
export function useAuth(){const c=useContext(AuthContext);if(!c)throw new Error('useAuth debe usarse dentro de AuthProvider');return c}
