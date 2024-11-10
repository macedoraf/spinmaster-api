from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependency function that yields db sessions to FastAPI endpoints.
    
    Yields:
        Generator: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Add authentication dependency if needed
async def get_current_user(db: Session = Depends(get_db)):
    """
    Dependency for getting the current authenticated user.
    Can be expanded based on your authentication implementation.
    """
    # Implement your authentication logic here
    pass