from pydantic import BaseModel
from datetime import datetime

class AuthRequest(BaseModel):
    email: str | None = None
    password: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class UserMetadataResponse(BaseModel):
    id: str
    email: str
    created_at: datetime