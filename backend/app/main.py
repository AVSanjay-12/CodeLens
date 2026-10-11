from fastapi import FastAPI
from app.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Repository Intelligence Engine",
    version=settings.app_version,
)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
