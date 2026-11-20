"""
Sesión y Engine de SQLAlchemy - T-002
======================================

Conceptos para aprender:
- Engine: Conexión principal con la base de datos PostgreSQL
- SessionLocal: Fábrica de sesiones para interactuar con la BD
- Session: Cada sesión es como una "conversación" con la BD
- get_db(): Función para obtener sesión en dependencias de FastAPI
- pool_pre_ping: Verifica conexión antes de usarla

Esta configuración NO conecta a la BD ahora. Solo prepara los objetos.
La conexión real se probará en tareas futuras con autorización.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def _build_engine():
    # Preferir construcción por componentes si están disponibles en .env
    if (
        settings.POSTGRES_USER
        and settings.POSTGRES_PASSWORD is not None
        and settings.POSTGRES_HOST
        and settings.POSTGRES_PORT
        and settings.POSTGRES_DB
    ):
        url = URL.create(
            drivername="postgresql",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=int(settings.POSTGRES_PORT),
            database=settings.POSTGRES_DB,
        )
        return create_engine(url, pool_pre_ping=True)

    # Fallback: parsear DATABASE_URL existente y reconstruir con URL.create
    try:
        parsed = make_url(settings.DATABASE_URL)
    except Exception:
        raise RuntimeError(
            "No se pudo interpretar DATABASE_URL; revise la configuración de conexión"
        ) from None

    if parsed.drivername in ("postgres", "postgresql"):
        url = URL.create(
            drivername="postgresql",
            username=parsed.username,
            password=parsed.password,
            host=parsed.host,
            port=parsed.port,
            database=parsed.database,
            query=dict(parsed.query),
        )
    else:
        url = parsed

    return create_engine(url, pool_pre_ping=True)


# Crear engine de SQLAlchemy
engine = _build_engine()

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependencia para obtener sesión de BD en FastAPI
from fastapi import Depends
from app.core.auth import require_sede
from app.core.sedes import SEDES


def get_db(sede: str = Depends(require_sede)):
    """
    Generador de sesión para usar como dependencia en FastAPI
    """
    db = SessionLocal(bind=engine.execution_options(schema_translate_map={None: SEDES[sede]['schema']}))
    try:
        yield db
    finally:
        db.close()
