# tests/test_auth.py
from fastapi.testclient import TestClient

def test_login_success(client: TestClient, admin_auth_headers: dict):
    # O próprio fixture 'admin_auth_headers' já testa a criação de usuário e o login.
    # Se o fixture foi criado sem erros, o login funcionou.
    # Vamos apenas verificar se o token nos dá acesso.
    response = client.get("/api/v1/products/", headers=admin_auth_headers)
    assert response.status_code == 200

def test_login_failure_wrong_password(client: TestClient):
    response = client.post("/api/v1/auth/token", data={"username": "testadmin", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha incorretos"

def test_login_failure_wrong_username(client: TestClient):
    response = client.post("/api/v1/auth/token", data={"username": "nouser", "password": "password"})
    assert response.status_code == 401

def test_protected_route_no_token(client: TestClient):
    response = client.get("/api/v1/products/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_protected_route_bad_token(client: TestClient):
    headers = {"Authorization": "Bearer badtoken"}
    response = client.get("/api/v1/products/", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Não foi possível validar as credenciais"