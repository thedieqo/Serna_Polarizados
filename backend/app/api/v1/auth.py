from fastapi import APIRouter, Depends

from app.core.auth import get_session_status
from app.schemas.auth import SessionStatus

router = APIRouter(tags=["auth"])


@router.get("/auth/session", response_model=SessionStatus)
async def read_session(status: dict = Depends(get_session_status)) -> SessionStatus:
    return SessionStatus(**status)


from app.core.auth import accesos_identidad, get_current_identity
from app.core.config import get_settings

@router.get('/auth/accesos')
def read_accesos(identity=Depends(get_current_identity), settings=Depends(get_settings)):
    return accesos_identidad(identity, settings)
