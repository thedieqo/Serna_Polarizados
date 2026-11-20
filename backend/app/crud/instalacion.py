"""
CRUD para Instalacion - T-008.2.5
================================

CRUD: Create, Read con filtros por vehículo
"""

from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app.models.cliente import Cliente
from app.models.instalacion import Instalacion
from app.models.vehiculo import Vehiculo
from app.schemas.instalacion import (
    HistorialResponse,
    InstalacionCreate,
    InstalacionDetalleRead,
    InstalacionHistorialItem,
)


def get_instalacion(db: Session, instalacion_id: int) -> Optional[Instalacion]:
    """Obtener una instalación por ID"""
    return db.query(Instalacion).filter(Instalacion.id == instalacion_id).first()


def get_instalaciones(db: Session, skip: int = 0, limit: int = 100) -> List[Instalacion]:
    """Obtener lista de instalaciones con paginación"""
    return db.query(Instalacion).offset(skip).limit(limit).all()


def get_instalaciones_by_vehiculo(db: Session, vehiculo_id: int) -> List[Instalacion]:
    """Obtener instalaciones de un vehículo específico"""
    return db.query(Instalacion).filter(Instalacion.vehiculo_id == vehiculo_id).all()


def create_instalacion(db: Session, instalacion: InstalacionCreate) -> Instalacion:
    """Crear una nueva instalación validando que el vehículo exista"""
    db_vehiculo = db.query(Vehiculo).filter(Vehiculo.id == instalacion.vehiculo_id).first()
    if not db_vehiculo:
        raise ValueError("Vehículo no existe")

    db_instalacion = Instalacion(
        vehiculo_id=instalacion.vehiculo_id,
        fecha=instalacion.fecha,
        tipo_servicio=instalacion.tipo_servicio,
        opacidad=instalacion.opacidad,
        zonas=instalacion.zonas,
        asignaciones_instaladores=instalacion.asignaciones_instaladores,
        retiro_material_anterior=instalacion.retiro_material_anterior,
        observaciones=instalacion.observaciones,
        estado=instalacion.estado,
    )
    db.add(db_instalacion)
    db.commit()
    db.refresh(db_instalacion)
    return db_instalacion


def _historial_query(db: Session, q: Optional[str] = None):
    consulta = (
        db.query(Instalacion)
        .join(Vehiculo, Instalacion.vehiculo_id == Vehiculo.id)
        .join(Cliente, Vehiculo.cliente_id == Cliente.id)
    )
    if q:
        termino = f"%{q.strip()}%"
        consulta = consulta.filter(
            or_(Cliente.documento.ilike(termino), Vehiculo.placa.ilike(termino))
        )
    return consulta


def _valores(items: Any, claves: tuple[str, ...]) -> List[str]:
    resultados: list[str] = []
    for item in items or []:
        if isinstance(item, dict):
            for clave in claves:
                valor = item.get(clave)
                if valor not in (None, ""):
                    resultados.append(str(valor))
    return sorted(dict.fromkeys(resultados))


def _base_historial(instalacion: Instalacion) -> dict:
    return {
        "id": instalacion.id,
        "fecha": instalacion.fecha,
        "estado": instalacion.estado,
        "tipo_servicio": instalacion.tipo_servicio,
        "cliente_documento": instalacion.vehiculo.cliente.documento,
        "cliente_nombre": instalacion.vehiculo.cliente.nombre,
        "vehiculo_placa": instalacion.vehiculo.placa,
        "vehiculo_marca": getattr(instalacion.vehiculo, "marca", None),
        "vehiculo_descripcion": instalacion.vehiculo.descripcion,
    }


def get_historial(
    db: Session, q: Optional[str] = None, skip: int = 0, limit: int = 20
) -> HistorialResponse:
    consulta = _historial_query(db, q)
    total = consulta.count()
    filas = (
        consulta.order_by(Instalacion.fecha.desc(), Instalacion.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return HistorialResponse(
        items=[InstalacionHistorialItem(**_base_historial(fila)) for fila in filas],
        total=total,
        skip=skip,
        limit=limit,
        q=q or None,
    )


def _detalles_vidrios(instalacion: Instalacion) -> list[dict]:
    def valor(item, *claves):
        return next((str(item[c]) for c in claves if item.get(c) not in (None, "")), None)

    detalles = []
    for zona in instalacion.zonas or []:
        if not isinstance(zona, dict):
            continue
        vidrio = valor(zona, "vidrio", "zona", "nombre")
        panel = valor(zona, "panel")
        asignaciones = [
            a for a in instalacion.asignaciones_instaladores or []
            if isinstance(a, dict)
            and vidrio is not None
            and valor(a, "vidrio", "zona", "nombre") == vidrio
            and valor(a, "panel") == panel
        ]
        detalles.append({
            "vidrio": vidrio,
            "panel": panel,
            "tecnologia": valor(zona, "tecnologia", "tecnologia_label"),
            "opacidad": valor(zona, "opacidad", "opacidad_aplicada"),
            "instaladores": _valores(asignaciones, ("instalador", "instalador_label")),
        })
    return detalles


def get_detalle(db: Session, instalacion_id: int) -> Optional[InstalacionDetalleRead]:
    fila = _historial_query(db).filter(Instalacion.id == instalacion_id).first()
    if fila is None:
        return None
    datos = _base_historial(fila)
    datos.update(
        {
            "cliente_email": fila.vehiculo.cliente.email,
            "cliente_telefono": fila.vehiculo.cliente.telefono or fila.vehiculo.cliente.contacto,
            "tipo_factura": fila.tipo_factura,
            "detalles_vidrios": _detalles_vidrios(fila),
            "retiro_material_anterior": fila.retiro_material_anterior,
            "observaciones": fila.observaciones,
            "tecnologias": _valores(fila.zonas, ("tecnologia", "tecnologia_label")),
            "vidrios": _valores(fila.zonas, ("vidrio", "zona", "nombre")),
            "opacidades": _valores(fila.zonas, ("opacidad", "opacidad_aplicada")),
            "instaladores": _valores(
                fila.asignaciones_instaladores, ("instalador", "instalador_label")
            ),
            "desglose_precios": getattr(fila, "desglose_precios", None),
            "tarifas_aplicadas": getattr(fila, "tarifas_aplicadas", None),
            "moneda": getattr(fila, "moneda", None),
            "precio_estado": getattr(fila, "precio_estado", None),
            "precio_total_cop": getattr(fila, "precio_total_cop", None),
        }
    )
    return InstalacionDetalleRead(**datos)


__all__ = [
    "get_instalacion",
    "get_instalaciones",
    "get_instalaciones_by_vehiculo",
    "create_instalacion",
    "get_historial",
    "get_detalle",
]
