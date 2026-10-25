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
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse

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
        parsed = urlparse(settings.DATABASE_URL)
        if parsed.scheme in ("postgresql", "postgres"):
            database = parsed.path.lstrip("/") if parsed.path else None
            url = URL.create(
                drivername="postgresql",
                username=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port,
                database=database,
            )
            return create_engine(url, pool_pre_ping=True)
    except Exception:
        pass

    # Último recurso: usar la URI tal como viene
    return create_engine(settings.DATABASE_URL, pool_pre_ping=True)


# Crear engine de SQLAlchemy
engine = _build_engine()

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependencia para obtener sesión de BD en FastAPI
def get_db():
    """
    Generador de sesión para usar como dependencia en FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
