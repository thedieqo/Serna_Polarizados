import InstalacionList from '../components/InstalacionList'

export default function InstalacionesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900">Registro de instalaciones</h2>
        <p className="text-sm text-gray-500 mt-1">Historial y consulta de instalaciones.</p>
      </div>

      <div className="bg-white shadow rounded-lg overflow-hidden">
        <InstalacionList />
      </div>
    </div>
  )
}
