import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


# --- Fixture principal para os testes ---

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture que cria um banco de dados limpo para cada teste.
    """
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Remove todas as tabelas após o teste
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture que cria um cliente de teste e sobrescreve a dependência do DB.
    """

    def override_get_db():
        """
        Substitui a função get_db original para usar a sessão de teste.
        """
        try:
            yield db_session
        finally:
            db_session.close()

    # Aplica a substituição na aplicação
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Limpa a substituição depois do teste
    app.dependency_overrides.clear()
    
    
# Adicione ao final de tests/conftest.py

@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, db_session):
    """
    Fixture que cria um usuário, faz login e retorna um cliente
    já com o header de autorização configurado.
    """
    user_data = {
        "username": "testauthuser",
        "password": "testauthpassword",
        "email": "auth@example.com",
        "full_name": "Authenticated User",
        "phone": "1122334455"
    }
    # Registrar usuário
    client.post("/api/auth/register", json=user_data)

    # Fazer login para obter token
    login_response = client.post(
        "/api/auth/token",
        data={"username": user_data["username"], "password": user_data["password"]},
    )
    token = login_response.json()["access_token"]

    # Configurar o header de autorização
    client.headers["Authorization"] = f"Bearer {token}"
    
    return client