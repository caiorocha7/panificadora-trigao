from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False) # Garanta que este campo exista
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user", nullable=False)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    product_name = Column(String, index=True, nullable=False)
    unit = Column(String(4), nullable=False)
    tax = Column(String, nullable=True)
    section = Column(String, nullable=True)
    price = Column(Float, nullable=False)