"""
Esquemas Pydantic para Vehiculo - T-004
=======================================

Conceptos para aprender:
- Pydantic: Biblioteca para validar datos con Python
- BaseModel: Clase base para crear esquemas
- Pydantic v2: Usa model_config with ConfigDict
- from_attributes: Permite leer datos desde objetos ORM (SQLAlchemy)
- ForeignKey: En el modelo, aquí solo validamos el valor (cliente_id)

Los esquemas validan los datos que entran/salen de la API,
los modelos definen cómo se guardan in la base de datos.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class VehiculoBase(BaseModel):
    """
    Esquema base with campos comunes para Vehiculo

    Explicación sencilla:
    - Campos compartidos entre creación y lectura
    - descripcion es opcional (coincide con nullable=True en el modelo)
    """
    placa: str
    descripcion: Optional[str] = None


class VehiculoCreate(VehiculoBase):
    """
    Esquema para crear un Vehiculo (entrada)

    Explicación sencilla:
    - Lo que recibe la API al registrar un vehículo
    - Debe asociarse obligatoriamente a un cliente existente (RF-02)
    - No incluye id (se genera automáticamente en la BD)
    """
    cliente_id: int


class VehiculoRead(VehiculoBase):
    """
    Esquema para leer/retornar a Vehiculo (salida)

    Explicación sencilla:
    - Lo que devuelve la API al consultar un vehículo
    - Incluye id y cliente_id
    - from_attributes permite leer desde objetos SQLAlchemy
    """
    id: int
    cliente_id: int

    model_config = ConfigDict(from_attributes=True)
