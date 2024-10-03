from pydantic import BaseModel, field_validator, model_validator, Field, ValidationError
from typing import Annotated, Optional
from _types import OrderStatus
import datetime

from models import UUID_LENGTH


class ProductDto(BaseModel):
    name: str
    price: Annotated[float, Field(ge=0.0)]
    description: Optional[str] = None
    amount_in_stock: Annotated[int, Field(ge=0, default=0)]

    # (no need for validations on db side tho)

# class UpdateProductDto(ProductDto): ...


class OrderDto(BaseModel):
    created_at: datetime.datetime
    status: OrderStatus


class CreateOrderDto(BaseModel):
    product_id: Annotated[str, Field(
        min_length=UUID_LENGTH, max_length=UUID_LENGTH)]
    amount: Annotated[int, Field(gt=0)]


# this is client-side dto TODO: rename to updateStatusDto
class UpdateOrderStatus(BaseModel):
    status: OrderStatus
