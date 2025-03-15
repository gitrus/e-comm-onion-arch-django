from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from e_comm_onion_arch.domain.entities.common import PositiveDecimal, PositiveInt

from .value_objects import Address, OrderStatus


class ProductSnapshot(BaseModel):
    product_id: UUID
    name: str
    version: int
    price: PositiveDecimal
    short_description: str | None = None
    image_url: HttpUrl | None = None


class OrderItemBase(BaseModel):
    product_snapshot: ProductSnapshot
    quantity: PositiveInt


class OrderItem(OrderItemBase):
    order_item_id: UUID
    order_id: UUID


class OrderInfo(BaseModel):
    order_id: UUID
    user_id: UUID

    shipping_address: Address
    total_price: PositiveDecimal

    status: OrderStatus
    created_at: datetime
    updated_at: datetime


class Order(OrderInfo):
    order_items: list["OrderItem"] = Field(default_factory=list)
