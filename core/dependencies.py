from typing import Annotated
from fastapi import Header, Depends
from supabase_client import supabase
from core.exception import MissingTokenError, InvalidTokenError

def _get_access_token(authorization: Annotated[str | None, Header()] = None):
    if not authorization:
        raise MissingTokenError()
        
    auth_scheme = authorization.split(" ")
    if len(auth_scheme) != 2 or auth_scheme[0] != "Bearer" or not auth_scheme[1]:
        raise MissingTokenError()

    return auth_scheme[1]

def get_current_user(token: Annotated[str, Depends(_get_access_token)]) -> dict:
    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise InvalidTokenError()

    if not response or not response.user:
        raise InvalidTokenError()

    return response.user