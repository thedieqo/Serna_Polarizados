import {useEffect,useState} from 'react'
import PersonalPage from './PersonalPage'
import InstalacionesPage from './InstalacionesPage'
import api from '../services/api'
import {errorSoporte} from '../components/soporte/Conversacion'
import './gerencia.css'
type Sede={id:string;nombre:string;lavadero:boolean;operativa:boolean}
type Resumen={sedes:Sede[];equipo_por_sede:{sede:string|null;total:number;activos:number}[]}
export default function GerenciaPage({seleccionarSede,sedeInicial=null}:{seleccionarSede:(sede:string)=>Promise<void>;sedeInicial?:string|null}){
 const [vista,setVista]=useState('inicio'),[resumen,setResumen]=useState<Resumen|null>(null),[sede,setSede]=useState<Sede|null>(null),[seccion,setSeccion]=useState('inicio'),[error,setError]=useState(''),[busy,setBusy]=useState(false),[revision,setRevision]=useState(0),[formulario,setFormulario]=useState(false),[nombre,setNombre]=useState(''),[ciudad,setCiudad]=useState('')
 useEffect(()=>{let vigente=true;void api.get('/gerencia/gestion/resumen').then(r=>{if(vigente)setResumen(r.data)}).catch(e=>{if(vigente)setError(errorSoporte(e))});return()=>{vigente=false}},[revision])
 useEffect(()=>{if(sedeInicial&&resumen&&!sede){const destino=resumen.sedes.find(s=>s.id===sedeInicial);if(destino){setSede(destino);setVista('sedes')}}},[sedeInicial,!!resumen])
 function irSedes(){setVista('sedes');setSede(null);setSeccion('inicio');setError('')}
 async function entrar(s:Sede){setBusy(true);setError('');try{if(s.operativa)await seleccionarSede(s.id);setSede(s);setSeccion('inicio')}catch(e){setError(errorSoporte(e))}finally{setBusy(false)}}
 async function crear(){setBusy(true);setError('');try{const r=await api.post('/gerencia/gestion/sedes',{nombre,ciudad});setFormulario(false);setNombre('');setCiudad('');setRevision(v=>v+1);setSede(r.data);setSeccion('inicio')}catch(e){setError(errorSoporte(e))}finally{setBusy(false)}}
 return <div className="gerencia gerencia-simple">
 <nav className="gerencia-tabs" aria-label="Secciones de Gerencia"><button aria-current={vista==='inicio'?'page':undefined} onClick={()=>{setVista('inicio');setSede(null);setFormulario(false)}}>Inicio</button><button aria-current={vista==='sedes'?'page':undefined} onClick={irSedes}>Sedes</button></nav>
 {error&&<p className="gerencia-error" role="alert">{error}</p>}
 {vista==='inicio'&&<section className="gerencia-bienvenida"><h2>Buen día, Milena</h2><p>Bienvenida a tu espacio de Gerencia.</p><button className="gerencia-entrada" onClick={irSedes}><span>Sedes</span><small>Encuentra cada sede y accede a su equipo.</small><strong>Ver sedes</strong></button></section>}
 {vista==='sedes'&&!sede&&<><div className="gerencia-section-title"><div><h2>Sedes</h2><p className="gerencia-nota">{resumen?`${resumen.sedes.length} sedes de Serna Polarizados`:'Cargando sedes…'}</p></div><button className="gerencia-primary" onClick={()=>{setFormulario(v=>!v);setError('')}}>Crear sede</button></div>
 {formulario&&<form className="gerencia-editor" onSubmit={e=>{e.preventDefault();void crear()}}><h3>Nueva sede</h3><p className="gerencia-nota">Registra la sede. Sus funciones se configurarán después.</p><fieldset disabled={busy}><div className="gerencia-form-grid"><label>Nombre de la sede<input autoFocus required minLength={2} maxLength={100} placeholder="Nombre" value={nombre} onChange={e=>setNombre(e.target.value)}/></label><label>Ciudad<input required minLength={2} maxLength={100} placeholder="Ciudad" value={ciudad} onChange={e=>setCiudad(e.target.value)}/></label></div><div className="gerencia-form-actions"><button className="gerencia-primary">{busy?'Guardando…':'Guardar sede'}</button><button type="button" onClick={()=>setFormulario(false)}>Cancelar</button></div></fieldset></form>}
 <div className="gerencia-sedes">{resumen?.sedes.map(s=><button className="gerencia-sede-card" key={s.id} disabled={busy} onClick={()=>void entrar(s)}><h3>{s.nombre}</h3><p>{s.operativa?`${resumen.equipo_por_sede.find(x=>x.sede===s.id)?.total||0} empleados`:'Funciones por configurar'}</p><span>Entrar a la sede</span></button>)}</div></>}
 {vista==='sedes'&&sede&&<><button className="gerencia-volver" onClick={irSedes}>← Todas las sedes</button><header className="gerencia-heading"><div><h2>{sede.nombre}</h2><span>{sede.operativa?'El espacio de esta sede.':'Sede registrada'}</span></div></header>
 {!sede.operativa?<p className="gerencia-nota">La sede ya aparece en el directorio. Sus funciones, empleados y accesos están pendientes de configuración.</p>:<><nav className="gerencia-tabs" aria-label="Funciones de la sede">{[['inicio','Inicio de sede'],['empleados','Empleados'],['registro','Registro de instalaciones']].map(([id,label])=><button key={id} aria-current={seccion===id?'page':undefined} onClick={()=>setSeccion(id)}>{label}</button>)}</nav>
 {seccion==='inicio'&&<div className="gerencia-accesos"><button onClick={()=>setSeccion('empleados')}><strong>Empleados</strong><span>Consulta y organiza el equipo de {sede.nombre}.</span></button><button onClick={()=>setSeccion('registro')}><strong>Registro de instalaciones</strong><span>Consulta las instalaciones realizadas en esta sede.</span></button></div>}
 {seccion==='empleados'&&<PersonalPage key={sede.id} sedeInicial={sede.id} sedeFija alCambiar={()=>setRevision(v=>v+1)}/>}
 {seccion==='registro'&&<InstalacionesPage key={sede.id}/>}</>}
 </>}
 </div>
}
