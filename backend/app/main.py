"""
Punto de entrada FastAPI - T-005
================================

Conceptos para aprender:
- FastAPI: Framework para crear APIs REST
- Router: Agrupa endpoints relacionados
- include_router: Registra routers en la aplicación

No se ejecutan servidores ni se instalan dependencias en esta tarea.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import clientes, vehiculos, instalaciones

app = FastAPI(
    title="Serna Polarizados API",
    description="Sistema de gestión de instalaciones, clientes, vehículos e inventario",
    version="0.1.0",
)

# Configuración CORS para permitir frontend local
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def root():
    """
    Endpoint raíz para verificar que la API está configurada
    Explicación sencilla: Ruta de prueba
    """
    return {"message": "Serna Polarizados API - T-005"}


# Registrar routers
app.include_router(clientes.router, prefix="/api/v1")
app.include_router(vehiculos.router, prefix="/api/v1")
app.include_router(instalaciones.router, prefix="/api/v1")
