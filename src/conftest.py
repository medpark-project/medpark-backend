import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import create_app
from src.db.session import Base
from src.db.dependencies import get_db

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL and 'postgresql' in DATABASE_URL:
    print("--- Usando Banco de Dados PostgreSQL para testes ---")
    engine = create_engine(DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    print("--- Usando Banco de Dados SQLite em memória para testes ---")
    SQLALCHEMY_DATABASE_URL_LOCAL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL_LOCAL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()