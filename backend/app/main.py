"""
Punto de entrada FastAPI - T-005
================================

Conceptos para aprender:
- FastAPI: Framework para crear APIs REST
- Router: Agrupa endpoints relacionados
- include_router: Registra routers en la aplicación

No se ejecutan servidores ni se instalan dependencias en esta tarea.
"""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, clientes, instalaciones, vehiculos
from app.core.auth import require_admin_identity
from app.core.config import settings

app = FastAPI(
    title="Serna Polarizados API",
    description="Sistema de gestión de instalaciones, clientes, vehículos e inventario",
    version="0.3.1",
)

# Configuración CORS para permitir frontend local
origins = [
    origin.strip()
    for origin in settings.FRONTEND_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
@app.get("/health")
def root():
    """
    Comprobación de salud sin datos personales.
    """
    return {"status": "ok", "service": "Serna Polarizados API"}


# La sesión solo devuelve la identidad propia; el resto de rutas exige administrador verificado.
app.include_router(auth.router, prefix="/api/v1")
protegido = [Depends(require_admin_identity)]
app.include_router(clientes.router, prefix="/api/v1", dependencies=protegido)
app.include_router(vehiculos.router, prefix="/api/v1", dependencies=protegido)
app.include_router(instalaciones.router, prefix="/api/v1", dependencies=protegido)
