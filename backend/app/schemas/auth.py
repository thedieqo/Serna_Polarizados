from pydantic import BaseModel


class SessionStatus(BaseModel):
    authenticated: bool
    email: str
    email_verified: bool
    authorized: bool
    authorization_code: str | None = None
