# test_models.py
from app.database import SessionLocal
from app import crud, schemas, models

def run_test():
    print("--- Iniciando teste de criação de pedido ---")
    db = SessionLocal()

    try:
        # 1. Pegar o usuário 'admin' (deve ter sido criado no startup da API)
        admin_user = crud.get_user_by_username(db, username="admin")
        if not admin_user:
            print("ERRO: Usuário 'admin' não encontrado. Certifique-se que a API está rodando.")
            return
        print(f"Usuário encontrado: {admin_user.username} (ID: {admin_user.id})")

        # 2. Criar alguns produtos para o teste, caso não existam
        p1_data = schemas.ProductCreate(code="1088", product_name="BAGUETE KG", unit="UN", price=22.50, section="1") # 
        p2_data = schemas.ProductCreate(code="1302", product_name="FARINHA DE ROSCA KG", unit="KG", price=12.00, section="1") # 

        db_p1 = crud.get_product_by_code(db, code=p1_data.code) or crud.create_product(db, product=p1_data)
        db_p2 = crud.get_product_by_code(db, code=p2_data.code) or crud.create_product(db, product=p2_data)
        print(f"Produtos de teste disponíveis: '{db_p1.product_name}' e '{db_p2.product_name}'")

        # 3. Definir os itens para o novo pedido
        items_para_o_pedido = [
            schemas.OrderItemCreate(product_id=db_p1.id, quantity=2), # 2 Baguetes
            schemas.OrderItemCreate(product_id=db_p2.id, quantity=1)  # 1 Farinha de Rosca
        ]
        print("\nTentando criar um pedido com 2 itens...")

        # 4. Chamar a função CRUD para criar o pedido
        novo_pedido = crud.create_order(db=db, user_id=admin_user.id, items_in=items_para_o_pedido)

        # 5. Verificar e imprimir os resultados
        print("\n--- SUCESSO! Pedido criado ---")
        print(f"ID do Pedido: {novo_pedido.id}")
        print(f"Pertence ao Usuário ID: {novo_pedido.user_id}")
        print(f"Data de Criação: {novo_pedido.created_at}")
        print(f"Valor Total Calculado: R$ {novo_pedido.total_amount:.2f}")
        print("Itens do Pedido:")
        for item in novo_pedido.items:
            print(f"  - Item ID: {item.id}, Produto ID: {item.product_id} ('{item.product.product_name}'), "
                  f"Qtd: {item.quantity}, Preço Unit.: R$ {item.price:.2f}")

    finally:
        print("\n--- Teste concluído. Fechando conexão. ---")
        db.close()

if __name__ == "__main__":
    run_test()