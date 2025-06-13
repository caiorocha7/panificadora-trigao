from typing import List
from sqlalchemy.orm import Session
from . import models, schemas, auth

# --- CRUD de Usuário ---

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    """Verifica se um usuário existe e se a senha está correta."""
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user: schemas.UserCreate, role: schemas.Role = schemas.Role.USER):
    """Cria um novo usuário no banco de dados."""
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- CRUD de Produto ---

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_code(db: Session, code: str):
    return db.query(models.Product).filter(models.Product.code == code).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product_update.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
def create_order(db: Session, user_id: int, items_in: List[schemas.OrderItemCreate]) -> models.Order:
    """
    Cria um novo pedido no banco de dados.
    """
    total_amount = 0
    order_items = []

    # Calcula o valor total e prepara os itens do pedido
    for item_in in items_in:
        product = get_product(db, item_in.product_id)
        if not product:
            # Em uma aplicação real, você poderia lançar uma exceção aqui
            continue
        
        item_price = product.price * item_in.quantity
        total_amount += item_price
        
        order_item = models.OrderItem(
            product_id=item_in.product_id,
            quantity=item_in.quantity,
            price=product.price # Salva o preço unitário no momento da compra
        )
        order_items.append(order_item)

    # Cria a instância do pedido
    db_order = models.Order(
        user_id=user_id,
        total_amount=total_amount,
        items=order_items # Associa os itens ao pedido
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

# --- CRUD de Pedidos ---

def get_order_by_id(db: Session, order_id: int):
    """Busca um único pedido pelo seu ID."""
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    """Busca todos os pedidos, para uso de administradores."""
    return db.query(models.Order).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

def get_orders_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Busca todos os pedidos de um usuário específico."""
    return db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

def create_order(db: Session, order_in: schemas.OrderCreate, user_id: int) -> models.Order:
    """
    Cria um novo pedido de forma transacional e segura.
    - Valida a existência dos produtos.
    - Busca os preços do banco de dados para evitar adulteração.
    - Calcula o valor total.
    - Salva tudo em um único commit.
    """
    total_amount = 0.0
    order_items_to_create = []

    # Validação e cálculo seguro dos itens
    for item_in in order_in.items:
        product = get_product(db, product_id=item_in.product_id)
        if not product:
            # Lança uma exceção que será capturada pela camada da API (router)
            raise ValueError(f"Produto com ID {item_in.product_id} não encontrado.")
        
        item_total_price = product.price * item_in.quantity
        total_amount += item_total_price
        
        order_item = models.OrderItem(
            product_id=item_in.product_id,
            quantity=item_in.quantity,
            price=product.price  # Preço é pego do banco, não da requisição do cliente
        )
        order_items_to_create.append(order_item)

    # Criação do pedido com seus itens
    db_order = models.Order(
        user_id=user_id,
        total_amount=total_amount,
        items=order_items_to_create
    )

    # Operação atômica: adiciona e commita
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order