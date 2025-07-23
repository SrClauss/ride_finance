from datetime import datetime
from fastapi.testclient import TestClient

# Testes para Metas (Goals)
def test_create_and_get_goal(authenticated_client: TestClient):
    """
    Testa a criação e busca de uma meta.
    """
    goal_data = {
        "title": "Meta de Ganhos Semanais",
        "type": "weekly",
        "category": "income",
        "target": 1500.00,
        "deadline": "2025-07-27",
    }
    create_response = authenticated_client.post("/api/goals", json=goal_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    assert created_data["title"] == "Meta de Ganhos Semanais"
    
    get_response = authenticated_client.get("/api/goals")
    assert get_response.status_code == 200
    goals_list = get_response.json()
    assert len(goals_list) > 0
    assert goals_list[0]["id"] == created_data["id"]

# Testes para Sessões de Trabalho (Work Sessions)
def test_create_and_get_work_session(authenticated_client: TestClient):
    """
    Testa a criação e busca de uma sessão de trabalho.
    """
    session_data = {
        "start_time": datetime.now().isoformat(),
        "date": "2025-07-22",
        "total_minutes": 120
    }
    create_response = authenticated_client.post("/api/work-sessions", json=session_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    assert created_data["total_minutes"] == 120

    get_response = authenticated_client.get("/api/work-sessions")
    assert get_response.status_code == 200
    sessions_list = get_response.json()
    assert len(sessions_list) > 0
    assert sessions_list[0]["id"] == created_data["id"]