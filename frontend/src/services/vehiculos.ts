import api from './api';
import type { VehiculoCreate, VehiculoRead } from '../types/vehiculo';

export const vehiculosService = {
  create: async (data: VehiculoCreate): Promise<VehiculoRead> => {
    const response = await api.post<VehiculoRead>('/vehiculos/', data);
    return response.data;
  },
  getAll: async (skip = 0, limit = 100): Promise<VehiculoRead[]> => {
    const response = await api.get<VehiculoRead[]>('/vehiculos/', { params: { skip, limit } });
    return response.data;
  },
  getById: async (id: number): Promise<VehiculoRead> => {
    const response = await api.get<VehiculoRead>(`/vehiculos/${id}`);
    return response.data;
  },
  getByPlaca: async (placa: string): Promise<VehiculoRead> => {
    const response = await api.get<VehiculoRead>(`/vehiculos/by-placa/${placa}`);
    return response.data;
  },
  getByCliente: async (clienteId: number): Promise<VehiculoRead[]> => {
    const response = await api.get<VehiculoRead[]>(`/vehiculos/by-cliente/${clienteId}`);
    return response.data;
  },
};

export default vehiculosService;
