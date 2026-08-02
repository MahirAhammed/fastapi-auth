"""
Entry point. Run with:

    uvicorn main:app --reload
"""
from fastapi import FastAPI

from core.config import get_settings
from core.exceptions import register_exception_handlers
from routers import auth, protected, public

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI backend using Supabase as the Identity Provider.",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(public.router)
app.include_router(protected.router)

# Note on Swagger: we don't need to hand-build the OpenAPI security schema.
# `core.dependencies.bearer_scheme` is a `fastapi.security.HTTPBearer`
# instance wired in via `Depends()` on the auth dependency chain. FastAPI
# walks each route's dependency tree at OpenAPI-generation time and
# automatically registers the "HTTPBearer" security scheme plus a per-route
# security requirement for any route that (transitively) depends on it. As a
# result, the "Authorize" padlock shows up only on /auth/logout,
# /protected/profile, and /protected/dashboard - not on /public/info.


@app.get("/", tags=["health"])
def health_check() -> dict:
    return {"status": "ok", "service": settings.APP_NAME}
