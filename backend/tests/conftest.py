import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# FIX 1: Importar os modelos para que o SQLAlchemy os reconheça
from app.db import models
from app.db.database import Base, get_db
from app.main import app

# URL para um banco de dados SQLite em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Engine de teste
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fábrica de sessões de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Fixtures de Teste Refatoradas ---

@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    Cria uma nova sessão de banco de dados com uma transação para cada teste.
    A transação é revertida (rollback) ao final, isolando os testes.
    """
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """
    Cria um cliente de teste que usa a sessão de banco de dados de teste.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def authenticated_client(client: TestClient) -> TestClient:
    """
    Cria um usuário, faz login e retorna um cliente já autenticado.
    """
    user_data = {
        "username": "testauthuser",
        "password": "testauthpassword",
        "email": "auth@example.com",
        "full_name": "Authenticated User",
        "phone": "1122334455"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200, f"Falha ao registrar usuário: {response.text}"

    login_response = client.post(
        "/api/auth/token",
        data={"username": user_data["username"], "password": user_data["password"]},
    )
    assert login_response.status_code == 200, f"Falha ao fazer login: {login_response.text}"
    token = login_response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"

    return client