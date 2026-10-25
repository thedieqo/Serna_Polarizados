"""
Esquemas Pydantic para Instalacion - T-008.2.4
===============================================

Conceptos para aprender:
- Pydantic v2: Validación con BaseModel y ConfigDict
- from_attributes: Permite leer datos desde objetos ORM (SQLAlchemy)
- Literal: Restricción de valores permitidos
- Field: Validaciones adicionales (mínimo de elementos)

Los esquemas validan los datos que entran/salen de la API.
"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any, Literal
from datetime import datetime


class InstalacionBase(BaseModel):
    """
    Esquema base con campos comunes para Instalacion
    """
    tipo_servicio: Literal["polarizado", "pelicula_seguridad", "ambos"]
    opacidad: Optional[str] = None
    zonas: list[dict[str, Any]] = Field(..., min_length=1)
    asignaciones_instaladores: list[dict[str, Any]] = Field(..., min_length=1)
    retiro_material_anterior: bool = False
    observaciones: Optional[str] = None
    estado: Literal["programado", "en_proceso", "finalizado", "anulado"]


class InstalacionCreate(InstalacionBase):
    """
    Esquema para crear una Instalacion (entrada)
    """
    vehiculo_id: int
    fecha: Optional[datetime] = None


class InstalacionRead(InstalacionBase):
    """
    Esquema para leer/retornar una Instalacion (salida)
    """
    id: int
    vehiculo_id: int
    fecha: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
