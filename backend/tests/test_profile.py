from fastapi.testclient import TestClient

def test_get_comprehensive_profile(authenticated_client: TestClient):
    """
    Testa o endpoint de perfil abrangente, verificando se os cálculos básicos estão corretos.
    """
    # 1. Setup: Cria dados para serem agregados
    # Categoria de renda
    cat_income_res = authenticated_client.post("/api/categories", json={"name": "Renda", "type": "income"})
    cat_income_id = cat_income_res.json()["id"]

    # Categoria de despesa
    cat_expense_res = authenticated_client.post("/api/categories", json={"name": "Despesa", "type": "expense"})
    cat_expense_id = cat_expense_res.json()["id"]

    # Transações
    authenticated_client.post("/api/transactions", json={"amount": 100, "date": "2025-07-22T12:00:00", "category_id": cat_income_id, "type": "income"})
    authenticated_client.post("/api/transactions", json={"amount": 150, "date": "2025-07-22T14:00:00", "category_id": cat_income_id, "type": "income"})
    authenticated_client.post("/api/transactions", json={"amount": 40, "date": "2025-07-22T13:00:00", "category_id": cat_expense_id, "type": "expense"})

    # Sessão de Trabalho
    authenticated_client.post("/api/work-sessions", json={"start_time": "2025-07-22T10:00:00", "date": "2025-07-22", "total_minutes": 240})

    # 2. Chama o endpoint do perfil
    response = authenticated_client.get("/api/profile/comprehensive")
    assert response.status_code == 200
    data = response.json()

    # 3. Verifica os dados agregados
    assert "personal_info" in data
    assert "stats" in data
    
    stats = data["stats"]
    assert stats["total_trips"] == 2
    assert float(stats["total_earnings"]) == 250.0  # 100 + 150
    assert float(stats["total_expenses"]) == 40.0
    assert float(stats["net_profit"]) == 210.0 # 250 - 40
    assert stats["total_hours"] == 4 # 240 minutes