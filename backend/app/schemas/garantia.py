from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InputModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class NovedadGarantiaCreate(InputModel):
    instalacion_id: int = Field(gt=0)
    fecha_atencion: datetime
    motivo: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)

    @field_validator("motivo", "descripcion")
    @classmethod
    def no_vacio(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El campo no puede estar vacío")
        return value


class NovedadGarantiaRead(BaseModel):
    id: int
    instalacion_id: int
    fecha_atencion: datetime
    motivo: str
    descripcion: str
    registrado_por: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
