import {useEffect,useRef,useState} from 'react'
import api from '../../services/api'
import './soporte.css'
export const errorSoporte=(e:unknown)=>{const d=(e as {detail?:unknown})?.detail;return typeof d==='string'?d:(d as {message?:string})?.message||'No se pudo completar la operación. Revisa tu conexión e intenta nuevamente.'}
type Mensaje={id:number;texto:string;autor_tipo:string;created_at:string}
export default function Conversacion({id,gerencia=false}:{id:string;gerencia?:boolean}){
 const [mensajes,setMensajes]=useState<Mensaje[]>([]),[texto,setTexto]=useState(''),[error,setError]=useState(''),[enviando,setEnviando]=useState(false),[anteriores,setAnteriores]=useState(false),[cargando,setCargando]=useState(true)
 const solicitud=useRef(crypto.randomUUID()),lista=useRef<HTMLDivElement>(null),bajar=useRef(true),ultimo=useRef<number|null>(null)
 const mezclar=(nuevos:Mensaje[])=>{ultimo.current=Math.max(ultimo.current||0,...nuevos.map(m=>m.id));setMensajes(prev=>Array.from(new Map([...prev,...nuevos].map(m=>[m.id,m])).values()).sort((a,b)=>a.id-b.id))}
 useEffect(()=>{let activo=true;let pendiente=false;let inicial=true;ultimo.current=null;setMensajes([]);setCargando(true)
  async function cargar(){if(pendiente)return;pendiente=true;try{const {data}=await api.get(`/soporte/conversaciones/${id}/mensajes`,{params:ultimo.current===null?{}:{despues:ultimo.current}});if(activo){mezclar(data.mensajes);if(inicial)setAnteriores(data.hay_anteriores);inicial=false;setError('')}}catch(e){if(activo)setError(errorSoporte(e))}finally{pendiente=false;if(activo)setCargando(false)}}
  void cargar();const timer=setInterval(()=>{if(document.visibilityState!=='hidden')void cargar()},5000)
  return()=>{activo=false;clearInterval(timer)}
 },[id])
 useEffect(()=>{if(bajar.current&&lista.current)lista.current.scrollTop=lista.current.scrollHeight},[mensajes])
 async function mas(){if(!mensajes.length)return;setCargando(true);try{const {data}=await api.get(`/soporte/conversaciones/${id}/mensajes`,{params:{antes:mensajes[0].id}});bajar.current=false;mezclar(data.mensajes);setAnteriores(data.hay_anteriores)}catch(e){setError(errorSoporte(e))}finally{setCargando(false)}}
 async function enviar(){if(!texto.trim()||enviando)return;setEnviando(true);setError('');try{await api.post(`/soporte/conversaciones/${id}/mensajes`,{solicitud_id:solicitud.current,texto:texto.trim()});setTexto('');solicitud.current=crypto.randomUUID();bajar.current=true;const {data}=await api.get(`/soporte/conversaciones/${id}/mensajes`,{params:ultimo.current===null?{}:{despues:ultimo.current}});mezclar(data.mensajes)}catch(e){setError(errorSoporte(e))}finally{setEnviando(false)}}
 return <div className={"soporte-conversacion "+(!cargando&&!mensajes.length?"soporte-sin-mensajes":"")}>
  {error&&<p className="soporte-error" role="alert">{error}</p>}
  <div className="soporte-mensajes" ref={lista} onScroll={()=>{const el=lista.current;if(el)bajar.current=el.scrollHeight-el.scrollTop-el.clientHeight<80}} role="log" aria-label="Historial de la conversación" aria-live="polite" aria-relevant="additions">
   {anteriores&&<button type="button" className="soporte-text-button" disabled={cargando} onClick={()=>void mas()}>Ver mensajes anteriores</button>}
   {cargando&&!mensajes.length&&<p>Consultando conversación…</p>}
   {!cargando&&!mensajes.length&&<p className="soporte-vacio">Cuéntanos en qué podemos ayudarte.</p>}
   {mensajes.map(m=><article key={m.id} className={'soporte-mensaje '+((m.autor_tipo==='gerencia')===gerencia?'propio':'')}><small>{m.autor_tipo==='gerencia'?'Gerencia':m.autor_tipo==='consulta'?'Consulta por identificación · remitente sin verificar':'Empleado'}</small><p>{m.texto}</p><time dateTime={m.created_at}>{new Date(m.created_at).toLocaleString('es-CO',{timeZone:'America/Bogota',dateStyle:'short',timeStyle:'short'})}</time></article>)}
  </div>
  <form className="soporte-redactar" onSubmit={e=>{e.preventDefault();void enviar()}}><label htmlFor={'mensaje-'+id}>Tu mensaje</label><textarea id={'mensaje-'+id} placeholder={gerencia?"Escribe tu respuesta…":"Cuéntanos qué inquietud tienes…"} maxLength={2000} rows={3} required value={texto} disabled={enviando} onChange={e=>{setTexto(e.target.value);solicitud.current=crypto.randomUUID()}}/><div><small>{texto.length}/2000</small><button className="soporte-primary" disabled={enviando||!texto.trim()}>{enviando?'Enviando…':'Enviar mensaje'}</button></div></form>
 </div>
}
