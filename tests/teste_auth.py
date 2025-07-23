from fastapi.testclient import TestClient


def test_register_user_success(client: TestClient):
    """
    Testa o registro de um novo usuário com sucesso.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "password": "testpassword123",
            "email": "test@example.com",
            "full_name": "Test User",
            "phone": "11999998888",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data  # Garante que a senha não é retornada


def test_register_duplicate_username(client: TestClient):
    """
    Testa a falha ao tentar registrar um usuário com um username que já existe.
    """
    # Cria o primeiro usuário
    client.post(
        "/api/auth/register",
        json={
            "username": "duplicateuser",
            "password": "password1",
            "email": "email1@example.com",
            "full_name": "User 1",
            "phone": "123",
        },
    )
    # Tenta criar o segundo com o mesmo username
    response = client.post(
        "/api/auth/register",
        json={
            "username": "duplicateuser",
            "password": "password2",
            "email": "email2@example.com",
            "full_name": "User 2",
            "phone": "456",
        },
    )
    assert response.status_code == 400
    assert "Username já está em uso" in response.json()["detail"]


def test_login_and_get_user_info(client: TestClient):
    """
    Testa o fluxo completo: registrar, fazer login e buscar os dados do usuário.
    """
    # 1. Registrar o usuário
    username = "logintest"
    password = "apowerfulpassword"
    email = "login@test.com"
    
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password,
            "email": email,
            "full_name": "Login Test User",
            "phone": "1122334455",
        },
    )
    assert register_response.status_code == 200

    # 2. Fazer login para obter o token
    login_response = client.post(
        "/api/auth/token", data={"username": username, "password": password}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    access_token = token_data["access_token"]

    # 3. Usar o token para buscar os dados do usuário
    headers = {"Authorization": f"Bearer {access_token}"}
    user_info_response = client.get("/api/auth/user", headers=headers)
    
    assert user_info_response.status_code == 200
    user_data = user_info_response.json()
    assert user_data["username"] == username
    assert user_data["email"] == email


def test_login_invalid_credentials(client: TestClient):
    """
    Testa a falha de login com credenciais inválidas.
    """
    response = client.post(
        "/api/auth/token", data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Usuário ou senha incorretos" in response.json()["detail"]