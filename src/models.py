from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column, deferred, relationship
from sqlalchemy.schema import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as pg_UUID, INTEGER, TEXT, VARCHAR
from sqlalchemy.sql import func, text
from sqlalchemy.types import DateTime
import sqlalchemy as sa
from datetime import datetime

from uuid import uuid4, UUID
from _types import OrderStatus


UUID_LENGTH = 5


def _gen_uuid_prefix():
    return str(uuid4())[:UUID_LENGTH]


class BaseModel(DeclarativeBase):
    ...


class Product(BaseModel):
    __tablename__ = "Product"

    id = Column('id', VARCHAR(UUID_LENGTH),
                primary_key=True, default=_gen_uuid_prefix)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True, default='')
    amount_in_stock: Mapped[int] = mapped_column(default=0)

    orders: Mapped[list['Order']] = relationship(
        cascade='all,delete,expunge', back_populates='product', secondary='OrderItem')


class Order(BaseModel):
    __tablename__ = "Order"

    id: Mapped[int] = mapped_column(
        VARCHAR(UUID_LENGTH), primary_key=True, default=_gen_uuid_prefix)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.IN_PROGRESS)

    # order: Mapped['Order'] = relationship(cascade='all,delete,expunge', back_populates='order', secondary='OrderItem')
    # orderItem: Mapped['OrderItem'] = relationship(cascade='all,delete,expunge', back_populates='order')
    product: Mapped['Product'] = relationship(
        back_populates='orders', secondary='OrderItem')


class OrderItem(BaseModel):
    __tablename__ = "OrderItem"

    id = Column("id", VARCHAR(UUID_LENGTH),
                primary_key=True, default=_gen_uuid_prefix)
    # id: Mapped[UUID] = mapped_column(pg_UUID(), init=False, primary_key=True, default=uuid4(), repr=False)
    order_id: Mapped[str] = mapped_column(ForeignKey(
        "Order.id", ondelete='CASCADE', onupdate='CASCADE'))
    product_id: Mapped[str] = mapped_column(ForeignKey(
        "Product.id", ondelete='CASCADE', onupdate='CASCADE'))
    amount: Mapped[int] = mapped_column(nullable=False)
