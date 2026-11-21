import type {PerfilAutorizado} from '../context/AuthContext'
export const cuentaPruebas='diegonangumaw@gmail.com'
export function accesoInicial(email:string,perfiles:PerfilAutorizado[],rolGuardado:string|null,sedeGuardada:string|null){
 const previo=perfiles.find(p=>p.rol===rolGuardado&&p.sedes.some(s=>s.id===sedeGuardada))
 if(previo)return {rol:previo.rol,sede:sedeGuardada!}
 if(email.trim().toLowerCase()===cuentaPruebas)return null
 // Solo el servidor decide qué perfiles y sedes existen para esta cuenta.
 const perfil=perfiles.find(p=>p.sedes.length>0)
 return perfil?{rol:perfil.rol,sede:perfil.sedes[0].id}:null
}
