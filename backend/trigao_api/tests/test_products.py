# tests/test_products.py
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas

def test_create_product_as_admin(client: TestClient, admin_auth_headers: dict):
    product_data = {"code": "P123", "product_name": "Bolo de Chocolate", "unit": "UN", "price": 50.0}
    response = client.post("/api/v1/products/", json=product_data, headers=admin_auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == product_data["product_name"]
    assert "id" in data

def test_create_product_as_user_is_forbidden(client: TestClient, normal_user_auth_headers: dict):
    product_data = {"code": "P456", "product_name": "Torta de Limão", "unit": "UN", "price": 45.0}
    response = client.post("/api/v1/products/", json=product_data, headers=normal_user_auth_headers)
    assert response.status_code == 403
    assert "permissão para executar esta ação" in response.json()["detail"]

def test_read_products_as_any_authenticated_user(client: TestClient, normal_user_auth_headers: dict):
    response = client.get("/api/v1/products/", headers=normal_user_auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_product_as_user_is_forbidden(client: TestClient, db_session: Session, normal_user_auth_headers: dict, admin_auth_headers: dict):
    # Admin cria o produto
    product = schemas.ProductCreate(code="P789", product_name="Sonho", unit="UN", price=5.0)
    response = client.post("/api/v1/products/", json=product.dict(), headers=admin_auth_headers)
    product_id = response.json()["id"]

    # Usuário normal tenta atualizar
    update_data = {"code": "P789_UPDATED", "product_name": "Sonho de Creme", "unit": "UN", "price": 6.0}
    response = client.put(f"/api/v1/products/{product_id}", json=update_data, headers=normal_user_auth_headers)
    assert response.status_code == 403

def test_delete_product_as_admin(client: TestClient, db_session: Session, admin_auth_headers: dict):
    # Admin cria o produto
    product = schemas.ProductCreate(code="P999", product_name="Produto para Deletar", unit="UN", price=1.0)
    response = client.post("/api/v1/products/", json=product.dict(), headers=admin_auth_headers)
    product_id = response.json()["id"]
    
    # Admin deleta o produto
    response = client.delete(f"/api/v1/products/{product_id}", headers=admin_auth_headers)
    assert response.status_code == 200

    # Verifica se o produto foi realmente deletado
    response = client.get(f"/api/v1/products/", headers=admin_auth_headers)
    product_ids = [p["id"] for p in response.json()]
    assert product_id not in product_ids