import type { DetalleVidrioInput } from '../types/instalacion'
import type { TarifasResponse } from '../types/catalogos'

export function cobroEnVivo(detalles: DetalleVidrioInput[], tarifas: TarifasResponse | undefined, tipo: string, montos: number[]) {
  let subtotal = 0
  let completo = !!tarifas && detalles.length > 0
  for (const d of detalles) {
    const precio = tarifas?.tecnologias.find(t => t.id === d.tecnologia_id)?.precio_seccion_cop
    if (precio == null || !d.vidrio_id) { completo = false; continue }
    const pares = d.vidrio_id === 'cuatro_laterales' ? 2 : 1
    subtotal += precio * pares + (d.pelicula_seguridad ? (tarifas?.incremento_seguridad_laterales_cop || 0) * pares : 0)
  }
  const porcentaje = ({ referido: 5, agenda: 10, especial: 15 } as Record<string, number>)[tipo] || 0
  const descuento = Math.round(subtotal * porcentaje / 100)
  const total = subtotal - descuento
  const pagado = montos.reduce((sum, n) => sum + (Number.isFinite(n) ? n : 0), 0)
  return { completo, subtotal, descuento, total, pagado, saldo: total - pagado }
}
