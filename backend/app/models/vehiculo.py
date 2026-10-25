"""
Modelo Vehiculo - T-003
=======================

Conceptos para aprender:
- Foreign Key (FK): Llave que une dos tablas. Apunta a la PK de otra tabla
- Relationship: Permite acceder al objeto relacionado
- back_populates: Sincroniza las relaciones bidireccionales
- UNIQUE: Evita duplicados (placa única según RF-02)

No se crean tablas, solo se definen modelos.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Vehiculo(Base):
    """
    Modelo de Vehiculo

    Representa la tabla 'vehiculos' con la información del vehículo.
    Relación: Un vehículo pertenece a un solo cliente (N:1)
    """
    __tablename__ = "vehiculos"

    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Campos del vehículo
    placa = Column(String, unique=True, nullable=False, index=True)
    descripcion = Column(String, nullable=True)

    # Clave foránea hacia Cliente
    # Explicación sencilla: Esta columna guarda el id del cliente al que pertenece
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)

    # Relación con Cliente
    # Explicación sencilla: Un vehículo pertenece a un cliente
    cliente = relationship("Cliente", back_populates="vehiculos")

    # Relación con Instalacion (1:N)
    instalaciones = relationship(
        "Instalacion",
        back_populates="vehiculo",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Vehiculo(id={self.id}, placa='{self.placa}', cliente_id={self.cliente_id})>"
