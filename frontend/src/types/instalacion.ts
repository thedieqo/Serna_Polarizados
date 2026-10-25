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
