import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/news")
#fall back if post gres fails
SQLITE_FALLBACK_URL = "sqlite:///./topic_intelligence.db"

logger = logging.getLogger(__name__)


def _build_engine():
    primary_engine = create_engine(DATABASE_URL)

    try:
        with primary_engine.connect():
            logger.info("Connected to configured database.")
        return primary_engine
    except OperationalError as exc:
        logger.warning(
            "Failed to connect to configured database URL. Falling back to SQLite at %s. Error: %s",
            SQLITE_FALLBACK_URL,
            exc,
        )
        return create_engine(SQLITE_FALLBACK_URL, connect_args={"check_same_thread": False})


engine = _build_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
