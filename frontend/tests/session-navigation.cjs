// NODE_PATH=/path/to/jsdom/node_modules node frontend/tests/session-navigation.cjs
const {JSDOM}=require('jsdom');
const assert=require('node:assert/strict');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const esbuild=require(path.join(root,'node_modules/esbuild'));
(async()=>{
 const dom=new JSDOM('<div id="app"></div>',{url:'https://qa.test',runScripts:'dangerously'}),w=dom.window;
 let calls=0;
 const session={user:{id:'a'},access_token:'first'};
 w.client={auth:{getSession:async()=>({data:{session}}),onAuthStateChange:fn=>{w.authEvent=fn;return {data:{subscription:{unsubscribe(){}}}}},signOut:async()=>{w.authEvent('SIGNED_OUT',null);return {}}}};
 w.api={get:async url=>{calls++;return {data:url==='/auth/accesos'?{email:'qa@example.com',perfiles:[{rol:'gerencia',sedes:[{id:'el-carmen',nombre:'El Carmen'}]}]}:{rol:'gerencia',authorized:true}}}};
 const result=await esbuild.build({stdin:{resolveDir:root,contents:`
 import React,{useEffect} from 'react';import {createRoot} from 'react-dom/client';
 import {AuthProvider,useAuth} from './src/context/AuthContext';
 import {useNavigation} from './src/lib/useNavigation';
 window.mounts=0;
 function Screen(){const [view,setView]=useNavigation('sede:el-carmen:vista','inicio');window.setView=setView;useEffect(()=>{window.mounts++},[]);return <div>{view}<input aria-label="Borrador"/></div>}
 function Shell(){const a=useAuth();window.auth=a;return a.loading?'Cargando':a.authorized?<Screen key={a.email}/>:<span>Sin acceso</span>}
 const root=createRoot(document.getElementById('app'));window.render=()=>root.render(<AuthProvider><Shell/></AuthProvider>);window.unmount=()=>root.render(null);window.render();
 `,loader:'tsx'},bundle:true,write:false,format:'iife',plugins:[{name:'mock',setup(b){b.onResolve({filter:/services\/api$/},()=>({path:'api',namespace:'mock'}));b.onResolve({filter:/lib\/supabase$/},()=>({path:'supabase',namespace:'mock'}));b.onLoad({filter:/.*/,namespace:'mock'},a=>({contents:a.path==='api'?'export default window.api':'export const supabase=window.client;export const supabaseConfigured=true;',loader:'js'}))}}]});
 w.eval(result.outputFiles[0].text);
 const wait=()=>new Promise(r=>setTimeout(r,60));await wait();
 assert.equal(calls,2,'Una sola validación inicial de permisos');
 w.setView('pendientes');await wait();w.document.querySelector('input').value='Trabajo sin guardar';
 for(const event of ['SIGNED_IN','SIGNED_IN','TOKEN_REFRESHED']){w.authEvent(event,{...session,access_token:'renewed'});await wait()}
 assert.equal(calls,2,'Recuperar el foco no repite consultas de acceso');
 assert.equal(w.mounts,1,'Renovar sesión no desmonta la pantalla');
 assert.equal(w.document.querySelector('input').value,'Trabajo sin guardar');
 assert(w.document.body.textContent.includes('pendientes'));
 w.unmount();await wait();w.render();await wait();
 assert(w.document.body.textContent.includes('pendientes'),'Recupera el apartado tras remontar');
 await w.auth.signOut();await wait();assert(w.document.body.textContent.includes('Sin acceso'));
 w.api.get=async url=>({data:url==='/auth/accesos'?{email:'other@example.com',perfiles:[]}:{authorized:false,rol:null}});
 w.authEvent('SIGNED_IN',{user:{id:'b'},access_token:'other'});await wait();
 assert(w.document.body.textContent.includes('Sin acceso'),'Otra identidad no hereda permisos');
 console.log('Sesión: foco, renovación, borrador, navegación restaurada, cierre y cambio de identidad verificados.');dom.window.close();
})().catch(e=>{console.error(e);process.exit(1)});
