from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

# --- Schema de Produto para Leitura Aninhada ---
class ProductRead(BaseModel):
    id: int
    product_name: str
    price: float
    unit: str

    class Config:
        from_attributes = True

# --- Schemas de Item de Pedido ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    price: float
    product: ProductRead # Schema aninhado para mostrar detalhes do produto

    class Config:
        from_attributes = True

# --- Schemas de Pedido ---
class OrderBase(BaseModel):
    pass

# Não criaremos OrderCreate agora, pois a criação será gerenciada no backend
# para calcular o total e garantir a consistência.

class OrderRead(OrderBase):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItemRead] = [] # Lista aninhada de itens do pedido

    class Config:
        from_attributes = True


# --- Schemas Existentes (mantidos para referência) ---
class ProductBase(BaseModel):
    code: str
    product_name: str
    unit: str
    price: float
    tax: Optional[str] = None
    section: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    role: Role
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[Role] = None