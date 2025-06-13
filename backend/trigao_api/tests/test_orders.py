# tests/test_orders.py
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas, crud

# Vamos reutilizar o teste anterior e expandi-lo
def test_create_order_success(client: TestClient, db_session: Session, normal_user_auth_headers: dict):
    # Cria um produto de exemplo
    product = crud.create_product(db_session, schemas.ProductCreate(code="T001", product_name="Pão Teste", unit="UN", price=1.0))
    
    order_data = {"items": [{"product_id": product.id, "quantity": 5}]}
    
    response = client.post("/api/v1/orders/", json=order_data, headers=normal_user_auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["total_amount"] == 5.0
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product.id
    assert data["items"][0]["quantity"] == 5
    assert data["items"][0]["price"] == 1.0

def test_create_order_product_not_found(client: TestClient, normal_user_auth_headers: dict):
    order_data = {"items": [{"product_id": 999, "quantity": 1}]} # ID de produto que não existe
    response = client.post("/api/v1/orders/", json=order_data, headers=normal_user_auth_headers)
    
    assert response.status_code == 404
    assert "Produto com ID 999 não encontrado" in response.json()["detail"]

def test_user_can_only_see_own_orders(client: TestClient, db_session: Session, normal_user_auth_headers: dict):
    # Cria um pedido para o usuário normal
    product = crud.create_product(db_session, schemas.ProductCreate(code="T002", product_name="Bolo Teste", unit="UN", price=15.0))
    client.post("/api/v1/orders/", json={"items": [{"product_id": product.id, "quantity": 1}]}, headers=normal_user_auth_headers)
    
    response = client.get("/api/v1/orders/", headers=normal_user_auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1 # Usuário normal deve ver apenas o seu pedido
    assert data[0]["items"][0]["product"]["product_name"] == "Bolo Teste"

def test_admin_can_see_all_orders(client: TestClient, db_session: Session, admin_auth_headers: dict, normal_user_auth_headers: dict):
    # 1. Cria um produto para o pedido
    product = crud.create_product(db_session, schemas.ProductCreate(code="T999", product_name="Item de Teste para Admin", unit="UN", price=10.0))
    
    # 2. Cria um pedido com o usuário normal
    client.post("/api/v1/orders/", json={"items": [{"product_id": product.id, "quantity": 1}]}, headers=normal_user_auth_headers)
    # --- FIM DA CORREÇÃO ---

    # 3. Admin busca os pedidos e agora deve encontrar o que foi criado
    response = client.get("/api/v1/orders/", headers=admin_auth_headers)
    
    assert response.status_code == 200
    assert len(response.json()) >= 1 # Agora o teste vai passar
    
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_user_cannot_see_others_order(client: TestClient, db_session: Session, admin_auth_headers: dict, normal_user_auth_headers: dict):
    # Admin cria um produto e um pedido
    product = crud.create_product(db_session, schemas.ProductCreate(code="T003", product_name="Admin Item", unit="UN", price=50.0))
    admin_order_res = client.post("/api/v1/orders/", json={"items": [{"product_id": product.id, "quantity": 1}]}, headers=admin_auth_headers)
    admin_order_id = admin_order_res.json()["id"]

    # Usuário normal tenta acessar o pedido do admin
    response = client.get(f"/api/v1/orders/{admin_order_id}", headers=normal_user_auth_headers)
    
    assert response.status_code == 403
    assert "Permissão insuficiente" in response.json()["detail"]