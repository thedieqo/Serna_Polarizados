"""
CRUD para Cliente - T-005
========================

Conceptos para aprender:
- CRUD: Create, Read, Update, Delete (solo Create/Read en T-005)
- Sesión SQLAlchemy: Permite interactuar con la base de datos
- IntegrityError: Error al violar restricciones UNIQUE/FOREIGN KEY
- Filtros: Buscar por documento para validar duplicados

No se ejecutan migraciones ni conexiones reales en esta tarea.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate


def get_cliente(db: Session, cliente_id: int) -> Optional[Cliente]:
    """
    Obtener un cliente por ID
    Explicación sencilla: Busca un registro por su clave primaria
    """
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def get_cliente_by_documento(db: Session, documento: str) -> Optional[Cliente]:
    """
    Obtener un cliente por documento
    Explicación sencilla: Útil para validar duplicados y para consultas (RF-03)
    """
    return db.query(Cliente).filter(Cliente.documento == documento).first()


def get_clientes(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
    """
    Obtener lista de clientes con paginación básica
    Explicación sencilla: Permite listar clientes si es necesario
    """
    return db.query(Cliente).offset(skip).limit(limit).all()


def create_cliente(db: Session, cliente: ClienteCreate) -> Cliente:
    """
    Crear un nuevo cliente
    Explicación sencilla: Crea un objeto ORM, lo guarda en BD y lo retorna
    Lanza IntegrityError si hay duplicado (documento único)
    """
    db_cliente = Cliente(
        nombre=cliente.nombre,
        documento=cliente.documento,
        contacto=cliente.contacto,
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
