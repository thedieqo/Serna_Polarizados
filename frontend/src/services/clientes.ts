import api from './api';
import type { ClienteCreate, ClienteRead } from '../types/cliente';

export const clientesService = {
  create: async (data: ClienteCreate): Promise<ClienteRead> => {
    const response = await api.post<ClienteRead>('/clientes/', data);
    return response.data;
  },
  getAll: async (skip = 0, limit = 100): Promise<ClienteRead[]> => {
    const response = await api.get<ClienteRead[]>('/clientes/', { params: { skip, limit } });
    return response.data;
  },
  getById: async (id: number): Promise<ClienteRead> => {
    const response = await api.get<ClienteRead>(`/clientes/${id}`);
    return response.data;
  },
  getByDocumento: async (documento: string): Promise<ClienteRead> => {
    const response = await api.get<ClienteRead>(`/clientes/by-documento/${documento}`);
    return response.data;
  },
};

export default clientesService;
