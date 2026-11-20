import api from './api';
import type { CatalogosResponse, SchemaStatusResponse } from '../types/catalogos';
import type {
  HistorialResponse,
  InstalacionCreate,
  InstalacionDetalle,
  InstalacionRead,
  RegistroInstalacionCreate,
  RegistroInstalacionPreview,
  RegistroInstalacionResult,
} from '../types/instalacion';

export const instalacionesService = {
  getCatalogos: async (): Promise<CatalogosResponse> => {
    const response = await api.get<CatalogosResponse>('/instalaciones/catalogos');
    return response.data;
  },
  getSchemaStatus: async (): Promise<SchemaStatusResponse> => {
    const response = await api.get<SchemaStatusResponse>('/instalaciones/schema-status');
    return response.data;
  },
  preview: async (data: RegistroInstalacionCreate): Promise<RegistroInstalacionPreview> => {
    const response = await api.post<RegistroInstalacionPreview>('/instalaciones/preview', data);
    return response.data;
  },
  registrar: async (data: RegistroInstalacionCreate): Promise<RegistroInstalacionResult> => {
    const response = await api.post<RegistroInstalacionResult>('/instalaciones/registro', data);
    return response.data;
  },
  create: async (data: InstalacionCreate): Promise<InstalacionRead> => {
    const response = await api.post<InstalacionRead>('/instalaciones/', data);
    return response.data;
  },
  getAll: async (skip = 0, limit = 100, vehiculoId?: number): Promise<InstalacionRead[]> => {
    const params: any = { skip, limit };
    if (vehiculoId !== undefined && vehiculoId !== null) {
      params.vehiculo_id = vehiculoId;
    }
    const response = await api.get<InstalacionRead[]>('/instalaciones/', { params });
    return response.data;
  },
  getById: async (id: number): Promise<InstalacionRead> => {
    const response = await api.get<InstalacionRead>(`/instalaciones/${id}`);
    return response.data;
  },
  getHistorial: async (q: string, skip: number, limit: number): Promise<HistorialResponse> => {
    const response = await api.get<HistorialResponse>('/instalaciones/historial', {
      params: { q: q || undefined, skip, limit },
    });
    return response.data;
  },
  getDetalle: async (id: number): Promise<InstalacionDetalle> => {
    const response = await api.get<InstalacionDetalle>(`/instalaciones/${id}/detalle`);
    return response.data;
  },
};

export default instalacionesService;
