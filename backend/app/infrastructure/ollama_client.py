import httpx

from app.config.settings import get_settings

settings = get_settings()


def check_ollama_connection() -> bool:
    """Check whether the Ollama API is reachable."""

    try:
        response = httpx.get(
            f"{settings.ollama_base_url.rstrip('/')}/api/tags",
            timeout=5.0,
        )
        response.raise_for_status()
        return True

    except httpx.HTTPError:
        return False


def list_available_models() -> list[str]:
    """Return the names of models available in Ollama."""

    response = httpx.get(
        f"{settings.ollama_base_url.rstrip('/')}/api/tags",
        timeout=10.0,
    )
    response.raise_for_status()

    data = response.json()

    return [
        model["name"]
        for model in data.get("models", [])
        if "name" in model
    ]