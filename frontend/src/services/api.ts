import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      return Promise.reject(error.response.data || error);
    } else if (error.request) {
      return Promise.reject({ detail: 'Error de conexión con el servidor' });
    } else {
      return Promise.reject({ detail: error.message });
    }
  }
);

export default api;
export { API_BASE_URL };
