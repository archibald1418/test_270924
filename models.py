from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column, deferred
from sqlalchemy.dialects.postgresql import UUID as pg_UUID
from sqlalchemy.types import DateTime
import sqlalchemy as sa
from datetime import datetime

from uuid import uuid4, UUID

from _types import OrderStatus

class BaseModel(MappedAsDataclass, DeclarativeBase, kw_only=True):
    ...


class Product(BaseModel):
    __tablename__ = "Product"

    id: Mapped[UUID] = mapped_column(pg_UUID(as_uuid=True), init=False, primary_key=True, default=uuid4(), repr=False)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    amount_in_stock: Mapped[int] = mapped_column(default=0)


class Order(BaseModel):
    __tablename__ = "Order"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int, repr=False, deferred=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.IN_PROGRESS)


class OrderItem(BaseModel):
    __tablename__ = "OrderItem"
    
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, default=uuid4().int, repr=False, deferred=True)
    order_id: Mapped[int] = mapped_column(
        init=False)  # TODO: reference
    product_id: Mapped[int] = mapped_column(
        init=False)  # TODO: reference
    amount: Mapped[int] = mapped_column(nullable=False, default=1)
