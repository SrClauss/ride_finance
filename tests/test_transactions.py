import json
from datetime import datetime
from fastapi.testclient import TestClient

def test_create_and_get_transaction(authenticated_client: TestClient):
    """
    Testa a criação e a busca de uma transação.
    """
    # 1. Primeiro, cria uma categoria para associar à transação
    cat_response = authenticated_client.post(
        "/api/categories",
        json={"name": "Corridas", "type": "income", "icon": "taxi"},
    )
    assert cat_response.status_code == 201
    category_id = cat_response.json()["id"]

    # 2. Cria a transação
    transaction_data = {
        "amount": 55.70,
        "description": "Corrida para o aeroporto",
        "type": "income",
        "date": datetime.now().isoformat(),
        "category_id": category_id,
    }
    
    # Pydantic converte Decimal para string em JSON, então precisamos fazer o mesmo
    create_response = authenticated_client.post("/api/transactions", json=json.loads(json.dumps(transaction_data, default=str)))
    assert create_response.status_code == 201
    created_data = create_response.json()
    assert created_data["description"] == "Corrida para o aeroporto"
    assert float(created_data["amount"]) == 55.70

    # 3. Busca a transação
    get_response = authenticated_client.get("/api/transactions")
    assert get_response.status_code == 200
    transactions_list = get_response.json()
    assert len(transactions_list) > 0
    assert transactions_list[0]["id"] == created_data["id"]


def test_get_transactions_date_range(authenticated_client: TestClient):
    """
    Testa a busca de transações por período.
    """
    # Cria uma categoria
    cat_res = authenticated_client.post("/api/categories", json={"name": "Test", "type": "income"})
    cat_id = cat_res.json()["id"]

    # Cria transações
    tx_data1 = {"amount": 10, "date": "2025-07-20T10:00:00", "category_id": cat_id, "type": "income"}
    tx_data2 = {"amount": 20, "date": "2025-07-22T10:00:00", "category_id": cat_id, "type": "income"}
    authenticated_client.post("/api/transactions", json=tx_data1)
    authenticated_client.post("/api/transactions", json=tx_data2)

    # Busca no período que inclui apenas a segunda transação
    response = authenticated_client.get("/api/transactions/date-range?start_date=2025-07-21&end_date=2025-07-23")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert float(data[0]["amount"]) == 20