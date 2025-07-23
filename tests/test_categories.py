from fastapi.testclient import TestClient


def test_create_category(authenticated_client: TestClient):
    """
    Testa a criação de uma nova categoria para um usuário autenticado.
    """
    response = authenticated_client.post(
        "/api/categories",
        json={"name": "Combustível", "type": "expense", "icon": "gas-pump"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Combustível"
    assert data["type"] == "expense"
    assert "id" in data


def test_get_categories(authenticated_client: TestClient):
    """
    Testa se o endpoint retorna as categorias do usuário.
    """
    # Cria uma categoria primeiro
    authenticated_client.post(
        "/api/categories",
        json={"name": "Alimentação", "type": "expense", "icon": "utensils"},
    )

    response = authenticated_client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Verifica se a categoria criada está na lista
    assert any(cat["name"] == "Alimentação" for cat in data)


def test_get_categories_unauthenticated(client: TestClient):
    """
    Testa a falha ao tentar buscar categorias sem autenticação.
    """
    response = client.get("/api/categories")
    assert response.status_code == 401