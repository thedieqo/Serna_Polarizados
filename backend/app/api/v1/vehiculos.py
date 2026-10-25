"""
Endpoints API v1 para Vehiculos - T-005
=======================================

Conceptos para aprender:
- FastAPI Router: Agrupa endpoints relacionados
- Depends: Inyección de dependencias (sesión de BD)
- HTTPException: Manejo de errores HTTP
- Status Codes: 200 OK, 201 Created, 404 Not Found, 409 Conflict, 400 Bad Request
- Response Model: Define qué esquema se devuelve

No se instalan dependencias ni se ejecutan migraciones en esta tarea.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.db.session import get_db
from app.schemas.vehiculo import VehiculoCreate, VehiculoRead
from app import crud

router = APIRouter(prefix="/vehiculos", tags=["Vehiculos"])


@router.post("/", response_model=VehiculoRead, status_code=status.HTTP_201_CREATED)
def create_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo vehículo

    Explicación sencilla:
    - Valida datos con VehiculoCreate
    - Verifica que el cliente exista
    - Verifica placa duplicada
    - Crea vehículo asociado a cliente
    """
    # Verificar si ya existe un vehículo con esa placa
    db_vehiculo = crud.vehiculo.get_vehiculo_by_placa(db, placa=vehiculo.placa)
    if db_vehiculo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe a vehículo with esa placa",
        )

    try:
        return crud.vehiculo.create_vehiculo(db=db, vehiculo=vehiculo)
    except ValueError as e:
        if str(e) == "Cliente no existe":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El cliente asociado no existe",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error en los datos del vehículo",
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe a vehículo with esa placa",
        )


@router.get("/", response_model=List[VehiculoRead])
def read_vehiculos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista of vehículos

    Explicación sencilla: Lista con paginación básica
    """
    vehiculos = crud.vehiculo.get_vehiculos(db, skip=skip, limit=limit)
    return vehiculos


@router.get("/{vehiculo_id}", response_model=VehiculoRead)
def read_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    """
    Obtener a vehículo por ID
    Explicación sencilla: Busca vehículo por clave primaria
    """
    db_vehiculo = crud.vehiculo.get_vehiculo(db, vehiculo_id=vehiculo_id)
    if db_vehiculo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado",
        )
    return db_vehiculo


@router.get("/by-placa/{placa}", response_model=VehiculoRead)
def read_vehiculo_by_placa(placa: str, db: Session = Depends(get_db)):
    """
    Obtener a vehículo por placa
    Explicación sencilla: Útil for búsquedas por placa (RF-03)
    """
    db_vehiculo = crud.vehiculo.get_vehiculo_by_placa(db, placa=placa)
    if db_vehiculo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado",
        )
    return db_vehiculo


@router.get("/by-cliente/{cliente_id}", response_model=List[VehiculoRead])
def read_vehiculos_by_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtener vehículos de a cliente
    Explicación sencilla: Útil for HU-03 (un cliente puede tener varios vehículos)
    """
    vehiculos = crud.vehiculo.get_vehiculos_by_cliente(db, cliente_id=cliente_id)
    return vehiculos
