from pydantic import BaseModel, EmailStr, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Item de Pedido ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    price: float
    product: ProductRead
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Pedido ---
class OrderBase(BaseModel):
    pass

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderRead(OrderBase):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItemRead] = []
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Produto ---
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
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Usuário ---
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    role: Role
    model_config = ConfigDict(from_attributes=True)

# --- Schemas de Autenticação ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[Role] = None