import { useAuth } from '../context/AuthContext'

export default function LoginScreen() {
  const { loading, configured, session, email, authorized, error, signIn, signOut } = useAuth()

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white border border-slate-200 shadow-sm rounded-lg p-8">
        <div className="flex items-center gap-3 mb-6">
          <img src="/serna-logo.jpg" alt="Logotipo Serna Polarizados" className="h-10 w-10 rounded-lg object-contain shrink-0" />
          <div>
            <h1 className="text-xl font-bold text-slate-900">Serna Polarizados</h1>
            <p className="text-xs text-slate-500">Acceso de administradores</p>
          </div>
        </div>

        {loading ? (
          <p className="text-sm text-slate-600">Verificando sesión…</p>
        ) : (
          <>
            {!configured && (
              <div className="mb-4 rounded-md border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900">
                Configura VITE_SUPABASE_URL y VITE_SUPABASE_PUBLISHABLE_KEY para habilitar el acceso.
              </div>
            )}

            {session && !authorized && (
              <div className="mb-4 rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-900">
                <p className="font-semibold">Acceso denegado</p>
                <p className="mt-1">
                  {email || 'Tu cuenta'} no tiene autorización para este sistema.
                </p>
              </div>
            )}

            {error && (
              <div className="mb-4 rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-900">
                {error}
              </div>
            )}

            {session ? (
              <div className="space-y-4">
                <p className="text-sm text-slate-600">
                  Sesión activa: <span className="font-medium text-slate-900">{email || 'Cuenta Google'}</span>
                </p>
                <button
                  type="button"
                  onClick={() => void signOut()}
                  className="w-full rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                >
                  Cerrar sesión
                </button>
              </div>
            ) : (
              <button
                type="button"
                onClick={() => void signIn()}
                disabled={!configured}
                className="w-full rounded-md bg-blue-800 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-900 disabled:cursor-not-allowed disabled:bg-slate-400"
              >
                Continuar con Google
              </button>
            )}
          </>
        )}
      </div>
    </div>
  )
}
