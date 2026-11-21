import {useEffect,useRef,useState} from 'react'
import {useAuth} from '../../context/AuthContext'
import api from '../../services/api'
import Conversacion,{errorSoporte} from './Conversacion'
const pendienteKey='serna-soporte-pendiente'
export const abrirSoporte=()=>window.dispatchEvent(new Event('serna:soporte'))
export default function SoporteChat(){
 const {session,loading,signIn}=useAuth()
 const dialogo=useRef<HTMLDialogElement>(null),campo=useRef<HTMLInputElement>(null)
 const [cedula,setCedula]=useState(''),[error,setError]=useState(''),[busy,setBusy]=useState(false),[conversacion,setConversacion]=useState('')
 const verificacion=useRef(false),version=useRef(0)
 function cerrar(){version.current++;sessionStorage.removeItem(pendienteKey);dialogo.current?.close();setCedula('');setError('');setConversacion('')}
 async function verificar(documento:string){if(verificacion.current)return;verificacion.current=true;const actual=version.current;setBusy(true);setError('');try{const {data}=await api.post('/soporte/verificar',{documento});if(actual===version.current){setConversacion(data.conversacion_id);setCedula('')}}catch(e){if(actual===version.current)setError(errorSoporte(e).includes('No pudimos verificar')?'No encontramos acceso con esta cédula y cuenta. Revisa tus datos.':errorSoporte(e))}finally{sessionStorage.removeItem(pendienteKey);verificacion.current=false;setBusy(false)}}
 useEffect(()=>{const abrir=()=>{if(!dialogo.current?.open)dialogo.current?.showModal();campo.current?.focus()};window.addEventListener('serna:soporte',abrir);return()=>window.removeEventListener('serna:soporte',abrir)},[])
 useEffect(()=>{version.current++;setConversacion('')},[session?.user.id])
 useEffect(()=>{
  if(loading)return
  try{const value=sessionStorage.getItem(pendienteKey);if(!value)return;const p=JSON.parse(value);if(p.hasta<Date.now()||!/^\d{5,15}$/.test(p.documento)){sessionStorage.removeItem(pendienteKey);return}if(!dialogo.current?.open)dialogo.current?.showModal();setCedula(p.documento);if(session)void verificar(p.documento)}catch{sessionStorage.removeItem(pendienteKey)}
 },[session,loading])
 async function continuar(){if(!/^\d{5,15}$/.test(cedula)){setError('Ingresa entre 5 y 15 números, sin puntos ni espacios.');return}if(session){await verificar(cedula);return}sessionStorage.setItem(pendienteKey,JSON.stringify({documento:cedula,hasta:Date.now()+10*60*1000}));setBusy(true);try{await signIn()}finally{setBusy(false)}}
 return <dialog className={"soporte-dialog soporte-flotante "+(conversacion?"soporte-chat-abierto":"soporte-compacto")} ref={dialogo} aria-labelledby="soporte-titulo" onCancel={e=>{e.preventDefault();cerrar()}} onClick={e=>{if(e.target===dialogo.current){const r=dialogo.current.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)cerrar()}}}>
  <header className="soporte-cabecera"><div><h2 id="soporte-titulo">{conversacion?'Chat con Gerencia':'Contacta a Gerencia'}</h2></div><button className="soporte-cerrar" onClick={cerrar} aria-label="Cerrar contacto con Gerencia">×</button></header>
  {conversacion?<Conversacion key={conversacion} id={conversacion}/>:<form className="soporte-identidad" onSubmit={e=>{e.preventDefault();void continuar()}}>
   <div className="soporte-capsula">
    <input aria-label="Número de cédula" aria-describedby="soporte-nota" aria-invalid={Boolean(error)} id="soporte-cedula" ref={campo} placeholder="Ingresa el número de cédula" type="text" inputMode="numeric" pattern="[0-9]{5,15}" maxLength={15} autoComplete="off" required value={cedula} onChange={e=>{setCedula(e.target.value.replace(/\D/g,''));setError('')}} disabled={busy}/>
    <button className="soporte-continuar" aria-label={busy?'Verificando cédula':'Continuar al chat'} disabled={busy||loading||!cedula}>{busy?<span className="soporte-espera">…</span>:<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>}</button>
   </div>
   <p id="soporte-nota" className={error?'soporte-nota soporte-nota-error':'soporte-nota'} role={error?'alert':undefined}>{error||(busy?'Verificando tu acceso…':session?'Usaremos tu cuenta para verificar el acceso.':'Continúa con tu cuenta para abrir el chat.')}</p>
  </form>}
 </dialog>
}
