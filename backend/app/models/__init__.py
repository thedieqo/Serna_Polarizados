"""
Modelos - T-003 / T-008
=======================

Importar modelos para que SQLAlchemy los registre en Base.metadata
"""

from app.models.cliente import Cliente
from app.models.vehiculo import Vehiculo
from app.models.instalacion import Instalacion

__all__ = ["Cliente", "Vehiculo", "Instalacion"]
