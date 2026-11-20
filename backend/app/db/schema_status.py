EXPECTED_TABLES = (
    "inventario",
    "inventario_movimientos",
    "catalogo_instaladores",
    "catalogo_opacidades_polarizado",
    "catalogo_tecnologias_polarizado",
    "catalogo_tipos_factura",
    "catalogo_vidrios_polarizado",
    "instalacion_detalles",
    "instalacion_novedades",
)

EXPECTED_COLUMNS = {
    "clientes": ("telefono", "email"),
    "vehiculos": ("marca",),
    "instalaciones": (
        "tipo_factura",
        "desglose_precios",
        "tarifas_aplicadas",
        "moneda",
        "precio_estado",
        "precio_total_cop",
    ),
}


def missing_requirements(inspector) -> list[str]:
    table_names = set(inspector.get_table_names())
    missing = []

    for table in EXPECTED_TABLES:
        if table not in table_names:
            missing.append(f"tabla:{table}")

    for table, columns in EXPECTED_COLUMNS.items():
        if table not in table_names:
            missing.append(f"tabla:{table}")
            continue
        existing = {column["name"] for column in inspector.get_columns(table)}
        for column in columns:
            if column not in existing:
                missing.append(f"{table}.{column}")

    return missing


def get_schema_status() -> dict:
    from sqlalchemy import inspect

    from app.core.auth import auth_ready, write_enabled as auth_write_enabled
    from app.core.config import settings
    from app.db.session import engine

    try:
        missing = missing_requirements(inspect(engine))
    except Exception:
        missing = ["INSPECCION_NO_DISPONIBLE"]

    admin_configurado = bool(settings.admin_emails)
    escritura_habilitada = auth_write_enabled(settings)
    autenticacion_lista = auth_ready(settings)
    reasons = []
    if not autenticacion_lista:
        reasons.append("AUTENTICACION_PENDIENTE")
    if missing:
        reasons.append("ESQUEMA_PENDIENTE")
    if not admin_configurado:
        reasons.append("ADMINISTRADORES_SIN_CONFIGURAR")
    if not escritura_habilitada:
        reasons.append("ESCRITURA_CERRADA")

    return {
        "save_enabled": not reasons,
        "write_enabled": escritura_habilitada,
        "schema_ready": not missing,
        "missing_requirements": missing,
        "admin_emails_configured": admin_configurado,
        "auth_ready": auth_ready(settings),
        "reasons": reasons,
    }
