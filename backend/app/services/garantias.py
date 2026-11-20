from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.db.registro_tables import instalacion_novedades, instalaciones
from app.schemas.garantia import NovedadGarantiaCreate, NovedadGarantiaRead


class GarantiaError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def guardar_novedad(
    db: Session, payload: NovedadGarantiaCreate, administrador: str
) -> NovedadGarantiaRead:
    identificacion = administrador.strip()
    if not identificacion:
        raise GarantiaError(
            "IDENTIDAD_AUTENTICADA_REQUERIDA",
            "La novedad requiere un administrador autenticado",
        )

    try:
        existe = db.execute(
            select(instalaciones.c.id).where(instalaciones.c.id == payload.instalacion_id)
        ).first()
        if existe is None:
            raise GarantiaError(
                "INSTALACION_NO_ENCONTRADA",
                "La instalación asociada no existe",
            )

        resultado = db.execute(
            insert(instalacion_novedades).values(
                instalacion_id=payload.instalacion_id,
                fecha_atencion=payload.fecha_atencion,
                motivo=payload.motivo,
                descripcion=payload.descripcion,
                registrado_por=identificacion,
            )
        )
        fila = db.execute(
            select(instalacion_novedades).where(
                instalacion_novedades.c.id == resultado.inserted_primary_key[0]
            )
        ).mappings().one()
        db.flush()
    except GarantiaError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise

    db.commit()
    return NovedadGarantiaRead(**dict(fila))
