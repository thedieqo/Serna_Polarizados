"""
Endpoints API v1 para Instalaciones - T-008.2.6
===============================================

Endpoints para gestión de instalaciones
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas.instalacion import InstalacionCreate, InstalacionRead
from app import crud

router = APIRouter(prefix="/instalaciones", tags=["Instalaciones"])


@router.post("/", response_model=InstalacionRead, status_code=status.HTTP_201_CREATED)
def create_instalacion(instalacion: InstalacionCreate, db: Session = Depends(get_db)):
    try:
        return crud.instalacion.create_instalacion(db=db, instalacion=instalacion)
    except ValueError as e:
        if str(e) == "Vehículo no existe":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El vehículo asociado no existe",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error en los datos de la instalación",
        )


@router.get("/", response_model=List[InstalacionRead])
def read_instalaciones(
    skip: int = 0,
    limit: int = 100,
    vehiculo_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if vehiculo_id is not None:
        return crud.instalacion.get_instalaciones_by_vehiculo(db, vehiculo_id=vehiculo_id)
    return crud.instalacion.get_instalaciones(db, skip=skip, limit=limit)


@router.get("/{instalacion_id}", response_model=InstalacionRead)
def read_instalacion(instalacion_id: int, db: Session = Depends(get_db)):
    db_instalacion = crud.instalacion.get_instalacion(db, instalacion_id=instalacion_id)
    if db_instalacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instalación no encontrada",
        )
    return db_instalacion
