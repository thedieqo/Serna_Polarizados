import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import type { Session } from '@supabase/supabase-js'

import api from '../services/api'
import { supabase, supabaseConfigured } from '../lib/supabase'

type SessionStatus = {
  rol: string | null
  authenticated: boolean
  email: string
  email_verified: boolean
  authorized: boolean
  authorization_code: string | null
}

type AuthContextValue = {
  rol: string | null
  loading: boolean
  configured: boolean
  session: Session | null
  email: string | null
  authorized: boolean
  error: string | null
  signIn: () => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

function describeError(error: unknown): string {
  const detail = (error as { detail?: unknown })?.detail
  if (typeof detail === 'string') return detail
  if (detail && typeof detail === 'object') {
    const code = (detail as { code?: unknown }).code
      if (typeof code === 'string') return code.replace(/_/g, ' ').toLowerCase()
  }
  return 'No fue posible verificar la sesión'
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [rol, setRol] = useState<string|null>(null)
  const [loading, setLoading] = useState(true)
  const [session, setSession] = useState<Session | null>(null)
  const [email, setEmail] = useState<string | null>(null)
  const [authorized, setAuthorized] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const statusInFlight = useRef(false)

  const loadStatus = useCallback(async () => {
    if (statusInFlight.current) return
    statusInFlight.current = true
    try {
      const { data } = await api.get<SessionStatus>('/auth/session')
      setEmail(data.email)
      setAuthorized(data.authorized && Boolean(data.rol))
      setRol(data.rol)
      setError(data.authorized ? null : (data.authorization_code || 'USUARIO_NO_AUTORIZADO'))
    } catch (err) {
      setAuthorized(false)
      setError(describeError(err))
    } finally {
      statusInFlight.current = false
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (!supabase) {
      setError('Faltan VITE_SUPABASE_URL o VITE_SUPABASE_PUBLISHABLE_KEY')
      setLoading(false)
      return
    }

    let active = true
    const client = supabase

    const initialize = async () => {
      const { data } = await client.auth.getSession()
      if (!active) return
      setSession(data.session)
      if (data.session) {
        await loadStatus()
      } else {
        setLoading(false)
      }
    }

    void initialize()

    const { data } = client.auth.onAuthStateChange((_event, nextSession) => {
      if (!active) return
      setSession(nextSession)
      if (!nextSession) {
        setEmail(null)
        setAuthorized(false)
        setLoading(false)
        setError(null)
        return
      }
      void loadStatus()
    })

    const handleExpired = () => {
      setAuthorized(false)
      setSession(null)
      setError('La sesión expiró. Inicia sesión nuevamente.')
    }
    window.addEventListener('auth:expired', handleExpired)

    return () => {
      active = false
      data.subscription.unsubscribe()
      window.removeEventListener('auth:expired', handleExpired)
    }
  }, [loadStatus])

  const signIn = useCallback(async () => {
    if (!supabase) return
    setError(null)
    const { error: signInError } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: `${window.location.origin}/` },
    })
    if (signInError) {
      setError(signInError.message)
    }
  }, [])

  const signOut = useCallback(async () => {
    if (!supabase) return
    await supabase.auth.signOut()
    setSession(null)
    setEmail(null)
    setAuthorized(false)
  }, [])

  const value = useMemo(
    () => ({
      loading,
      configured: supabaseConfigured,
      rol,
      session,
      email,
      authorized,
      error,
      signIn,
      signOut,
    }),
    [loading, session, email, authorized, error, signIn, signOut, rol]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth debe usarse dentro de AuthProvider')
  return context
}
