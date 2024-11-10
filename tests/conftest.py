import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_db
from app.db.base import Base

# Criar banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    # Criar tabelas no banco de teste
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client() -> Generator:
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def clean_tables(db):
    """Limpa as tabelas após cada teste"""
    # Limpeza em ordem para evitar problemas de foreign key
    tables = [
        'ranking',
        'match',
        'tournament',
        'player'
    ]
    for table in tables:
        db.execute(f'DELETE FROM {table}')
    db.commit()