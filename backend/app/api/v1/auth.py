from fastapi import APIRouter, Depends

from app.core.auth import get_session_status
from app.schemas.auth import SessionStatus

router = APIRouter(tags=["auth"])


@router.get("/auth/session", response_model=SessionStatus)
async def read_session(status: dict = Depends(get_session_status)) -> SessionStatus:
    return SessionStatus(**status)
