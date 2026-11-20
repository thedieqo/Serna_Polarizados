"""
Endpoints API v1 para Instalaciones - T-008.2.6
===============================================

Endpoints para gestión de instalaciones
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.auth import require_admin_identity, require_write_access
from app.core.catalogs import catalogos_response
from app.core.config import settings
from app.db.schema_status import get_schema_status
from app.db.session import get_db
from app.schemas.garantia import NovedadGarantiaCreate, NovedadGarantiaRead
from app.schemas.instalacion import (
    HistorialResponse,
    InstalacionCreate,
    InstalacionDetalleRead,
    InstalacionRead,
)
from app.schemas.registro_instalacion import (
    CatalogosResponse,
    RegistroInstalacionCreate,
    RegistroInstalacionPreview,
    RegistroInstalacionResult,
    SchemaStatusResponse,
    build_preview,
)
from app.services.garantias import GarantiaError, guardar_novedad
from app.services.registro_instalacion import (
    RegistroConflictError,
    guardar_registro,
)
from app import crud

router = APIRouter(prefix="/instalaciones", tags=["Instalaciones"])


@router.get("/catalogos", response_model=CatalogosResponse)
def read_catalogos():
    return catalogos_response()


@router.get("/schema-status", response_model=SchemaStatusResponse)
def read_schema_status():
    return get_schema_status()


@router.post("/preview", response_model=RegistroInstalacionPreview)
def preview_registro(payload: RegistroInstalacionCreate, db: Session = Depends(get_db)):
    preview = build_preview(payload)
    estado = get_schema_status()
    preview.guardado_habilitado = estado["save_enabled"]
    preview.motivos = list(estado["reasons"])
    cobro = preview.desglose.cobro
    if cobro['total_cop'] is None:
        preview.guardado_habilitado = False
        preview.motivos.append('Hay precios pendientes de definir')
    elif cobro['saldo_cop'] != 0:
        preview.guardado_habilitado = False
        preview.motivos.append(f"Falta registrar ${cobro['saldo_cop']:,} COP en medios de pago")
    if payload.tipo_descuento == 'referido':
        from app.services.referidos import consultar_referido
        referido = consultar_referido(db, payload.referido_placa, documento_receptor=payload.cliente.documento)
        preview.desglose.cobro['referido'] = referido
        if not referido['disponible']:
            preview.guardado_habilitado = False
            preview.motivos.append(referido['motivo'])
    return preview


@router.post(
    "/registro",
    response_model=RegistroInstalacionResult,
    status_code=status.HTTP_201_CREATED,
)
def create_registro(
    payload: RegistroInstalacionCreate,
    db: Session = Depends(get_db),
    administrador: str = Depends(require_admin_identity),
):
    require_write_access(settings)
    try:
        return guardar_registro(db, payload)
    except RegistroConflictError as exc:
        detail = {"code": exc.code, "message": exc.message}
        if exc.fields:
            detail["fields"] = exc.fields
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail) from exc


@router.get("/historial", response_model=HistorialResponse)
def read_historial(
    q: Optional[str] = Query(default=None, max_length=100),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.instalacion.get_historial(db, q=q, skip=skip, limit=limit)


@router.get("/referidos/{placa}")
def read_referido(placa: str, db: Session = Depends(get_db)):
    from app.services.referidos import consultar_referido
    return consultar_referido(db, placa)


@router.get("/ventas/resumen")
def read_ventas(anio: int = Query(ge=2000, le=2100), mes: int = Query(ge=1, le=12), corte: str = Query(default="mes", pattern="^(mes|primera|segunda)$"), db: Session = Depends(get_db)):
    from app.services.ventas import resumen_ventas
    reporte = resumen_ventas(db, anio, mes, corte)
    reporte['acumulado_mes'] = resumen_ventas(db, anio, mes, 'mes', acumulado=True)
    return reporte


@router.get("/{instalacion_id}/detalle", response_model=InstalacionDetalleRead)
def read_detalle(instalacion_id: int, db: Session = Depends(get_db)):
    detalle = crud.instalacion.get_detalle(db, instalacion_id=instalacion_id)
    if detalle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instalación no encontrada",
        )
    return detalle


@router.post(
    "/{instalacion_id}/novedades",
    response_model=NovedadGarantiaRead,
    status_code=status.HTTP_201_CREATED,
)
def create_novedad_garantia(
    instalacion_id: int,
    payload: NovedadGarantiaCreate,
    db: Session = Depends(get_db),
    administrador: str = Depends(require_admin_identity),
):
    require_write_access(settings)
    if payload.instalacion_id != instalacion_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La instalación del cuerpo no coincide con la ruta",
        )
    try:
        return guardar_novedad(db, payload, administrador)
    except GarantiaError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": exc.code, "message": exc.message},
        ) from exc


@router.post("/", response_model=InstalacionRead, status_code=status.HTTP_201_CREATED)
def create_instalacion(instalacion: InstalacionCreate, db: Session = Depends(get_db)):
    try:
        return crud.instalacion.create_instalacion(db=db, instalacion=instalacion)
    except ValueError as e:
        if str(e) == "Vehículo no existe":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El vehículo asociado no existe",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error en los datos de la instalación",
        )


@router.get("/", response_model=List[InstalacionRead])
def read_instalaciones(
    skip: int = 0,
    limit: int = 100,
    vehiculo_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if vehiculo_id is not None:
        return crud.instalacion.get_instalaciones_by_vehiculo(db, vehiculo_id=vehiculo_id)
    return crud.instalacion.get_instalaciones(db, skip=skip, limit=limit)


@router.get("/{instalacion_id}", response_model=InstalacionRead)
def read_instalacion(instalacion_id: int, db: Session = Depends(get_db)):
    db_instalacion = crud.instalacion.get_instalacion(db, instalacion_id=instalacion_id)
    if db_instalacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instalación no encontrada",
        )
    return db_instalacion
