from pydantic import BaseModel


class SessionStatus(BaseModel):
    rol: str | None = None
    authenticated: bool
    email: str
    email_verified: bool
    authorized: bool
    authorization_code: str | None = None
