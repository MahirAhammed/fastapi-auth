from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.supabase_client import supabase
from app.core.config import ADMINS
from app.core.exception import MissingTokenError, InvalidTokenError, ForbiddenError

security = HTTPBearer(auto_error= False)

def _get_access_token(credentials: Annotated[HTTPAuthorizationCredentials , Depends(security)] = None):
    if not credentials or not credentials.credentials:
        raise MissingTokenError()
    return credentials.credentials

def get_current_user(token: Annotated[str, Depends(_get_access_token)]) -> dict:
    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise InvalidTokenError()

    if not response or not response.user:
        raise InvalidTokenError()

    return response.user

def get_admin(user: Annotated[dict, Depends(get_current_user)]):
    email = user.email or ""
    if email not in ADMINS:
        raise ForbiddenError()
    return user