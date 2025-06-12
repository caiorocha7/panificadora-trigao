# populate_db.py (versão atualizada com autenticação)
import json
import requests
from requests.auth import HTTPBasicAuth

# --- CONFIGURAÇÃO ---
# URL da API com o novo prefixo
API_URL = "http://127.0.0.1:8000/api/v1/products/"
TOKEN_URL = "http://127.0.0.1:8000/api/v1/auth/token"

# Credenciais do usuário admin para obter o token
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"


def get_auth_token(username, password):
    """Função para obter o token de autenticação da API."""
    print("Tentando obter o token de autenticação...")
    try:
        response = requests.post(
            TOKEN_URL,
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("Token obtido com sucesso!")
            return token
        else:
            print(f"Falha ao obter token. Status: {response.status_code}, Resposta: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao tentar obter token: {e}")
        return None

def populate_from_json(file_path):
    """
    Lê o arquivo JSON, obtém um token e envia os dados para a API
    para criar os produtos no banco de dados.
    """
    # 1. Obter o token de autenticação
    token = get_auth_token(ADMIN_USERNAME, ADMIN_PASSWORD)
    if not token:
        print("Não foi possível continuar sem um token de autenticação. Abortando.")
        return
        
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Ler e processar o arquivo JSON
    print("Iniciando o povoamento do banco de dados...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    products_to_add = []
    for section, products in data.items():
        for product in products:
            if "inativo" in product["product_name"].lower():
                continue
            
            try:
                price = float(product.get("price", 0))
            except (ValueError, TypeError):
                price = 0.0

            product_data = {
                "code": str(product.get("code")),
                "product_name": product.get("product_name"),
                "unit": product.get("unit"),
                "tax": product.get("tax"),
                "section": product.get("section"),
                "price": price
            }
            products_to_add.append(product_data)
    
    print(f"Encontrados {len(products_to_add)} produtos válidos para adicionar.")

    # 3. Enviar cada produto para a API com o cabeçalho de autenticação
    for product in products_to_add:
        try:
            # Inclui o 'headers' na requisição
            response = requests.post(API_URL, json=product, headers=headers)
            
            if response.status_code == 201: # O status de criação agora é 201
                print(f"Sucesso: Produto '{product['product_name']}' adicionado.")
            elif response.status_code == 400 and "já existe" in response.json().get("detail", ""):
                print(f"Aviso: Produto '{product['product_name']}' já existe. Pulando.")
            else:
                print(f"Falha ao adicionar '{product['product_name']}'. Status: {response.status_code}, Resposta: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de conexão: {e}")


if __name__ == "__main__":
    populate_from_json("produtos-trigao.json")
    print("Povoamento do banco de dados concluído.")