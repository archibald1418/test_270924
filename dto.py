from pydantic import BaseModel, field_validator, model_validator, Field, ValidationError
from typing import Annotated, Optional 
from _types import OrderStatus
import datetime


class ProductDto(BaseModel):
    name: str
    price: Annotated[float, Field(ge=0.0)]
    description: Optional[str] = None
    amount_in_stock: Annotated[int, Field(gt=0, default=0)]

    # (no need for validations on db side tho)


class OrderDto(BaseModel):
    created_at: datetime.datetime
    status: OrderStatus


class CreateOrder(BaseModel):
    amount: Annotated[int, Field(gt=0)]
    product_id: Annotated[int, Field(ge=0)]


# this is client-side dto TODO: rename to updateStatusDto
class UpdateOrderStatus(BaseModel):
    status: OrderStatus
