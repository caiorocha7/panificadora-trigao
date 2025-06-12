# populate_db.py (versão final, lendo do arquivo JSON do usuário)

import json
import logging
from decimal import Decimal, InvalidOperation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    from app.database import SessionLocal
    from app.models import User, Product, Order, OrderItem
    from app.schemas import Role
    from app.auth import get_password_hash
except ImportError as e:
    logging.error(f"Erro ao importar módulos da aplicação: {e}")
    logging.error("Certifique-se de que o script está sendo executado no contexto correto do projeto.")
    exit(1)


def create_initial_users(db):
    """Verifica e cria os usuários 'admin' e 'user' se eles não existirem."""
    logging.info("Verificando e criando usuários iniciais...")
    users_to_create = [
        {"username": "admin", "email": "admin@example.com", "password": "admin123", "role": Role.ADMIN},
        {"username": "user", "email": "user@example.com", "password": "user123", "role": Role.USER}
    ]
    users_added = []
    for user_data in users_to_create:
        user_exists = db.query(User).filter((User.email == user_data["email"]) | (User.username == user_data["username"])).first()
        if user_exists:
            logging.info(f"Usuário com email '{user_data['email']}' ou username '{user_data['username']}' já existe. Pulando.")
            continue
        new_user = User(username=user_data["username"], email=user_data["email"], hashed_password=get_password_hash(user_data["password"]), role=user_data["role"])
        db.add(new_user)
        users_added.append(user_data["email"])
    if users_added:
        db.commit()
        for email in users_added:
            logging.info(f"Usuário '{email}' criado com sucesso no banco de dados.")
    else:
        logging.info("Nenhum usuário novo para criar.")


def create_products_from_json(db, file_path="produtos-trigao.json"):
    """Lê um arquivo JSON, processa os produtos e os cria no banco se não existirem."""
    logging.info(f"Iniciando a criação de produtos a partir do arquivo '{file_path}'...")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"ERRO CRÍTICO: O arquivo de produtos '{file_path}' não foi encontrado. Abortando criação de produtos.")
        return
    except json.JSONDecodeError:
        logging.error(f"ERRO CRÍTICO: O arquivo '{file_path}' contém um JSON inválido.")
        return

    products_to_add = []
    for section_name, products_in_section in data.items():
        for product_data in products_in_section:
            # Pula produtos marcados como inativos
            if "inativo" in product_data.get("product_name", "").lower():
                continue
            
            # Valida e converte o preço para Decimal
            try:
                price = Decimal(str(product_data.get("price", "0")))
            except InvalidOperation:
                logging.warning(f"Preço inválido para o produto '{product_data.get('product_name')}'. Usando 0.0.")
                price = Decimal("0.0")

            code = str(product_data.get("code"))
            if not code or code == 'None':
                logging.warning(f"Produto '{product_data.get('product_name')}' sem código. Pulando.")
                continue

            # Verifica se o produto já existe pelo código
            product_exists = db.query(Product).filter(Product.code == code).first()
            if product_exists:
                continue # Silenciosamente pula para não poluir o log com centenas de mensagens

            # Adiciona o produto à lista para criação
            products_to_add.append(
                Product(
                    code=code,
                    product_name=product_data.get("product_name"),
                    unit=product_data.get("unit"),
                    tax=product_data.get("tax"),
                    section=product_data.get("section"),
                    price=price
                )
            )

    if not products_to_add:
        logging.info("Nenhum produto novo para adicionar do arquivo JSON. Todos já existem no banco de dados.")
        return

    db.add_all(products_to_add)
    db.commit()
    logging.info(f"SUCESSO: {len(products_to_add)} novos produtos foram criados a partir do arquivo '{file_path}'.")


def create_sample_orders(db):
    """Cria um pedido de exemplo usando produtos que devem existir do JSON."""
    logging.info("Verificando e criando pedidos de exemplo...")
    
    if db.query(Order).first():
        logging.info("Tabela de pedidos já populada. Pulando.")
        return

    # Busca entidades necessárias para criar um pedido de exemplo
    user = db.query(User).filter(User.email == "user@example.com").first()
    # Tenta pegar dois produtos quaisquer do banco para o pedido
    produto1 = db.query(Product).offset(0).first()
    produto2 = db.query(Product).offset(1).first()

    if not all([user, produto1, produto2]):
        logging.error("Não foi possível encontrar usuário ou produtos suficientes no banco para criar um pedido de exemplo. Abortando.")
        return
    
    logging.info(f"Criando pedido de exemplo com os produtos '{produto1.product_name}' e '{produto2.product_name}'.")

    order_item1 = OrderItem(product_id=produto1.id, quantity=2, price=produto1.price)
    order_item2 = OrderItem(product_id=produto2.id, quantity=1, price=produto2.price)
    total_order = (order_item1.quantity * order_item1.price) + (order_item2.quantity * order_item2.price)
    
    new_order = Order(user_id=user.id, items=[order_item1, order_item2], total_amount=total_order)
    db.add(new_order)
    
    db.commit()
    logging.info(f"Pedido de exemplo criado para o usuário '{user.email}' no valor de R$ {total_order:.2f}.")


def main():
    logging.info("Iniciando o processo de povoamento do banco de dados...")
    db = SessionLocal()
    try:
        create_initial_users(db)
        create_products_from_json(db) # Chamando a nova função
        create_sample_orders(db)
    except Exception as e:
        logging.error(f"Ocorreu um erro irrecuperável durante o povoamento: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()
        logging.info("Processo de povoamento concluído. Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()