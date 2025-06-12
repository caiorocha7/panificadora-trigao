from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

# Enum para os papéis (roles)
class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

# --- Schemas de Produto (sem alterações) ---
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

# --- Schemas de Usuário (Atualizado) ---
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

# --- Schemas de Autenticação ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[Role] = None