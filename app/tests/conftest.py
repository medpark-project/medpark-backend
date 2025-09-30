import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base
from app.db.dependencies import get_db

TEST_DATABASE_URL = os.environ.get("FAKE_DATABASE_URL")

if TEST_DATABASE_URL:
    print("--- Usando Banco de Dados PostgreSQL para testes ---")
    engine = create_engine(TEST_DATABASE_URL)
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

app.dependency_overrides[get_db] = override_get_db

# cliente api teste: faz as requisições
@pytest.fixture(scope="function")
def client():

    Base.metadata.create_all(bind=engine)

    yield TestClient(app)

    Base.metadata.drop_all(bind=engine)
