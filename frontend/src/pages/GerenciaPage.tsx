import {useEffect,useState} from 'react'
import PanelSede from './PanelSede'
import api from '../services/api'
import {errorSoporte} from '../components/soporte/Conversacion'
import './gerencia.css'
type Sede={id:string;nombre:string;lavadero:boolean;operativa:boolean}
type Resumen={sedes:Sede[];equipo_por_sede:{sede:string|null;total:number;activos:number}[]}
export default function GerenciaPage({seleccionarSede,sedeInicial=null}:{seleccionarSede:(sede:string)=>Promise<void>;sedeInicial?:string|null}){
 const [vista,setVista]=useState('inicio'),[resumen,setResumen]=useState<Resumen|null>(null),[sede,setSede]=useState<Sede|null>(null),[error,setError]=useState(''),[busy,setBusy]=useState(false),[revision,setRevision]=useState(0),[formulario,setFormulario]=useState(false),[nombre,setNombre]=useState(''),[ciudad,setCiudad]=useState('')
 useEffect(()=>{let vigente=true;void api.get('/gerencia/gestion/resumen').then(r=>{if(vigente)setResumen(r.data)}).catch(e=>{if(vigente)setError(errorSoporte(e))});return()=>{vigente=false}},[revision])
 useEffect(()=>{if(sedeInicial&&resumen&&!sede){const destino=resumen.sedes.find(s=>s.id===sedeInicial);if(destino){setSede(destino);setVista('sedes')}}},[sedeInicial,!!resumen])
 function irSedes(){setVista('sedes');setSede(null);setError('')}
 async function entrar(s:Sede){setBusy(true);setError('');try{if(s.operativa)await seleccionarSede(s.id);setSede(s)}catch(e){setError(errorSoporte(e))}finally{setBusy(false)}}
 async function crear(){setBusy(true);setError('');try{const r=await api.post('/gerencia/gestion/sedes',{nombre,ciudad});setFormulario(false);setNombre('');setCiudad('');setRevision(v=>v+1);setSede(r.data)}catch(e){setError(errorSoporte(e))}finally{setBusy(false)}}
 return <div className="gerencia gerencia-simple">
 {error&&<p className="gerencia-error" role="alert">{error}</p>}
 {vista==='inicio'&&<section className="gerencia-bienvenida"><h2>Buen día, Milena</h2><p>Bienvenida a tu espacio de Gerencia.</p><button className="gerencia-entrada" onClick={irSedes}><span>Sedes</span><small>Encuentra cada sede y accede a su equipo.</small><strong>Ver sedes</strong></button></section>}
 {vista==='sedes'&&!sede&&<><div className="gerencia-section-title"><div><h2>Sedes</h2><p className="gerencia-nota">{resumen?`${resumen.sedes.length} sedes de Serna Polarizados`:'Cargando sedes…'}</p></div><button className="gerencia-primary" onClick={()=>{setFormulario(v=>!v);setError('')}}>Crear sede</button></div>
 {formulario&&<form className="gerencia-editor" onSubmit={e=>{e.preventDefault();void crear()}}><h3>Nueva sede</h3><p className="gerencia-nota">Registra la sede. Sus funciones se configurarán después.</p><fieldset disabled={busy}><div className="gerencia-form-grid"><label>Nombre de la sede<input autoFocus required minLength={2} maxLength={100} placeholder="Nombre" value={nombre} onChange={e=>setNombre(e.target.value)}/></label><label>Ciudad<input required minLength={2} maxLength={100} placeholder="Ciudad" value={ciudad} onChange={e=>setCiudad(e.target.value)}/></label></div><div className="gerencia-form-actions"><button className="gerencia-primary">{busy?'Guardando…':'Guardar sede'}</button><button type="button" onClick={()=>setFormulario(false)}>Cancelar</button></div></fieldset></form>}
 <div className="gerencia-sedes">{resumen?.sedes.map(s=><button className="gerencia-sede-card" key={s.id} disabled={busy} onClick={()=>void entrar(s)}><h3>{s.nombre}</h3><p>{s.operativa?`${resumen.equipo_por_sede.find(x=>x.sede===s.id)?.total||0} empleados`:'Funciones por configurar'}</p><span>Entrar a la sede</span></button>)}</div></>}
 {vista==='sedes'&&sede&&<><button className="gerencia-volver" onClick={irSedes}>← Todas las sedes</button><PanelSede key={sede.id} sede={sede} alCambiar={()=>setRevision(v=>v+1)}/></>}

 </div>
}
