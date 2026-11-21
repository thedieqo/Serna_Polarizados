import type { ReactNode } from 'react'
import './portal.css'

export type RolAcceso = 'gerencia' | 'propietario' | 'administrador' | 'instalador'
const perfiles: { id: RolAcceso; titulo: string; descripcion: string; numero: string; icono: string }[] = [
  {id:'gerencia',titulo:'Gerencia',descripcion:'Supervisión y gestión de la operación.',numero:'01',icono:'M4 18V10h4v8m4 0V6h4v12m4 0V3M3 21h18'},
  {id:'propietario',titulo:'Propietario',descripcion:'Una visión general de la empresa.',numero:'02',icono:'M3 7l4 4 5-7 5 7 4-4-2 11H5L3 7zm3 14h12'},
  {id:'administrador',titulo:'Soy administrador',descripcion:'La operación diaria de tu sede.',numero:'03',icono:'M4 21V7l8-4 8 4v14M2 21h20M9 21v-6h6v6M8 8h1m6 0h1M8 11h1m6 0h1'},
  {id:'instalador',titulo:'Soy instalador',descripcion:'Tu espacio de trabajo y seguimiento.',numero:'04',icono:'M14 4a5 5 0 0 0-6 6L3 15a3 3 0 0 0 4 4l5-5a5 5 0 0 0 6-6l-4 4-3-3 3-5z'},
]
export default function PortalAcceso({rol,onSeleccionar,children}: {rol:RolAcceso|null;onSeleccionar:(rol:RolAcceso)=>void;children?:ReactNode}){
  return <main className="serna-portal">
    <header className="portal-top"><a href="/" className="portal-brand" aria-label="Serna Polarizados, inicio"><img src="/serna-logo.jpg" alt=""/><span>SERNA<span>POLARIZADOS</span></span></a><span className="portal-private"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true"><rect x="5" y="10" width="14" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>Portal privado de la empresa</span></header>
    <div className="portal-content"><section className="portal-intro"><span className="portal-eyebrow">PERSONAS. SEDES. UNA MISMA EMPRESA.</span><h1>Serna<br/><span>Polarizados.</span></h1><p>Tu equipo. Tu operación.<br/>Todo en un mismo lugar.</p><div className="portal-line" aria-hidden="true"/><span className="portal-caption">Precisión en cada instalación.<br/>Control en cada detalle.</span></section>
    <section className="portal-access" aria-labelledby="portal-access-title"><div className="portal-section-heading"><span className="portal-eyebrow">BIENVENIDO AL EQUIPO</span><h2 id="portal-access-title">Elige tu espacio</h2><p>Selecciona tu perfil para continuar.</p></div>
      <div className="portal-profiles" role="group" aria-label="Perfil de acceso">{perfiles.map(p=><button type="button" key={p.id} aria-pressed={rol===p.id} onClick={()=>onSeleccionar(p.id)} className={'portal-profile'+(rol===p.id?' is-selected':'')}><div className="portal-profile-top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={p.icono}/></svg><span>{p.numero}</span></div><h3>{p.titulo}</h3><p>{p.descripcion}</p><span className="portal-enter">{rol===p.id?'Seleccionado':'Seleccionar perfil'} <span aria-hidden="true">↗</span></span></button>)}</div>
      {children&&<div className="portal-login-panel">{children}</div>}
      <p className="portal-note">El acceso está reservado a las cuentas autorizadas para cada perfil.</p>
    </section></div>
    <footer className="portal-footer"><span>SERNA POLARIZADOS</span><span>Un espacio para quienes hacen parte del equipo.</span></footer>
  </main>
}
