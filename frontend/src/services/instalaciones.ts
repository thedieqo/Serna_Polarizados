import api from './api';
import type { InstalacionCreate, InstalacionRead } from '../types/instalacion';

export const instalacionesService = {
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
};

export default instalacionesService;
