export interface CatalogoItem {
  id: string;
  label: string;
  paneles?: string[];
}

export interface TarifaTecnologia {
  id: string;
  label: string;
  precio_seccion_cop: number;
}

export interface TarifasResponse {
  moneda: 'COP';
  version: string;
  tecnologias: TarifaTecnologia[];
  incremento_seguridad_laterales_cop: number;
  incremento_seguridad_laterales_unidad: string;
  reglas_pendientes: string[];
}

export interface CatalogosResponse {
  servicio: string;
  tecnologias: CatalogoItem[];
  opacidades: CatalogoItem[];
  instaladores: CatalogoItem[];
  tipos_factura: CatalogoItem[];
  vidrios: CatalogoItem[];
  tarifas: TarifasResponse;
}

export interface SchemaStatusResponse {
  save_enabled: boolean;
  write_enabled: boolean;
  schema_ready: boolean;
  missing_requirements: string[];
  admin_emails_configured: boolean;
  auth_ready: boolean;
  reasons: string[];
}
