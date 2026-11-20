export interface InstalacionBase {
  tipo_servicio: 'polarizado' | 'pelicula_seguridad' | 'ambos';
  opacidad?: string | null;
  zonas: Array<Record<string, any>>;
  asignaciones_instaladores: Array<Record<string, any>>;
  retiro_material_anterior: boolean;
  observaciones?: string | null;
  estado: 'programado' | 'en_proceso' | 'finalizado' | 'anulado';
}

export interface InstalacionCreate extends InstalacionBase {
  vehiculo_id: number;
  fecha?: string | null;
}

export interface InstalacionRead extends InstalacionBase {
  id: number;
  vehiculo_id: number;
  fecha: string;
  created_at: string;
  updated_at?: string | null;
}

export type Instalacion = InstalacionRead;

export interface RegistroClienteInput {
  documento: string;
  nombre: string;
  contacto?: string | null;
  telefono?: string | null;
  email?: string | null;
}

export interface RegistroVehiculoInput {
  vehiculo_id?: number | null;
  placa: string;
  marca: string;
  descripcion?: string | null;
}

export interface DetalleVidrioInput {
  vidrio_id: string;
  panel?: string | null;
  tecnologia_id: string;
  opacidad_id: string;
  instalador_id: string;
}

export interface RegistroInstalacionCreate {
  cliente: RegistroClienteInput;
  vehiculo: RegistroVehiculoInput;
  tipo_factura: string;
  fecha?: string | null;
  retiro_material_anterior?: boolean;
  observaciones?: string | null;
  estado?: 'programado';
  detalles: DetalleVidrioInput[];
}

export interface DesgloseConcepto {
  concepto: string;
  detalle: string;
  secciones: number | null;
  tarifa_unitaria_cop: number | null;
  importe_cop: number | null;
  estado: 'definido' | 'pendiente';
  motivo_pendiente: string | null;
}

export interface DesglosePrecios {
  moneda: 'COP';
  version: string;
  estado: 'definido' | 'pendiente';
  total_cop: number | null;
  etiqueta_total: string;
  conceptos: DesgloseConcepto[];
}

export interface RegistroVidrioResumen {
  vidrio: string;
  panel?: string | null;
  tecnologia: string;
  opacidad: string;
  instalador: string;
}

export interface RegistroInstalacionPreview {
  cliente: Record<string, string | null>;
  vehiculo: Record<string, string | null>;
  tipo_factura: string;
  cantidad_vidrios: number;
  tecnologias_utilizadas: string[];
  detalles: RegistroVidrioResumen[];
  desglose: DesglosePrecios;
  guardado_habilitado: boolean;
  motivos: string[];
}

export interface RegistroInstalacionResult {
  instalacion_id: number;
  cliente_id: number;
  vehiculo_id: number;
  cliente_reutilizado: boolean;
  vehiculo_reutilizado: boolean;
  detalles_guardados: number;
}

export interface HistorialInstalacion {
  id: number;
  fecha: string;
  estado: string;
  tipo_servicio: string;
  cliente_documento: string;
  cliente_nombre: string;
  vehiculo_placa: string;
  vehiculo_marca?: string | null;
  vehiculo_descripcion?: string | null;
}

export interface HistorialResponse {
  items: HistorialInstalacion[];
  total: number;
  skip: number;
  limit: number;
  q?: string | null;
}

export interface InstalacionDetalle extends HistorialInstalacion {
  retiro_material_anterior: boolean;
  observaciones?: string | null;
  tecnologias: string[];
  vidrios: string[];
  opacidades: string[];
  instaladores: string[];
  desglose_precios?: DesglosePrecios | null;
  tarifas_aplicadas?: Record<string, unknown> | null;
  moneda?: string | null;
  precio_estado?: string | null;
  precio_total_cop?: number | null;
}
