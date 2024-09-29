from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
from sqlalchemy.types import DateTime
from datetime import datetime

from uuid import uuid4

from _types import OrderStatus


class Base(MappedAsDataclass, DeclarativeBase):
    ...


class Product(Base):
    __tablename__ = "Product"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str]
    amount_in_stock: Mapped[int] = mapped_column(default=0)


class Order(Base):

    __tablename__ = "Order"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int)
    created_at: Mapped[DateTime] = mapped_column(default=datetime.now())
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.IN_PROGRESS)


class OrderItem(Base):
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int)
    order_id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int)  # TODO: reference
    product_id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int)  # TODO: reference
    amount: Mapped[int] = mapped_column(nullable=False)
