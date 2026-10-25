"""
CRUD para Vehiculo - T-005
==========================

Conceptos para aprender:
- CRUD: Create, Read, Update, Delete (solo Create/Read en T-005)
- ForeignKey: Validar que el cliente exista antes de asociar
- IntegrityError: Error al violar restricciones UNIQUE/FOREIGN KEY
- Filtros: Buscar by placa y by cliente_id

No se ejecutan migraciones ni conexiones reales en esta tarea.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.models.vehiculo import Vehiculo
from app.models.cliente import Cliente
from app.schemas.vehiculo import VehiculoCreate


def get_vehiculo(db: Session, vehiculo_id: int) -> Optional[Vehiculo]:
    """
    Obtener un vehículo por ID
    Explicación sencilla: Busca a vehículo por su clave primaria
    """
    return db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()


def get_vehiculo_by_placa(db: Session, placa: str) -> Optional[Vehiculo]:
    """
    Obtener a vehículo por placa
    Explicación sencilla: Útil para validar duplicados y consultas (RF-03)
    """
    return db.query(Vehiculo).filter(Vehiculo.placa == placa).first()


def get_vehiculos(db: Session, skip: int = 0, limit: int = 100) -> List[Vehiculo]:
    """
    Obtener lista of vehículos con paginación básica
    Explicación sencilla: Permite listar vehículos si es necesario
    """
    return db.query(Vehiculo).offset(skip).limit(limit).all()


def get_vehiculos_by_cliente(db: Session, cliente_id: int) -> List[Vehiculo]:
    """
    Obtener vehículos de un cliente específico
    Explicación sencilla: Útil para HU-03 (un cliente puede tener varios vehículos)
    """
    return db.query(Vehiculo).filter(Vehiculo.cliente_id == cliente_id).all()


def create_vehiculo(db: Session, vehiculo: VehiculoCreate) -> Vehiculo:
    """
    Crear un nuevo vehículo
    Explicación sencilla:
    - Valida que el cliente exista antes de crear (requerido)
    - Crea el vehículo asociado al cliente
    - Lanza IntegrityError si hay placa duplicada
    """
    # Validar que el cliente exista
    db_cliente = db.query(Cliente).filter(Cliente.id == vehiculo.cliente_id).first()
    if not db_cliente:
        raise ValueError("Cliente no existe")

    db_vehiculo = Vehiculo(
        placa=vehiculo.placa,
        descripcion=vehiculo.descripcion,
        cliente_id=vehiculo.cliente_id,
    )
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo
