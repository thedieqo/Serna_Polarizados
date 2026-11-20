import type { RegistroInstalacionPreview } from '../types/instalacion'

// La vista previa incluye la comprobación actual del servidor.
export function motivoBloqueoGuardado(
  preview: Pick<RegistroInstalacionPreview, 'guardado_habilitado' | 'motivos'> | null,
  generando: boolean,
  guardando: boolean,
  guardado: boolean,
): string | null {
  if (guardando) return 'Guardando instalación…'
  if (guardado) return 'Esta instalación ya está guardada.'
  if (generando) return 'Generando y validando el resumen…'
  if (!preview) return 'Genera el resumen antes de guardar. Si cambias datos, vuelve a generarlo.'
  if (!preview.guardado_habilitado) {
    return preview.motivos.join(', ') || 'El servidor no habilitó el guardado. Vuelve a generar el resumen para comprobarlo.'
  }
  return null
}
