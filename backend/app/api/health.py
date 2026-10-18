from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.application.health_service import get_service_health

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def service_health() -> JSONResponse:
    """Report application dependency availability."""

    health = get_service_health()

    status_code = 200 if health["status"] == "ok" else 503

    return JSONResponse(
        status_code=status_code,
        content=health,
    )