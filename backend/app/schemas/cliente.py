"""
Esquemas Pydantic para Cliente - T-004
=======================================

Conceptos para aprender:
- Pydantic: Biblioteca para validar datos con Python
- BaseModel: Clase base para crear esquemas
- Pydantic v2: Usa model_config con ConfigDict
- from_attributes: Permite leer datos desde objetos ORM (SQLAlchemy)
- Create/Read: Separación entre datos de entrada y salida

Los esquemas validan los datos que entran/salen de la API,
los modelos definen cómo se guardan en la base de datos.
"""

from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    """
    Esquema base con campos comunes para Cliente

    Explicación sencilla:
    - Campos compartidos entre creación y lectura
    - Coincide con los campos obligatorios del modelo Cliente
    """
    nombre: str
    documento: str
    contacto: str


class ClienteCreate(ClienteBase):
    """
    Esquema para crear un Cliente (entrada)

    Explicación sencilla:
    - Lo que recibe la API al registrar un cliente
    - No incluye id (se genera automáticamente en la BD)
    """
    pass


class ClienteRead(ClienteBase):
    """
    Esquema para leer/retornar un Cliente (salida)

    Explicación sencilla:
    - Lo que devuelve la API al consultar un cliente
    - Incluye id generado por la BD
    - from_attributes permite leer desde objetos SQLAlchemy
    """
    id: int

    model_config = ConfigDict(from_attributes=True)
