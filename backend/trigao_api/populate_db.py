import json
import requests

# A URL base da sua API que está rodando
API_URL = "http://127.0.0.1:8000/products/"

def populate_from_json(file_path):
    """
    Lê o arquivo JSON, formata os dados e os envia para a API
    para criar os produtos no banco de dados.
    """
    print("Iniciando o povoamento do banco de dados...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    products_to_add = []
    # Itera sobre cada seção (como "1", "2", "22", etc.) no JSON
    for section, products in data.items():
        for product in products:
            # Pula produtos marcados como "INATIVO"
            if "inativo" in product["product_name"].lower():
                continue

            # Garante que o preço seja um número (float)
            try:
                price = float(product.get("price", 0))
            except (ValueError, TypeError):
                price = 0.0

            # Monta o dicionário com os dados do produto, conforme o schema da API
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

    # Envia cada produto para a API via requisição POST
    for product in products_to_add:
        try:
            response = requests.post(API_URL, json=product)
            if response.status_code == 200:
                print(f"Sucesso: Produto '{product['product_name']}' adicionado.")
            # Verifica se o produto já existe para não dar erro
            elif response.status_code == 400 and "já existe" in response.json().get("detail", ""):
                print(f"Aviso: Produto '{product['product_name']}' já existe. Pulando.")
            else:
                print(f"Falha ao adicionar '{product['product_name']}'. Status: {response.status_code}, Resposta: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro de conexão: {e}")

if __name__ == "__main__":
    populate_from_json("produtos-trigao.json")
    print("Povoamento do banco de dados concluído.")
