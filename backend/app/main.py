import logging
import time

from fastapi import FastAPI, Request

from app.api.error_handlers import register_exception_handlers
from app.config.logging_config import configure_logging
from app.config.settings import get_settings
from app.api.health import router as health_router

configure_logging()

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Repository Intelligence Engine",
    version=settings.app_version,
)

register_exception_handlers(app)
app.include_router(
    health_router,
    prefix=settings.api_prefix,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log each HTTP request, its status code, and processing time."""

    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    except Exception:
        logger.exception(
            "Request failed: %s %s",
            request.method,
            request.url.path,
        )
        raise

    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "%s %s | status=%s | duration=%.2fms",
            request.method,
            request.url.path,
            status_code,
            duration_ms,
        )


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    logger.debug("Health check requested")
    return {"status": "ok"}