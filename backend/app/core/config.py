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

    ADMIN_EMAILS: str = ""
    REGISTRO_WRITE_ENABLED: bool = False
    FRONTEND_ORIGINS: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:5174,http://127.0.0.1:5174"
    )

    SUPABASE_URL: Optional[str] = None
    SUPABASE_PUBLISHABLE_KEY: Optional[str] = None
    SUPABASE_JWKS_URL: Optional[str] = None
    SUPABASE_JWT_ISSUER: Optional[str] = None
    SUPABASE_JWT_AUDIENCE: str = "authenticated"
    SUPABASE_VERIFY_MODE: str = "jwks"

    @property
    def admin_emails(self) -> frozenset[str]:
        return frozenset(
            email.strip().lower()
            for email in self.ADMIN_EMAILS.split(",")
            if email.strip()
        )

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings() -> Settings:
    return settings


# Instancia única de configuración (Singleton)
settings = Settings()
