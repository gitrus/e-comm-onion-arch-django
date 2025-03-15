from datetime import datetime
from decimal import Decimal
from uuid import UUID

from e_comm_onion_arch.domain.repositories import BaseRepository
from orders import models as m
from orders.domain.entities.orders import Order, OrderItemBase, OrderStatus
from orders.domain.entities.value_objects import Address
from orders.domain.repositories import IOrderRepo


class OrderRepository(BaseRepository, IOrderRepo):

    async def create(
        self,
        user_uid: UUID,
        shipping_address: Address,
        order_items: list[OrderItemBase],
        total_price: Decimal,
    ) -> Order:
        order = m.Order.objects.create(
            user_id=user_uid,
            shipping_address=shipping_address.dict(),  # Assuming Address is Pydantic model
            total_price=total_price,
            status=OrderStatus.PENDING.value,
        )
        order_items_list = [
            m.OrderItem(
                order=order,
                product_snapshot=m.ProductSnapshot.objects.get(
                    id=item.product_snapshot.product_id
                ),
                quantity=item.quantity,
            )
            for item in order_items
        ]

        m.OrderItem.objects.bulk_create(order_items_list)

        return order

    async def get_by_id(self, order_id: UUID) -> Order:
        try:
            order = m.Order.objects.get(id=order_id)
            return order
        except m.Order.DoesNotExist:
            raise IOrderRepo.OrderNotFoundError()

    async def get_by_user_id(
        self, user_id: UUID, date_range: tuple[datetime, datetime]
    ) -> list[Order]:
        orders = m.Order.objects.filter(user_id=user_id, created_at__range=date_range)
        return list(orders)
