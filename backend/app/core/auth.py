from typing import Annotated
from fastapi import Depends, Header, HTTPException, Request, status

from app.core.config import Settings, get_settings
from app.core.sedes import SEDES, permitidas
from app.core.roles import roles_permitidos, sedes_perfil, puede_usar_ruta
from app.core.token_verifier import (
    TokenVerificationError,
    VerifiedIdentity,
    get_token_verifier,
)


def auth_ready(settings: Settings) -> bool:
    return bool(
        settings.SUPABASE_URL
        and settings.SUPABASE_PUBLISHABLE_KEY
        and settings.admin_emails
    )


AUTH_READY = auth_ready(get_settings())


def write_enabled(settings: Settings) -> bool:
    return bool(getattr(settings, "REGISTRO_WRITE_ENABLED", False) and auth_ready(settings))


def require_write_access(settings: Settings = Depends(get_settings)) -> None:
    if write_enabled(settings):
        return
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "code": "ESCRITURA_NO_HABILITADA",
            "message": "El guardado estará disponible tras aplicar la migración y conectar autenticación real",
        },
    )


async def get_current_identity(
    authorization: str | None = Header(default=None),
    verifier=Depends(get_token_verifier),
    settings: Settings = Depends(get_settings),
) -> VerifiedIdentity:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTENTICACION_REQUERIDA", "message": "Se requiere una sesión válida"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization[7:].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTENTICACION_REQUERIDA", "message": "Se requiere una sesión válida"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth_ready(settings) or verifier is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "AUTENTICACION_NO_CONFIGURADA", "message": "La autenticación no está configurada"},
        )
    try:
        return verifier.verify(token)
    except TokenVerificationError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail={"code": exc.code, "message": exc.message},
            headers={"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None,
        ) from exc


async def require_admin_identity(
    identity: VerifiedIdentity = Depends(get_current_identity),
    settings: Settings = Depends(get_settings),
) -> str:
    if not identity.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "CORREO_NO_VERIFICADO", "message": "El correo de la sesión no está verificado"},
        )
    if not roles_permitidos(identity.email, settings):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "USUARIO_NO_AUTORIZADO", "message": "Esta identidad no está autorizada"},
        )
    return identity.email


async def get_session_status(
    x_rol: str | None = Header(default=None),
    x_sede: str | None = Header(default=None),
    identity: VerifiedIdentity = Depends(get_current_identity),
    settings: Settings = Depends(get_settings),
) -> dict:
    authorized = identity.email_verified and acceso_sede(identity.email, x_rol, x_sede, settings)
    return {
        "authenticated": True,
        "rol": x_rol if authorized else None,
        "email": identity.email,
        "email_verified": identity.email_verified,
        "authorized": authorized,
        "authorization_code": None if authorized else (
            "CORREO_NO_VERIFICADO" if not identity.email_verified else "USUARIO_NO_AUTORIZADO"
        ),
    }


async def require_sede(
    x_sede: str | None = Header(default=None),
    identity: VerifiedIdentity = Depends(get_current_identity),
    settings: Settings = Depends(get_settings),
    x_rol: Annotated[str, Header()] = "administrador",
) -> str:
    if x_sede not in SEDES:
        raise HTTPException(400, detail={'code':'SEDE_REQUERIDA', 'message':'Selecciona una sede válida'})
    if not identity.email_verified or not acceso_sede(identity.email, x_rol, x_sede, settings):
        raise HTTPException(403, detail={'code':'SEDE_NO_AUTORIZADA', 'message':'Tu correo no tiene acceso a esta sede'})
    return x_sede


async def require_role_access(request: Request, identity: VerifiedIdentity = Depends(get_current_identity), settings: Settings = Depends(get_settings)):
    rol = request.headers.get('x-rol')
    if not identity.email_verified or not acceso_sede(identity.email, rol, request.headers.get('x-sede'), settings) or not puede_usar_ruta(rol, request.method, request.url.path):
        raise HTTPException(403, detail={'code':'PERFIL_NO_AUTORIZADO','message':'Este perfil no tiene permiso para realizar esta operación'})
    return rol


def acceso_sede(email, rol, sede, settings):
    if sede not in SEDES: return False
    if rol != 'instalador':
        return sede in sedes_perfil(email, rol, settings)
    # La cuenta temporal puede entrar sin asignación, pero no confirmar trabajos.
    from app.core.roles import CUENTA_PRUEBAS
    if email.lower() == CUENTA_PRUEBAS:
        return sede in sedes_perfil(email, rol, settings)
    from app.db.session import SessionLocal, engine
    from app.services.trabajo import trabajador
    with SessionLocal(bind=engine.execution_options(schema_translate_map={None:SEDES[sede]['schema']})) as db:
        return trabajador(db, email) is not None


def sedes_instalador_aprobado(email):
    """Descubre asignaciones sin confiar en roles o sedes enviados por el navegador."""
    from sqlalchemy import MetaData, literal, select, union_all
    from app.db.session import engine
    from app.db.registro_tables import trabajadores
    consultas = []
    for sede, config in SEDES.items():
        tabla = trabajadores.to_metadata(MetaData(), schema=config['schema'])
        consultas.append(select(literal(sede).label('sede')).where(tabla.c.email == email.lower(), tabla.c.activo.is_(True)))
    with engine.connect() as conn:
        return list(conn.execute(union_all(*consultas)).scalars())


def accesos_identidad(identity, settings):
    if not identity.email_verified:
        return {'email':identity.email, 'perfiles':[], 'authorization_code':'CORREO_NO_VERIFICADO'}
    from app.core.roles import ROLES, CUENTA_PRUEBAS
    permisos = {rol:sedes_perfil(identity.email, rol, settings) for rol in ROLES}
    # La cuenta temporal conserva sus permisos explícitos; las demás requieren aprobación real.
    if identity.email.lower() != CUENTA_PRUEBAS:
        permisos['instalador'] = sedes_instalador_aprobado(identity.email)
    perfiles = [{'rol':rol, 'sedes':[{'id':sede,'nombre':SEDES[sede]['nombre']} for sede in sedes]}
                for rol, sedes in permisos.items() if sedes]
    return {'email':identity.email, 'perfiles':perfiles,
            'authorization_code':None if perfiles else 'USUARIO_NO_AUTORIZADO'}
