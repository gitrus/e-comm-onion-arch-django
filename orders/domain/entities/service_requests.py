from uuid import UUID

from pydantic import BaseModel

from e_comm_onion_arch.domain.entities.common import PositiveDecimal
from orders.domain.entities.value_objects import Address


class OrderItemRequest(BaseModel):
    product_id: UUID
    quantity: int
    price: PositiveDecimal


class CreateOrderRequest(BaseModel):
    user_id: UUID
    shipping_address: Address
    order_items: list[OrderItemRequest]
