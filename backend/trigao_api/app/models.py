from sqlalchemy import (Column, Integer, String, Float, Boolean, 
                        DateTime, ForeignKey, Numeric, func)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)

    # Relação: Um usuário pode ter vários pedidos
    orders: Mapped[List["Order"]] = relationship(back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    product_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    unit: Mapped[str] = mapped_column(String(4), nullable=False)
    tax: Mapped[str] = mapped_column(String, nullable=True)
    section: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Relação adicionada para vincular a OrderItem (opcional, mas bom para futuras consultas)
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")

# --- NOVO MODELO: Order ---
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relação: Um pedido pertence a um usuário
    owner: Mapped["User"] = relationship(back_populates="orders")
    # Relação: Um pedido tem múltiplos itens
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

# --- NOVO MODELO: OrderItem ---
class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False) # Preço no momento da compra
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    # Relação: Um item de pedido pertence a um pedido
    order: Mapped["Order"] = relationship(back_populates="items")
    # Relação: Um item de pedido refere-se a um produto
    product: Mapped["Product"] = relationship(back_populates="order_items")