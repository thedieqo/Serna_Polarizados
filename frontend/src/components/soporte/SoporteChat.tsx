import {useEffect,useRef,useState} from 'react'
import api from '../../services/api'
import {errorSoporte} from './Conversacion'
import './soporte.css'
export const abrirSoporte=()=>window.dispatchEvent(new Event('serna:soporte'))
export default function SoporteChat(){
 const dialogo=useRef<HTMLDialogElement>(null),campo=useRef<HTMLInputElement>(null),redactar=useRef<HTMLTextAreaElement>(null)
 const [cedula,setCedula]=useState(''),[texto,setTexto]=useState(''),[error,setError]=useState(''),[busy,setBusy]=useState(false),[paso,setPaso]=useState<'identificacion'|'mensaje'|'enviado'>('identificacion')
 const version=useRef(0),solicitud=useRef(crypto.randomUUID()),pendiente=useRef(false)
 function cerrar(){version.current++;dialogo.current?.close();setCedula('');setTexto('');setError('');setPaso('identificacion');solicitud.current=crypto.randomUUID()}
 useEffect(()=>{sessionStorage.removeItem('serna-soporte-pendiente');const abrir=()=>{if(!dialogo.current?.open)dialogo.current?.showModal();campo.current?.focus()};window.addEventListener('serna:soporte',abrir);return()=>window.removeEventListener('serna:soporte',abrir)},[])
 useEffect(()=>{if(paso==='mensaje')redactar.current?.focus()},[paso])
 async function continuar(){if(pendiente.current)return;pendiente.current=true;setBusy(true);setError('');const actual=version.current;try{if(paso==='identificacion'){await api.post('/soporte/contacto/verificar',{documento:cedula});if(actual===version.current)setPaso('mensaje')}else{await api.post('/soporte/contacto/mensajes',{documento:cedula,texto:texto.trim(),solicitud_id:solicitud.current});if(actual===version.current){setPaso('enviado');setTexto('')}}}catch(e){if(actual===version.current)setError(errorSoporte(e))}finally{pendiente.current=false;setBusy(false)}}
 return <dialog className="soporte-dialog soporte-flotante soporte-compacto" ref={dialogo} aria-labelledby="soporte-titulo" onCancel={e=>{e.preventDefault();cerrar()}} onClick={e=>{if(e.target===dialogo.current){const r=dialogo.current.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)cerrar()}}}>
  <header className="soporte-cabecera"><h2 id="soporte-titulo">Contacta a Gerencia</h2><button className="soporte-cerrar" onClick={cerrar} aria-label="Cerrar contacto con Gerencia">×</button></header>
  {paso==='enviado'?<div className="soporte-identidad"><p role="status" className="soporte-confirmacion">Tu inquietud fue enviada a Gerencia.</p><button className="soporte-primary" onClick={cerrar}>Listo</button></div>:<form className="soporte-identidad" onSubmit={e=>{e.preventDefault();void continuar()}}>
   {paso==='identificacion'?<div className="soporte-capsula"><input aria-label="Número de identificación" aria-describedby="soporte-nota" aria-invalid={Boolean(error)} ref={campo} placeholder="Ingrese su número de identificación" type="text" inputMode="numeric" pattern="[0-9]{5,15}" maxLength={15} autoComplete="off" required value={cedula} onChange={e=>{setCedula(e.target.value.replace(/\D/g,''));setError('')}} disabled={busy}/><button className="soporte-continuar" aria-label="Continuar" disabled={busy||!cedula}>{busy?'…':<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>}</button></div>:<div className="soporte-consulta"><textarea ref={redactar} aria-label="Tu inquietud" placeholder="Cuéntanos qué inquietud tienes…" maxLength={2000} rows={4} required disabled={busy} value={texto} onChange={e=>{setTexto(e.target.value);solicitud.current=crypto.randomUUID()}}/><button className="soporte-primary" disabled={busy||!texto.trim()}>{busy?'Enviando…':'Enviar a Gerencia'}</button></div>}
   <p id="soporte-nota" className={'soporte-nota'+(error?' soporte-nota-error':'')} role={error?'alert':undefined}>{error||(paso==='identificacion'?'Ingresa tu identificación para escribirnos.':'Tu inquietud llegará directamente a Gerencia.')}</p>
  </form>}
 </dialog>
}
