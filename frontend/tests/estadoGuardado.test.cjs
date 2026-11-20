const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const ts = require('typescript')
const vm = require('node:vm')
const path = require('node:path')
const source = fs.readFileSync(path.join(__dirname, '../src/lib/estadoGuardado.ts'), 'utf8')
const compiled = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.CommonJS } }).outputText
const context = { exports: {} }
vm.runInNewContext(compiled, context)
const { motivoBloqueoGuardado: motivo } = context.exports
const enabled = { guardado_habilitado: true, motivos: [] }

test('una validación nueva habilita guardar sin depender de una consulta inicial', () => {
  assert.ok(motivo(null, false, false, false))
  assert.equal(motivo(enabled, false, false, false), null)
})
test('el bloqueo actual del servidor se respeta y explica', () => {
  assert.equal(motivo({ guardado_habilitado: false, motivos: ['Escritura deshabilitada'] }, false, false, false), 'Escritura deshabilitada')
})
test('una nueva vista previa permite recuperarse de un bloqueo anterior', () => {
  assert.ok(motivo({ guardado_habilitado: false, motivos: [] }, false, false, false))
  assert.equal(motivo(enabled, false, false, false), null)
})
test('bloquea el guardado durante peticiones y después de guardar', () => {
  assert.ok(motivo(enabled, true, false, false))
  assert.ok(motivo(enabled, false, true, false))
  assert.ok(motivo(enabled, false, false, true))
})
test('editar e invalidar el resumen requiere validación nueva', () => {
  assert.equal(motivo(enabled, false, false, false), null)
  assert.ok(motivo(null, false, false, false))
})
