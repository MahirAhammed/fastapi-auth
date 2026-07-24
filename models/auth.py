from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str | None = None
    password: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str