from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquemas de Produto
class ProductBase(BaseModel):
    code: str # 
    product_name: str # 
    unit: str # 
    price: float # 
    tax: Optional[str] = None # 
    section: Optional[str] = None # 

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# Esquemas de Usuário
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True