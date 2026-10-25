"""
Endpoints API v1 para Clientes - T-005
======================================

Conceptos para aprender:
- FastAPI Router: Agrupa endpoints relacionados
- Depends: Inyección de dependencias (sesión de BD)
- HTTPException: Manejo de errores HTTP
- Status Codes: 200 OK, 201 Created, 404 Not Found, 409 Conflict
- Response Model: Define qué esquema se devuelve

No se instalan dependencias ni se ejecutan migraciones en esta tarea.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.db.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteRead
from app import crud

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo cliente

    Explicación sencilla:
    - Valida datos con ClienteCreate
    - Verifica documento duplicado
    - Crea cliente y retorna con ClienteRead
    """
    # Verificar si ya existe un cliente con ese documento
    db_cliente = crud.cliente.get_cliente_by_documento(db, documento=cliente.documento)
    if db_cliente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un cliente con ese documento",
        )

    try:
        return crud.cliente.create_cliente(db=db, cliente=cliente)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un cliente con ese documento",
        )


@router.get("/", response_model=List[ClienteRead])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de clientes

    Explicación sencilla: Lista con paginación básica
    """
    clientes = crud.cliente.get_clientes(db, skip=skip, limit=limit)
    return clientes


@router.get("/{cliente_id}", response_model=ClienteRead)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtener un cliente por ID

    Explicación sencilla: Busca cliente por clave primaria
    """
    db_cliente = crud.cliente.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )
    return db_cliente


@router.get("/by-documento/{documento}", response_model=ClienteRead)
def read_cliente_by_documento(documento: str, db: Session = Depends(get_db)):
    """
    Obtener un cliente por documento

    Explicación sencilla: Útil para búsquedas por documento (RF-03)
    """
    db_cliente = crud.cliente.get_cliente_by_documento(db, documento=documento)
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )
    return db_cliente
