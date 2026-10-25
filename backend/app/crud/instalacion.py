"""
CRUD para Instalacion - T-008.2.5
================================

CRUD: Create, Read con filtros por vehículo
"""

from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.instalacion import Instalacion
from app.models.vehiculo import Vehiculo
from app.schemas.instalacion import InstalacionCreate


def get_instalacion(db: Session, instalacion_id: int) -> Optional[Instalacion]:
    """Obtener una instalación por ID"""
    return db.query(Instalacion).filter(Instalacion.id == instalacion_id).first()


def get_instalaciones(db: Session, skip: int = 0, limit: int = 100) -> List[Instalacion]:
    """Obtener lista de instalaciones con paginación"""
    return db.query(Instalacion).offset(skip).limit(limit).all()


def get_instalaciones_by_vehiculo(db: Session, vehiculo_id: int) -> List[Instalacion]:
    """Obtener instalaciones de un vehículo específico"""
    return db.query(Instalacion).filter(Instalacion.vehiculo_id == vehiculo_id).all()


def create_instalacion(db: Session, instalacion: InstalacionCreate) -> Instalacion:
    """Crear una nueva instalación validando que el vehículo exista"""
    db_vehiculo = db.query(Vehiculo).filter(Vehiculo.id == instalacion.vehiculo_id).first()
    if not db_vehiculo:
        raise ValueError("Vehículo no existe")

    db_instalacion = Instalacion(
        vehiculo_id=instalacion.vehiculo_id,
        fecha=instalacion.fecha,
        tipo_servicio=instalacion.tipo_servicio,
        opacidad=instalacion.opacidad,
        zonas=instalacion.zonas,
        asignaciones_instaladores=instalacion.asignaciones_instaladores,
        retiro_material_anterior=instalacion.retiro_material_anterior,
        observaciones=instalacion.observaciones,
        estado=instalacion.estado,
    )
    db.add(db_instalacion)
    db.commit()
    db.refresh(db_instalacion)
    return db_instalacion


__all__ = ["get_instalacion", "get_instalaciones", "get_instalaciones_by_vehiculo", "create_instalacion"]
