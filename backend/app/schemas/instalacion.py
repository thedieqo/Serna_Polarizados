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


class InstalacionHistorialItem(BaseModel):
    id: int
    fecha: datetime
    estado: str
    tipo_servicio: str
    cliente_documento: str
    cliente_nombre: str
    vehiculo_placa: str
    vehiculo_marca: Optional[str] = None
    vehiculo_descripcion: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class HistorialResponse(BaseModel):
    items: list[InstalacionHistorialItem]
    total: int
    skip: int
    limit: int
    q: Optional[str] = None


class VidrioInstaladoRead(BaseModel):
    vidrio: Optional[str] = None
    panel: Optional[str] = None
    tecnologia: Optional[str] = None
    opacidad: Optional[str] = None
    instaladores: list[str] = Field(default_factory=list)


class InstalacionDetalleRead(InstalacionHistorialItem):
    referido: dict | None = None
    cliente_email: Optional[str] = None
    cliente_telefono: Optional[str] = None
    tipo_factura: Optional[str] = None
    detalles_vidrios: list[VidrioInstaladoRead] = Field(default_factory=list)
    retiro_material_anterior: bool
    observaciones: Optional[str] = None
    tecnologias: list[str]
    vidrios: list[str]
    opacidades: list[str]
    instaladores: list[str]
    desglose_precios: Optional[dict[str, Any]] = None
    tarifas_aplicadas: Optional[dict[str, Any]] = None
    moneda: Optional[str] = None
    precio_estado: Optional[str] = None
    precio_total_cop: Optional[int] = None
