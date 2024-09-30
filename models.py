from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column, deferred
from sqlalchemy.ext.hybrid import Comparator, hybrid_property
from sqlalchemy import ColumnElement
from sqlalchemy.schema import Column
from sqlalchemy.dialects.postgresql import UUID as pg_UUID, INTEGER, TEXT, VARCHAR
from sqlalchemy.types import DateTime
import sqlalchemy as sa
from datetime import datetime

from uuid import uuid4, UUID
# import shortuuid

from _types import OrderStatus


UUID_LENGTH = 5

class BaseModel(MappedAsDataclass, DeclarativeBase, kw_only=True):
    ...


class Product(BaseModel):
    __tablename__ = "Product"


    # id = Column(INTEGER, primary_key=True)
    id = Column('id', VARCHAR(UUID_LENGTH), primary_key=True, default=str(uuid4())[:UUID_LENGTH])
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True, default_factory=str)
    amount_in_stock: Mapped[int] = mapped_column(default=0)



class Order(BaseModel):
    __tablename__ = "Order"

    id = Column("id", INTEGER, primary_key=True, autoincrement=True) # better for testing
    # id: Mapped[UUID] = mapped_column(pg_UUID(), init=False, primary_key=True, default=uuid4(), repr=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.IN_PROGRESS)


class OrderItem(BaseModel):
    __tablename__ = "OrderItem"
    
    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        init=False)  # TODO: reference
    product_id: Mapped[int] = mapped_column(
        init=False)  # TODO: reference
    amount: Mapped[int] = mapped_column(nullable=False, default=1)
