"""
Base declarativa de SQLAlchemy - T-002
======================================

Conceptos para aprender:
- SQLAlchemy ORM: Permite trabajar con tablas usando clases Python
- DeclarativeBase: Clase base para todos los modelos
- Modelos: Cada clase heredada de Base representa una tabla en la BD
- MetaData: Información sobre las tablas y sus columnas

Esta base NO crea tablas, solo prepara el molde para futuros modelos.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Clase base declarativa para todos los modelos SQLAlchemy

    Explicación sencilla:
    - Todos los modelos (Cliente, Vehiculo) heredarán de esta clase
    - SQLAlchemy usará esta clase base to define el esquema de tablas
    - No se ejecutan migraciones ni se crean tablas en esta tarea
    """
    pass
