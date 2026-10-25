"""
Configuración del proyecto Serna Polarizados - T-002
====================================================

Conceptos para aprender:
- Variables de entorno: Valores que cambian según el ambiente (desarrollo/producción)
- pydantic-settings: Permite leer .env y validar tipos automáticamente
- .env: Archivo con secretos (NUNCA subir a Git)
- DATABASE_URL: Cadena de conexión a PostgreSQL

Esta configuración NO conecta a la base de datos, solo prepara la lectura
de las variables de entorno.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """
    Clase de configuración usando pydantic-settings
    """

    # Configuración de Base de Datos PostgreSQL
    DATABASE_URL: str = "postgresql://usuario:contrasena@localhost:5432/serna_polarizados"

    # Componentes opcionales para construcción segura (evitan errores de codificación)
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_DB: Optional[str] = None

    # Configuración de la aplicación
    APP_NAME: str = "Serna Polarizados API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Instancia única de configuración (Singleton)
settings = Settings()
