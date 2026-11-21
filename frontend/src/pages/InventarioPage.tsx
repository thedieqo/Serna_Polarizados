import { useEffect, useState } from 'react'
import api from '../services/api'

type Item = { sku:string; tecnologia:string; opacidad_id:string; material:string; disponible_m:number }
type Movimiento = { id:number; sku:string; instalacion_id:number|null; cantidad_cm:number; motivo:string; created_at:string }
type Inventario = {items:Item[]; movimientos:Movimiento[]}
const metros=(n:number)=>new Intl.NumberFormat('es-CO',{minimumFractionDigits:2,maximumFractionDigits:2}).format(n)+' m'
export default function InventarioPage(){
  const [data,setData]=useState<Inventario|null>(null)
  const [error,setError]=useState('')
  const [loading,setLoading]=useState(true)
  const [revision,setRevision]=useState(0)
  const [material,setMaterial]=useState('todos')
  useEffect(()=>{
    let activo=true; setLoading(true);setError('')
    api.get<Inventario>('/inventario/').then(r=>{if(activo)setData(r.data)})
      .catch(()=>{if(activo)setError('No se pudo consultar el inventario. Intenta actualizar.')})
      .finally(()=>{if(activo)setLoading(false)})
    return ()=>{activo=false}
  },[revision])
  const items=data?.items.filter(i=>material==='todos'||i.material===material)||[]
  return <div className="space-y-6">
    <div className="flex flex-wrap justify-between gap-4"><div><h2 className="text-xl font-semibold">Inventario de material</h2><p className="text-sm mt-2">Existencias de la sede actual · metros lineales · rollo inicial de 200 m por combinación.</p></div><button disabled={loading} onClick={()=>setRevision(n=>n+1)} className="bg-blue-700 text-white rounded-md px-4 py-2 disabled:opacity-50">Actualizar</button></div>
    <div className="bg-white rounded-lg p-5 space-y-2"><p>Medidas de referencia: parabrisas 1,50 m · cada pareja de laterales 0,80 m · luneta 1,10 m · sunroof sencillo 1,10 m · doble 1,50 m (0,75 m por panel).</p><p className="text-sm">Con película de seguridad se descuenta solo película. En las nuevas ventas, el material se descuenta únicamente cuando el instalador confirma los metros reales cortados. Guardar la venta no consume existencias.</p><p className="text-sm">El control comienza con la carga inicial. Las instalaciones anteriores no descuentan material retroactivamente.</p></div>
    <label className="block">Material<select value={material} onChange={e=>setMaterial(e.target.value)} className="ml-3 border rounded-md p-2"><option value="todos">Todos</option><option value="polarizado">Polarizado</option><option value="pelicula_seguridad">Película de seguridad</option></select></label>
    {loading&&<p role="status">Consultando existencias…</p>}
    {error&&<p role="alert" className="text-red-700">{error}</p>}
    {!loading&&!error&&data&&<>
    <section className="bg-white p-5 rounded-lg overflow-x-auto"><h3 className="font-semibold mb-3">Material disponible</h3><table className="min-w-full text-sm"><thead><tr>{['Tecnología','Opacidad','Material','Inicial','Consumido','Disponible'].map(t=><th key={t} className="text-left p-3">{t}</th>)}</tr></thead><tbody>{items.map(i=><tr key={i.sku} className="border-t"><td className="p-3">{i.tecnologia}</td><td>{i.opacidad_id} %</td><td>{i.material==='polarizado'?'Polarizado':'Película de seguridad'}</td><td>{metros(200)}</td><td>{metros(200-i.disponible_m)}</td><td className="font-bold">{metros(i.disponible_m)}</td></tr>)}</tbody></table></section>
    <section className="bg-white rounded-lg p-5 overflow-x-auto"><h3 className="font-semibold mb-3">Últimos 100 movimientos</h3><table className="min-w-full text-sm"><thead><tr>{['Fecha','Instalación / motivo','Tecnología y opacidad','Material','Movimiento'].map(t=><th key={t} className="p-3 text-left">{t}</th>)}</tr></thead><tbody>{data.movimientos.filter(m=>material==='todos'||data.items.find(i=>i.sku===m.sku)?.material===material).map(m=>{const i=data.items.find(i=>i.sku===m.sku);return <tr key={m.id} className="border-t"><td className="p-3">{new Date(m.created_at).toLocaleString('es-CO',{timeZone:'America/Bogota'})}</td><td>{m.instalacion_id?`SP${m.instalacion_id}`:m.motivo}</td><td>{i?.tecnologia} · {i?.opacidad_id} %</td><td>{i?.material==='polarizado'?'Polarizado':'Película de seguridad'}</td><td className="font-semibold">{m.cantidad_cm>0?'+':''}{metros(m.cantidad_cm/100)}</td></tr>})}</tbody></table></section>
    </>}
  </div>
}
