from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


class OrderDetail(SQLModel, table=True):
    order_id: int = Field(default=None, foreign_key="order.id", primary_key=True)
    product_id: int = Field(default=None, foreign_key="product.id", primary_key=True)
    quantity: Optional[int]
    discount: Optional[int]


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    description: Optional[str]
    supplier_id: Optional[int] = Field(default=None, foreign_key="supplier.id")
    orders: List["Order"] = Relationship(
        back_populates="products", link_model=OrderDetail)


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_date: datetime
    products: List[Product] = Relationship(
        back_populates="orders", link_model=OrderDetail)
    customer_id: int = Field(default=None, foreign_key="customer.id")


class Supplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: Optional[str]
    phone: Optional[str]


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birthday: datetime
