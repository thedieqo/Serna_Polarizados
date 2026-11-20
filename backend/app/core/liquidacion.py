"""Honorarios por sección, conservados junto al desglose de cada instalación."""
from app.core.catalogs import label_for

TARIFA_SECCION_COP = 25000
SECCIONES_PAGABLES = frozenset({
    "parabrisas", "luneta", "laterales_delanteros", "laterales_traseros",
    "sunroof_simple", "sunroof_doble",
})


def liquidar_instaladores(detalles) -> list[dict]:
    conceptos = []
    for detalle in detalles:
        if detalle.vidrio_id not in SECCIONES_PAGABLES:
            raise ValueError("Vidrio sin regla de pago al instalador")
        conceptos.append({
            "instalador_id": detalle.instalador_id,
            "instalador": label_for("instaladores", detalle.instalador_id),
            "vidrio": label_for("vidrios", detalle.vidrio_id),
            "panel": detalle.panel,
            "valor_cop": TARIFA_SECCION_COP,
        })
    return conceptos
