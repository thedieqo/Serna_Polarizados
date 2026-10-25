export interface VehiculoBase {
  placa: string;
  descripcion?: string | null;
}

export interface VehiculoCreate extends VehiculoBase {
  cliente_id: number;
}

export interface VehiculoRead extends VehiculoBase {
  id: number;
  cliente_id: number;
}

export type Vehiculo = VehiculoRead;
