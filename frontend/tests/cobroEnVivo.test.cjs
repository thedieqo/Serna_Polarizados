const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const ts = require('typescript')
const vm = require('node:vm')
const path = require('node:path')
const compiled = ts.transpileModule(fs.readFileSync(path.join(__dirname, '../src/lib/cobroEnVivo.ts'), 'utf8'), { compilerOptions: { module: ts.ModuleKind.CommonJS } }).outputText
const context = { exports: {} }; vm.runInNewContext(compiled, context)
const { cobroEnVivo } = context.exports
const tarifas = { tecnologias: [{id:'prueba', precio_seccion_cop:1000000}], incremento_seguridad_laterales_cop:100000 }
const detalle = (vidrio_id, pelicula_seguridad=false) => ({vidrio_id, tecnologia_id:'prueba', pelicula_seguridad})
test('dos millones menos transferencia y efectivo actualiza saldo sin generar resumen', () => {
 const detalles = [detalle('parabrisas'), detalle('luneta')]
 assert.equal(cobroEnVivo(detalles,tarifas,'ninguno',[1600000]).saldo,400000)
 assert.equal(cobroEnVivo(detalles,tarifas,'ninguno',[1600000,400000]).saldo,0)
 assert.equal(cobroEnVivo(detalles,tarifas,'ninguno',[1600000,500000]).saldo,-100000)
 assert.equal(cobroEnVivo(detalles,tarifas,'ninguno',[]).saldo,2000000)
})
test('descuentos excluyentes y película sobre el subtotal', () => {
 const detalles=[detalle('cuatro_laterales',true)]
 for (const [tipo, descuento] of [['referido',110000],['agenda',220000],['especial',330000]]) {
  const r=cobroEnVivo(detalles,tarifas,tipo,[])
  assert.equal(r.subtotal,2200000);assert.equal(r.descuento,descuento)
  assert.equal(r.total,2200000-descuento)
 }
})
test('sin catálogo o tecnología no presenta total como confirmado', () => {
 assert.equal(cobroEnVivo([detalle('parabrisas')],undefined,'ninguno',[]).completo,false)
 assert.equal(cobroEnVivo([{vidrio_id:'parabrisas', tecnologia_id:''}],tarifas,'ninguno',[]).completo,false)
})
