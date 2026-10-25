"""
Modelos - T-003
===============

Importar modelos para que SQLAlchemy los registre en Base.metadata
"""

from app.models.cliente import Cliente
from app.models.vehiculo import Vehiculo

__all__ = ["Cliente", "Vehiculo"]
