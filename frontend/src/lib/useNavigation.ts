import {useState} from 'react'
import {useAuth} from '../context/AuthContext'

// Solo navegación; nunca fichas, documentos, mensajes ni permisos.
export function useNavigation(key:string, fallback:string){
 const {email,rol}=useAuth()
 const storageKey=`serna-nav:${email}:${rol}:${key}`
 const [value,setValue]=useState(()=>{try{return sessionStorage.getItem(storageKey)||fallback}catch{return fallback}})
 function update(next:string){setValue(next);try{sessionStorage.setItem(storageKey,next)}catch{/* Navegación disponible aunque el navegador bloquee almacenamiento. */}}
 return [value,update] as const
}
