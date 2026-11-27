import CobroResumen from './CobroResumen'
import type {InstalacionDetalle} from '../types/instalacion'
function formatearFecha(fecha: string): string {
  try {
    return new Date(fecha).toLocaleString()
  } catch {
    return fecha
  }
}

function formatearCOP(valor: number | null | undefined): string {
  if (valor === null || valor === undefined) return 'Precio pendiente de definir'
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(valor)
}

function lista(valores: string[]): string {
  return valores.length ? valores.join(', ') : 'No disponible en el registro histórico'
}

export default function DetalleInstalacion({detalle,onClose}:{detalle:InstalacionDetalle;onClose:()=>void}){return (
        <div className="border-t border-gray-200 p-4 bg-slate-50">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Detalle de instalación SP{detalle.id}</h3>
              <p className="text-sm text-gray-500 mt-1">
                {detalle.cliente_nombre} · {detalle.cliente_documento} · {detalle.vehiculo_placa}
              </p>
            </div>
            <button
              type="button"
              onClick={onClose}
              className="text-sm text-blue-700 hover:text-blue-900"
            >
              Cerrar
            </button>
          </div>

          <dl className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div><dt className="font-medium text-gray-700">Nombre del propietario</dt><dd>{detalle.cliente_nombre}</dd></div>
            <div><dt className="font-medium text-gray-700">Cédula</dt><dd>{detalle.cliente_documento}</dd></div>
            <div><dt className="font-medium text-gray-700">Placa</dt><dd>{detalle.vehiculo_placa}</dd></div>
            <div><dt className="font-medium text-gray-700">Correo electrónico</dt><dd>{detalle.cliente_email || 'No registrado'}</dd></div>
            <div><dt className="font-medium text-gray-700">Teléfono</dt><dd>{detalle.cliente_telefono || 'No registrado'}</dd></div>
            <div><dt className="font-medium text-gray-700">Descripción / color</dt><dd>{detalle.vehiculo_descripcion || 'No registrado'}</dd></div>
            <div><dt className="font-medium text-gray-700">Tipo de factura</dt><dd>{detalle.tipo_factura === 'electronica' ? 'Electrónica' : detalle.tipo_factura === 'normal' ? 'Normal' : 'No registrado'}</dd></div>
            <div><dt className="font-medium text-gray-700">Servicio instalado</dt><dd>{({ polarizado: 'Polarizado', pelicula_seguridad: 'Película de seguridad', ambos: 'Polarizado y película de seguridad' } as Record<string, string>)[detalle.tipo_servicio] || detalle.tipo_servicio}</dd></div>
            <div><dt className="font-medium text-gray-700">Valor de la instalación</dt><dd>{detalle.precio_total_cop != null ? formatearCOP(detalle.precio_total_cop) : detalle.desglose_precios ? detalle.desglose_precios.etiqueta_total : 'No registrado en esta instalación histórica'}</dd></div>
            <div><dt className="font-medium text-gray-700">Fecha</dt><dd>{formatearFecha(detalle.fecha)}</dd></div>
            <div><dt className="font-medium text-gray-700">Vehículo</dt><dd>{detalle.vehiculo_marca || 'Marca no registrada'}</dd></div>
            <div><dt className="font-medium text-gray-700">Vidrios</dt><dd>{lista(detalle.vidrios)}</dd></div>
            <div><dt className="font-medium text-gray-700">Tecnologías</dt><dd>{lista(detalle.tecnologias)}</dd></div>
            <div><dt className="font-medium text-gray-700">Opacidades</dt><dd>{lista(detalle.opacidades)}</dd></div>
            <div><dt className="font-medium text-gray-700">Instaladores</dt><dd>{lista(detalle.instaladores)}</dd></div>
            <div><dt className="font-medium text-gray-700">Retiro de material</dt><dd>{detalle.retiro_material_anterior ? 'Sí' : 'No'}</dd></div>
            <div><dt className="font-medium text-gray-700">Observaciones</dt><dd>{detalle.observaciones || '-'}</dd></div>
          </dl>

          <div className="mt-4">
            <h4 className="text-sm font-semibold text-gray-900">Detalles de la instalación por vidrio</h4>
            {detalle.detalles_vidrios?.length ? (
              <div className="overflow-x-auto mt-2">
                <table className="min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-gray-50"><tr>
                    {['Vidrio', 'Panel', 'Tecnología instalada', 'Opacidad', 'Instalador'].map(label => <th key={label} className="px-3 py-2 text-left font-medium text-gray-600">{label}</th>)}
                  </tr></thead>
                  <tbody className="divide-y divide-gray-200">
                    {detalle.detalles_vidrios.map((vidrio, indice) => (
                      <tr key={indice}>
                        <td className="px-3 py-2">{vidrio.vidrio || 'No registrado'}</td>
                        <td className="px-3 py-2">{vidrio.panel || '—'}</td>
                        <td className="px-3 py-2">{vidrio.tecnologia || 'No registrada'}</td>
                        <td className="px-3 py-2">{vidrio.opacidad ? (vidrio.opacidad.includes('%') ? vidrio.opacidad : `${vidrio.opacidad} %`) : 'No registrada'}</td>
                        <td className="px-3 py-2">{vidrio.instaladores.join(', ') || 'Sin asignación por vidrio registrada'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : <p className="mt-2 text-sm text-gray-600">Sin desglose por vidrio en este registro.</p>}
          </div>

          {detalle.referido && <section className="mt-4 rounded-lg border border-gray-300 p-4"><h4 className="font-semibold">Descuento de referidos · 5 %</h4><p className="text-sm mt-2">Código: {detalle.referido.placa} · {detalle.referido.disponible ? 'Disponible' : 'No disponible'}</p><p className="text-sm mt-1">{detalle.referido.motivo}</p></section>}
          <CobroResumen desglose={detalle.desglose_precios} />
          <div className="mt-4">
            <h4 className="text-sm font-semibold text-gray-900">Desglose de precios</h4>
            {detalle.desglose_precios ? (
              <>
                <table className="mt-2 min-w-full divide-y divide-gray-200 text-sm">
                  <thead className="bg-white">
                    <tr>
                      <th className="px-3 py-2 text-left font-medium text-gray-600">Concepto</th>
                      <th className="px-3 py-2 text-left font-medium text-gray-600">Detalle</th>
                      <th className="px-3 py-2 text-left font-medium text-gray-600">Importe</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 bg-white">
                    {detalle.desglose_precios.conceptos.map((concepto, indice) => (
                      <tr key={indice}>
                        <td className="px-3 py-2">{concepto.concepto}</td>
                        <td className="px-3 py-2">{concepto.detalle}</td>
                        <td className="px-3 py-2">{formatearCOP(concepto.importe_cop)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <p className="mt-2 text-sm font-semibold text-gray-900">
                  {detalle.desglose_precios.total_cop === null
                    ? detalle.desglose_precios.etiqueta_total
                    : `${detalle.desglose_precios.etiqueta_total}: ${formatearCOP(detalle.desglose_precios.total_cop)}`}
                </p>
              </>
            ) : (
              <p className="mt-2 text-sm text-gray-600">
                Sin información de precios en el registro histórico.
              </p>
            )}
          </div>
        </div>)}
