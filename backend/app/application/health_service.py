from app.infrastructure.database import check_database_connection
from app.infrastructure.ollama_client import check_ollama_connection
from app.infrastructure.redis_client import check_redis_connection


def get_service_health() -> dict:
    """Return the availability of the application's dependencies."""

    dependencies = {
        "postgresql": check_database_connection(),
        "redis": check_redis_connection(),
        "ollama": check_ollama_connection(),
    }

    all_healthy = all(dependencies.values())

    return {
        "status": "ok" if all_healthy else "degraded",
        "dependencies": {
            name: {
                "status": "available" if is_available else "unavailable"
            }
            for name, is_available in dependencies.items()
        },
    }