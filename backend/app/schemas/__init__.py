"""
Esquemas Pydantic - T-004
=========================

Exportar esquemas para facilitar imports futuros
"""

from app.schemas.cliente import ClienteBase, ClienteCreate, ClienteRead
from app.schemas.vehiculo import VehiculoBase, VehiculoCreate, VehiculoRead

__all__ = [
    "ClienteBase",
    "ClienteCreate",
    "ClienteRead",
    "VehiculoBase",
    "VehiculoCreate",
    "VehiculoRead",
]
from app.schemas.instalacion import InstalacionBase, InstalacionCreate, InstalacionRead

__all__.extend(["InstalacionBase", "InstalacionCreate", "InstalacionRead"])
