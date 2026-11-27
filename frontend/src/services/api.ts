import axios, { type InternalAxiosRequestConfig } from 'axios'

import { supabase } from '../lib/supabase'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

type AuthRetryConfig = InternalAxiosRequestConfig & { _authRetried?: boolean }

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

api.interceptors.request.use(async (config) => {
  config.headers['X-Rol'] ??= sessionStorage.getItem('serna-rol') || ''
  config.headers['X-Sede'] ??= sessionStorage.getItem('serna-sede') || ''
  if (supabase) {
    const { data } = await supabase.auth.getSession()
    if (data.session?.access_token) {
      config.headers.Authorization = `Bearer ${data.session.access_token}`
    }
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config as AuthRetryConfig | undefined
    const detail = error.response?.data?.detail
    const code = detail && typeof detail === 'object' ? detail.code : undefined
    if (
      error.response?.status === 401 &&
      code === 'TOKEN_EXPIRADO' &&
      original &&
      !original._authRetried &&
      supabase
    ) {
      original._authRetried = true
      const { data, error: refreshError } = await supabase.auth.refreshSession()
      if (!refreshError && data.session?.access_token) {
        original.headers.Authorization = `Bearer ${data.session.access_token}`
        return api(original)
      }
      window.dispatchEvent(new Event('auth:expired'))
    }
    if (error.response) {
      return Promise.reject(error.response.data || error)
    }
    if (error.request) {
      return Promise.reject({ detail: 'Error de conexión con el servidor' })
    }
    return Promise.reject({ detail: error.message })
  }
)

export default api
export { API_BASE_URL }
