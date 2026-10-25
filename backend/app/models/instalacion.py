"""
Modelo Instalacion - T-008.2.1
=============================

No se crean tablas, solo se definen modelos.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Instalacion(Base):
    __tablename__ = "instalaciones"

    id = Column(Integer, primary_key=True, index=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False, index=True)

    fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    tipo_servicio = Column(String, nullable=False)  # polarizado | pelicula_seguridad | ambos
    opacidad = Column(String, nullable=True)
    zonas = Column(JSON, nullable=False)  # detalles por zona con opacidad
    asignaciones_instaladores = Column(JSON, nullable=False)  # asignaciones por zona
    retiro_material_anterior = Column(Boolean, default=False, nullable=False)
    observaciones = Column(Text, nullable=True)
    estado = Column(String, nullable=False)  # programado | en_proceso | finalizado | anulado

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    vehiculo = relationship("Vehiculo", back_populates="instalaciones")

    def __repr__(self):
        return f"<Instalacion(id={self.id}, vehiculo_id={self.vehiculo_id}, estado='{self.estado}')>"
