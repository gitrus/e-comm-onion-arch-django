from datetime import datetime
from uuid import UUID

from ninja import Schema
from pydantic import BaseModel, HttpUrl

from e_comm_onion_arch.domain.entities.common import PositiveDecimal
from orders.domain.entities.value_objects import OrderStatus


class AddressScm(BaseModel):
    address_id: UUID
    address_line: str


class ProductSnapshotScm(BaseModel):
    product_id: UUID
    name: str
    version: int
    short_description: str | None = None
    price: PositiveDecimal
    image_url: HttpUrl | None = None


class NewOrderItemScm(BaseModel):
    order_item_id: UUID
    product_snapshot: ProductSnapshotScm
    quantity: int


class OrderItemScm(NewOrderItemScm):
    order_id: UUID


class OrderScm(BaseModel):
    order_id: UUID
    user_id: UUID

    shipping_address: AddressScm
    total_price: PositiveDecimal

    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    order_items: list[OrderItemScm]


class CreateOrderRequest(Schema):
    shipping_address: AddressScm
    order_items: list[NewOrderItemScm]
