import type {ReactNode} from 'react'
import './portal.css'
export default function PortalAcceso({children}:{children:ReactNode}){
 return <main className="serna-welcome">
  <header className="welcome-top"><span>Serna Polarizados</span><span className="welcome-private"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true"><rect x="6" y="10" width="12" height="10" rx="2"/><path d="M9 10V7a3 3 0 0 1 6 0v3"/></svg>Portal privado</span></header>
  <div className="welcome-center"><section className="welcome-content" aria-labelledby="welcome-title">
   <img className="welcome-logo" src="/serna-logo.jpg" alt="Logotipo de Serna Polarizados" width="128" height="128"/>
   <h1 id="welcome-title">Bienvenido a<br/>Serna Polarizados</h1>
   <p className="welcome-description">Tu espacio de trabajo, en un solo lugar.</p>
   <div className="welcome-access">{children}</div>
  </section></div>
  <footer className="welcome-footer"><span>Acceso exclusivo para el equipo de Serna.</span><span>¿Necesitas acceso? Contacta a Gerencia.</span></footer>
 </main>
}
