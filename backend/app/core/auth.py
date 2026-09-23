from fastapi import Header, HTTPException, status

from app.core.config import get_settings


def require_demo_user(
    x_api_key: str | None = Header(default=None),
    x_demo_user: str | None = Header(default="demo@resolviq.local"),
) -> str:
    """Optional demo auth boundary.

    If DEMO_API_KEY is not set, local development stays frictionless. If it is set,
    requests must send X-API-Key and can identify the demo user with X-Demo-User.
    """

    settings = get_settings()
    if settings.demo_api_key and x_api_key != settings.demo_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid demo API key",
        )
    return x_demo_user or "demo@resolviq.local"
