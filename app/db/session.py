from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)

# Create SessionLocal class with sessionmaker factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Database dependency
def get_db():
    """
    Dependency function that creates a new SQLAlchemy SessionLocal
    that will be used in a single request, and then closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()