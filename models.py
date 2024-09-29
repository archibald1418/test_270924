from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy.types import DateTime
from datetime import datetime

from uuid import uuid4

from _types import OrderStatus


class BaseModel(MappedAsDataclass, DeclarativeBase):
    ...


class Product(BaseModel):
    __tablename__ = "Product"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int, repr=False)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str]
    amount_in_stock: Mapped[int] = mapped_column(default=0)


class Order(BaseModel):
    __tablename__ = "Order"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int, repr=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.IN_PROGRESS)


class OrderItem(BaseModel):
    __tablename__ = "OrderItem"
    
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int, repr=False)
    order_id: Mapped[int] = mapped_column(
        init=False)  # TODO: reference
    product_id: Mapped[int] = mapped_column(
        init=False)  # TODO: reference
    amount: Mapped[int] = mapped_column(nullable=False)
