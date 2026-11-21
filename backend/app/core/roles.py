"""Perfiles autorizados por servidor. Cuenta temporal explícita para pruebas."""
from app.core.sedes import SEDES, permitidas
ROLES = ('gerencia','propietario','administrador','instalador')
CUENTA_PRUEBAS = 'diegonangumaw@gmail.com'

def roles_permitidos(email, settings):
    if email.lower() == CUENTA_PRUEBAS:
        return list(ROLES)
    return ['administrador'] if permitidas(email, settings) else []

def sedes_perfil(email, rol, settings):
    if rol not in roles_permitidos(email, settings): return []
    if rol in ('gerencia','propietario'): return list(SEDES)
    return permitidas(email, settings)


def puede_usar_ruta(rol, metodo, ruta):
    if rol == 'gerencia': return True
    if rol == 'propietario':
        return metodo == 'GET' and ruta == '/api/v1/instalaciones/ventas/resumen'
    if rol == 'instalador':
        return metodo == 'GET' and ruta == '/api/v1/mi-trabajo'
    if rol == 'administrador':
        # Operaciones actuales de registro/consulta de su sede; no habilita gestión de cuentas.
        return ruta != '/api/v1/instalaciones/ventas/resumen' and ruta.startswith(('/api/v1/instalaciones','/api/v1/clientes','/api/v1/vehiculos','/api/v1/inventario'))
    return False
