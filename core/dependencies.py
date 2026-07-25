from typing import Annotated
from fastapi import Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase_client import supabase
from core.exception import MissingTokenError, InvalidTokenError

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