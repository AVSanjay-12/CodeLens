from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def check_database_connection() -> bool:
    """Check whether PostgreSQL is reachable."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception:
        return False