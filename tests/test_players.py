import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.main import app
from app.services.player_service import PlayerService
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerUpdate

client = TestClient(app)

# Dados para teste
test_player_data = {
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123"
}

def test_create_player():
    response = client.post("/api/v1/players/", json=test_player_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_player_data["email"]
    assert data["username"] == test_player_data["username"]
    assert "id" in data
    
def test_create_player_duplicate_email():
    # Primeiro criar um jogador
    client.post("/api/v1/players/", json=test_player_data)
    
    # Tentar criar outro jogador com mesmo email
    duplicate_player = dict(test_player_data)
    duplicate_player["username"] = "another_user"
    response = client.post("/api/v1/players/", json=duplicate_player)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_create_player_duplicate_username():
    # Tentar criar jogador com username duplicado
    duplicate_player = dict(test_player_data)
    duplicate_player["email"] = "another@example.com"
    response = client.post("/api/v1/players/", json=duplicate_player)
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]

def test_get_player():
    # Primeiro criar um jogador
    create_response = client.post("/api/v1/players/", json=test_player_data)
    player_id = create_response.json()["id"]
    
    # Buscar o jogador criado
    response = client.get(f"/api/v1/players/{player_id}")
    assert response.status_code == 200
    assert response.json()["email"] == test_player_data["email"]

def test_get_nonexistent_player():
    response = client.get("/api/v1/players/99999")
    assert response.status_code == 404

def test_list_players():
    response = client.get("/api/v1/players/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_player():
    # Criar jogador
    create_response = client.post("/api/v1/players/", json=test_player_data)
    player_id = create_response.json()["id"]
    
    # Atualizar dados
    update_data = {
        "full_name": "Updated Name"
    }
    response = client.patch(f"/api/v1/players/{player_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"

def test_delete_player():
    # Criar jogador
    create_response = client.post("/api/v1/players/", json=test_player_data)
    player_id = create_response.json()["id"]
    
    # Deletar jogador
    response = client.delete(f"/api/v1/players/{player_id}")
    assert response.status_code == 200
    assert response.json()["is_active"] == False

def test_reactivate_player():
    # Criar jogador
    create_response = client.post("/api/v1/players/", json=test_player_data)
    player_id = create_response.json()["id"]
    
    # Deletar jogador
    client.delete(f"/api/v1/players/{player_id}")
    
    # Reativar jogador
    response = client.post(f"/api/v1/players/{player_id}/reactivate")
    assert response.status_code == 200
    assert response.json()["is_active"] == True