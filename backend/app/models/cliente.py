"""
Modelo Cliente - T-003
======================

Conceptos para aprender:
- Modelo ORM: Representa una tabla en la base de datos con una clase Python
- Primary Key (PK): Identificador único de cada registro
- Relationship: Permite relacionar modelos sin crear columnas extra
- back_populates: Sincroniza las relaciones bidireccionales
- UNIQUE: Evita duplicados (documento único según RF-01)

No se crean tablas, solo se definen los modelos.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Cliente(Base):
    """
    Modelo de Cliente

    Representa la tabla 'clientes' con la información básica del cliente.
    Relación: Un cliente puede tener muchos vehículos (1:N)
    """
    __tablename__ = "clientes"

    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Campos del cliente
    nombre = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False, index=True)
    contacto = Column(String, nullable=False)

    # Relación con Vehiculo (1:N)
    # Explicación sencilla: Un cliente tiene muchos vehículos
    vehiculos = relationship(
        "Vehiculo",
        back_populates="cliente",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Cliente(id={self.id}, documento='{self.documento}', nombre='{self.nombre}')>"
