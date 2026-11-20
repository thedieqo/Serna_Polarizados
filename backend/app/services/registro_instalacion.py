from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.catalogs import label_for
from app.core.pricing import calcular_desglose, tarifas_aplicadas
from app.db.registro_tables import (
    clientes,
    instalacion_detalles,
    instalaciones,
    vehiculos,
)
from app.schemas.registro_instalacion import (
    DetalleVidrioInput,
    RegistroInstalacionCreate,
    RegistroInstalacionResult,
)

CAMPO_LABELS = {
    "nombre": "nombre del propietario",
    "contacto": "contacto del propietario",
    "telefono": "teléfono del propietario",
    "email": "correo del propietario",
    "marca": "marca del vehículo",
    "descripcion": "descripción del vehículo",
}


class RegistroConflictError(Exception):
    def __init__(self, code: str, message: str, fields: list[str] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.fields = fields or []


def _normal(value: object) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip().casefold()
    return normalized or None


def _same(existing: object, incoming: object) -> bool:
    return _normal(existing) == _normal(incoming)


def _resolve_cliente(db: Session, payload: RegistroInstalacionCreate) -> tuple[int, bool]:
    fila = db.execute(
        select(clientes).where(clientes.c.documento == payload.cliente.documento)
    ).mappings().first()
    if fila is None:
        resultado = db.execute(
            insert(clientes).values(
                documento=payload.cliente.documento,
                nombre=payload.cliente.nombre,
                contacto=payload.cliente.contacto or "",
                telefono=payload.cliente.telefono,
                email=payload.cliente.email,
            )
        )
        return resultado.inserted_primary_key[0], False

    conflictos = []
    if not _same(fila["nombre"], payload.cliente.nombre):
        conflictos.append(CAMPO_LABELS["nombre"])
    if not _same(fila["email"], payload.cliente.email):
        conflictos.append(CAMPO_LABELS["email"])

    telefono = _normal(payload.cliente.telefono or payload.cliente.contacto)
    telefonos_existentes = {
        _normal(fila["telefono"]),
        _normal(fila["contacto"]),
    }
    if telefono is not None and telefono not in telefonos_existentes:
        conflictos.append(CAMPO_LABELS["telefono"])
    if telefono is None and any(item is not None for item in telefonos_existentes):
        conflictos.append(CAMPO_LABELS["telefono"])
    if conflictos:
        raise RegistroConflictError(
            "DATOS_CLIENTE_DIFERENTES",
            "El documento pertenece a un registro con datos diferentes",
            conflictos,
        )
    return fila["id"], True


def _resolve_vehiculo(
    db: Session, payload: RegistroInstalacionCreate, cliente_id: int
) -> tuple[int, bool]:
    fila = db.execute(
        select(vehiculos).where(vehiculos.c.placa == payload.vehiculo.placa)
    ).mappings().first()
    if fila is None:
        resultado = db.execute(
            insert(vehiculos).values(
                placa=payload.vehiculo.placa,
                descripcion=payload.vehiculo.descripcion,
                cliente_id=cliente_id,
                marca=payload.vehiculo.marca,
            )
        )
        return resultado.inserted_primary_key[0], False

    if fila["cliente_id"] != cliente_id:
        raise RegistroConflictError(
            "VEHICULO_PERTENECE_A_OTRO_CLIENTE",
            "La placa pertenece a un propietario diferente",
            ["propietario del vehículo"],
        )

    conflictos = []
    for campo, valor in (
        ("marca", payload.vehiculo.marca),
        ("descripcion", payload.vehiculo.descripcion),
    ):
        if not _same(fila[campo], valor):
            conflictos.append(CAMPO_LABELS[campo])
    if conflictos:
        raise RegistroConflictError(
            "DATOS_VEHICULO_DIFERENTES",
            "La placa pertenece a un registro con datos diferentes",
            conflictos,
        )
    return fila["id"], True


def _zonas(detalles: list[DetalleVidrioInput]) -> list[dict[str, str | None]]:
    return [
        {
            "vidrio": label_for("vidrios", detalle.vidrio_id),
            "panel": detalle.panel.title() if detalle.panel else None,
            "tecnologia": label_for("tecnologias", detalle.tecnologia_id),
            "opacidad": label_for("opacidades", detalle.opacidad_id),
        }
        for detalle in detalles
    ]


def _asignaciones(detalles: list[DetalleVidrioInput]) -> list[dict[str, str | None]]:
    return [
        {
            "vidrio": label_for("vidrios", detalle.vidrio_id),
            "panel": detalle.panel.title() if detalle.panel else None,
            "instalador": label_for("instaladores", detalle.instalador_id),
        }
        for detalle in detalles
    ]


def _insert_instalacion(
    db: Session, payload: RegistroInstalacionCreate, vehiculo_id: int
) -> tuple[int, dict]:
    desglose = calcular_desglose(payload.detalles)
    valores = {
        "vehiculo_id": vehiculo_id,
        "tipo_servicio": "polarizado",
        "opacidad": None,
        "zonas": _zonas(payload.detalles),
        "asignaciones_instaladores": _asignaciones(payload.detalles),
        "retiro_material_anterior": payload.retiro_material_anterior,
        "observaciones": payload.observaciones,
        "estado": payload.estado,
        "tipo_factura": payload.tipo_factura,
        "desglose_precios": desglose,
        "tarifas_aplicadas": tarifas_aplicadas(desglose),
        "moneda": desglose["moneda"],
        "precio_estado": desglose["estado"],
        "precio_total_cop": desglose["total_cop"],
    }
    if payload.fecha is not None:
        valores["fecha"] = payload.fecha
    resultado = db.execute(insert(instalaciones).values(**valores))
    return resultado.inserted_primary_key[0], desglose


def _insert_detalles(
    db: Session, instalacion_id: int, detalles: list[DetalleVidrioInput]
) -> int:
    valores = [
        {
            "instalacion_id": instalacion_id,
            "vidrio_id": detalle.vidrio_id,
            "panel": detalle.panel,
            "tecnologia_id": detalle.tecnologia_id,
            "opacidad_id": detalle.opacidad_id,
            "instalador_id": detalle.instalador_id,
        }
        for detalle in detalles
    ]
    db.execute(insert(instalacion_detalles), valores)
    return len(valores)


def _map_integrity_error(exc: IntegrityError) -> RegistroConflictError:
    original = exc.orig
    pgcode = getattr(original, "pgcode", None)
    diag = getattr(original, "diag", None)
    constraint = getattr(diag, "constraint_name", None) or ""
    mensaje = str(original).casefold()

    if pgcode == "23505" or "unique" in mensaje or "duplicate" in mensaje:
        if "cliente" in constraint or "documento" in constraint:
            detalle = "Otro registro creó el documento del propietario"
        elif "vehiculo" in constraint or "placa" in constraint:
            detalle = "Otro registro creó la placa del vehículo"
        elif "vidrio" in constraint or "panel" in constraint:
            detalle = "Otro registro guardó un vidrio o panel de esta instalación"
        else:
            detalle = "Otro registro creó un valor único"
        return RegistroConflictError("DUPLICADO_CONCURRENTE", detalle)
    if pgcode in ("23503", "23514") or "foreign key" in mensaje or "check" in mensaje:
        return RegistroConflictError(
            "RESTRICCION_NO_CUMPLIDA",
            "Los datos no cumplen una restricción de la base de datos",
        )
    return RegistroConflictError(
        "ERROR_DE_INTEGRIDAD", "No fue posible guardar la instalación"
    )


def guardar_registro(
    db: Session, payload: RegistroInstalacionCreate
) -> RegistroInstalacionResult:
    try:
        cliente_id, cliente_reutilizado = _resolve_cliente(db, payload)
        vehiculo_id, vehiculo_reutilizado = _resolve_vehiculo(db, payload, cliente_id)
        instalacion_id, desglose = _insert_instalacion(db, payload, vehiculo_id)
        detalles_guardados = _insert_detalles(db, instalacion_id, payload.detalles)
        db.flush()
    except RegistroConflictError:
        db.rollback()
        raise
    except IntegrityError as exc:
        db.rollback()
        raise _map_integrity_error(exc) from exc
    except Exception:
        db.rollback()
        raise

    db.commit()
    return RegistroInstalacionResult(
        instalacion_id=instalacion_id,
        cliente_id=cliente_id,
        vehiculo_id=vehiculo_id,
        cliente_reutilizado=cliente_reutilizado,
        vehiculo_reutilizado=vehiculo_reutilizado,
        detalles_guardados=detalles_guardados,
        desglose=desglose,
    )
