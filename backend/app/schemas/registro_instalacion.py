from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.catalogs import (
    INSTALADOR_IDS,
    OPACIDAD_IDS,
    PANELES_SUNROOF_DOBLE,
    TECNOLOGIA_IDS,
    TIPO_FACTURA_IDS,
    VIDRIO_IDS,
    label_for,
)
from app.core.pricing import calcular_desglose, catalogo_tarifas
from app.core.liquidacion import liquidar_instaladores
from app.core.cobros import calcular_cobro, garantia_instalacion


class InputModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class CatalogoItem(BaseModel):
    id: str
    label: str
    paneles: list[str] = Field(default_factory=list)


class TarifaTecnologia(BaseModel):
    id: str
    label: str
    precio_seccion_cop: int


class TarifasResponse(BaseModel):
    moneda: Literal["COP"]
    version: str
    tecnologias: list[TarifaTecnologia]
    incremento_seguridad_laterales_cop: int
    incremento_seguridad_laterales_unidad: str
    reglas_pendientes: list[str]


class CatalogosResponse(BaseModel):
    servicio: str
    tecnologias: list[CatalogoItem]
    opacidades: list[CatalogoItem]
    instaladores: list[CatalogoItem]
    tipos_factura: list[CatalogoItem]
    vidrios: list[CatalogoItem]
    tarifas: TarifasResponse


class SchemaStatusResponse(BaseModel):
    save_enabled: bool
    write_enabled: bool
    schema_ready: bool
    missing_requirements: list[str]
    admin_emails_configured: bool
    auth_ready: bool
    reasons: list[str]


class DesgloseConcepto(BaseModel):
    concepto: str
    detalle: str
    secciones: int | None = None
    tarifa_unitaria_cop: int | None = None
    importe_cop: int | None = None
    estado: Literal["definido", "pendiente"]
    motivo_pendiente: str | None = None


class DesglosePrecios(BaseModel):
    moneda: Literal["COP"]
    version: str
    estado: Literal["definido", "pendiente"]
    total_cop: int | None = None
    etiqueta_total: str
    conceptos: list[DesgloseConcepto]
    mano_obra: list[dict[str, Any]] = Field(default_factory=list)
    cobro: dict[str, Any] | None = None
    garantia: dict[str, Any] | None = None


class PagoInput(InputModel):
    medio: Literal['efectivo', 'transferencia', 'tarjeta_credito', 'sistecredito', 'addi']
    monto_cop: int = Field(gt=0, le=1000000000, strict=True)
    referencia: str | None = Field(default=None, max_length=120)


class RegistroInstalacionResult(BaseModel):
    instalacion_id: int
    cliente_id: int
    vehiculo_id: int
    cliente_reutilizado: bool
    vehiculo_reutilizado: bool
    detalles_guardados: int
    desglose: DesglosePrecios


class ClienteRegistroInput(InputModel):
    documento: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    contacto: str | None = None
    telefono: str | None = None
    email: str | None = None

    @field_validator("contacto", "telefono", "email")
    @classmethod
    def empty_to_none(cls, value: str | None) -> str | None:
        if not value:
            return None
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if "@" not in value or "." not in value.rsplit("@", 1)[-1]:
            raise ValueError("Correo electrónico inválido")
        return value.lower()

    @model_validator(mode="after")
    def sincronizar_telefono(self):
        telefono = self.telefono or self.contacto
        self.telefono = telefono
        self.contacto = telefono
        return self


class VehiculoRegistroInput(InputModel):
    vehiculo_id: int | None = Field(default=None, gt=0)
    placa: str = Field(min_length=1)
    marca: str = Field(min_length=1)
    descripcion: str | None = None

    @field_validator("descripcion")
    @classmethod
    def empty_to_none(cls, value: str | None) -> str | None:
        if not value:
            return None
        return value


class DetalleVidrioInput(InputModel):
    vidrio_id: str
    panel: str | None = None
    tecnologia_id: str
    opacidad_id: str
    instalador_id: str
    pelicula_seguridad: bool = False
    grupo: Literal["cuatro_laterales"] | None = None

    @field_validator("vidrio_id")
    @classmethod
    def validate_vidrio(cls, value: str) -> str:
        if value not in VIDRIO_IDS:
            raise ValueError("Vidrio no soportado")
        return value

    @field_validator("panel")
    @classmethod
    def normalize_panel(cls, value: str | None) -> str | None:
        if value in (None, "", "unico", "único"):
            return None
        if value not in PANELES_SUNROOF_DOBLE:
            raise ValueError("Panel no soportado")
        return value

    @field_validator("tecnologia_id")
    @classmethod
    def validate_tecnologia(cls, value: str) -> str:
        if value not in TECNOLOGIA_IDS:
            raise ValueError("Tecnología no soportada")
        return value

    @field_validator("opacidad_id")
    @classmethod
    def validate_opacidad(cls, value: str) -> str:
        if value not in OPACIDAD_IDS:
            raise ValueError("Opacidad no soportada")
        return value

    @field_validator("instalador_id")
    @classmethod
    def validate_instalador(cls, value: str) -> str:
        if value not in INSTALADOR_IDS:
            raise ValueError("Instalador no soportado")
        return value

    @model_validator(mode="after")
    def validate_panel_for_vidrio(self):
        if self.pelicula_seguridad and self.vidrio_id not in ('laterales_delanteros', 'laterales_traseros'):
            raise ValueError('La película de seguridad adicional solo aplica a laterales')
        if self.grupo and self.vidrio_id not in ('laterales_delanteros', 'laterales_traseros'):
            raise ValueError('El grupo cuatro laterales solo admite parejas laterales')
        if self.vidrio_id == "sunroof_doble" and self.panel is None:
            raise ValueError("El techo solar doble requiere panel delantero y trasero")
        if self.vidrio_id != "sunroof_doble" and self.panel is not None:
            raise ValueError("Solo el techo solar doble admite panel")
        return self


class RegistroInstalacionCreate(InputModel):
    cliente: ClienteRegistroInput
    vehiculo: VehiculoRegistroInput
    tipo_factura: str
    fecha: datetime | None = None
    retiro_material_anterior: bool = False
    observaciones: str | None = None
    estado: Literal["programado"] = "programado"
    detalles: list[DetalleVidrioInput] = Field(min_length=1)
    descuento_cop: int = Field(default=0, ge=0, le=1000000000, strict=True)
    motivo_descuento: str | None = Field(default=None, max_length=250)
    pagos: list[PagoInput] = Field(default_factory=list, max_length=20)

    @field_validator("tipo_factura")
    @classmethod
    def validate_tipo_factura(cls, value: str) -> str:
        if value not in TIPO_FACTURA_IDS:
            raise ValueError("Tipo de factura no soportado")
        return value

    @field_validator("observaciones")
    @classmethod
    def empty_to_none(cls, value: str | None) -> str | None:
        if not value:
            return None
        return value

    @model_validator(mode="after")
    def validate_detalles(self):
        vistos = set()
        for detalle in self.detalles:
            clave = (detalle.vidrio_id, detalle.panel or "unico")
            if clave in vistos:
                raise ValueError("No se puede repetir un vidrio o panel")
            vistos.add(clave)

        agrupados = [d for d in self.detalles if d.grupo == 'cuatro_laterales']
        if agrupados and {d.vidrio_id for d in agrupados} != {'laterales_delanteros', 'laterales_traseros'}:
            raise ValueError('El grupo cuatro laterales requiere ambas parejas')
        paneles_solares = {
            detalle.panel
            for detalle in self.detalles
            if detalle.vidrio_id == "sunroof_doble"
        }
        if paneles_solares and paneles_solares != set(PANELES_SUNROOF_DOBLE):
            raise ValueError("El techo solar doble requiere panel delantero y trasero")

        calcular_cobro(calcular_desglose(self.detalles)['total_cop'], self.descuento_cop, self.motivo_descuento, self.pagos)
        return self


class RegistroVidrioResumen(BaseModel):
    vidrio: str
    panel: str | None = None
    tecnologia: str
    opacidad: str
    instalador: str


class RegistroInstalacionPreview(BaseModel):
    cliente: dict[str, Any]
    vehiculo: dict[str, Any]
    tipo_factura: str
    cantidad_vidrios: int
    tecnologias_utilizadas: list[str]
    detalles: list[RegistroVidrioResumen]
    desglose: DesglosePrecios
    guardado_habilitado: bool = False
    motivos: list[str]


def desglose_registro(payload: RegistroInstalacionCreate) -> dict:
    desglose = calcular_desglose(payload.detalles)
    desglose['cobro'] = calcular_cobro(desglose['total_cop'], payload.descuento_cop, payload.motivo_descuento, payload.pagos)
    desglose['total_cop'] = desglose['cobro']['total_cop']
    desglose['mano_obra'] = liquidar_instaladores(payload.detalles)
    desglose['garantia'] = garantia_instalacion(payload.fecha, payload.detalles)
    return desglose


def build_preview(payload: RegistroInstalacionCreate) -> RegistroInstalacionPreview:
    return RegistroInstalacionPreview(
        cliente={
            "documento": payload.cliente.documento,
            "nombre": payload.cliente.nombre,
            "contacto": payload.cliente.contacto,
            "telefono": payload.cliente.telefono,
            "email": payload.cliente.email,
        },
        vehiculo={
            "vehiculo_id": str(payload.vehiculo.vehiculo_id)
            if payload.vehiculo.vehiculo_id
            else None,
            "placa": payload.vehiculo.placa,
            "marca": payload.vehiculo.marca,
            "descripcion": payload.vehiculo.descripcion,
        },
        tipo_factura=label_for("tipos_factura", payload.tipo_factura),
        cantidad_vidrios=len(payload.detalles),
        tecnologias_utilizadas=sorted(
            {label_for("tecnologias", item.tecnologia_id) for item in payload.detalles}
        ),
        detalles=[
            RegistroVidrioResumen(
                vidrio=label_for("vidrios", item.vidrio_id),
                panel=item.panel.title() if item.panel else None,
                tecnologia=label_for("tecnologias", item.tecnologia_id) + (" + película de seguridad" if item.pelicula_seguridad else ""),
                opacidad=label_for("opacidades", item.opacidad_id),
                instalador=label_for("instaladores", item.instalador_id),
            )
            for item in payload.detalles
        ],
        desglose=desglose_registro(payload),
        motivos=["GUARDADO_PENDIENTE_DE_ESQUEMA_Y_AUTENTICACION"],
    )
