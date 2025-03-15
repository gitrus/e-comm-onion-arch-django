from decimal import Decimal
from typing import cast

from e_comm_onion_arch.domain.services import BaseService
from orders.domain.entities.orders import (
    Order,
    OrderItemBase,
    ProductSnapshot,
)
from orders.domain.entities.service_requests import CreateOrderRequest, OrderItemRequest
from orders.domain.entities.value_objects import Address
from orders.domain.repositories import IOrderRepo, IProductSnapshotRepo


class OrderService(BaseService):
    order_repo: IOrderRepo
    product_snapshot_repo: IProductSnapshotRepo

    class OrderShippingAddressError(Exception): ...

    class ProductPriceChangedError(Exception): ...

    async def create_order(self, request: CreateOrderRequest) -> Order:
        self._validate_address(address=request.shipping_address)

        product_snapshots = await self.product_snapshot_repo.get_by_product_ids(
            product_ids=[item.product_id for item in request.order_items]
        )
        self._validate_product_prices(
            order_items=request.order_items, product_snapshots=product_snapshots
        )

        product_id_to_snapshot = {snapshot.product_id: snapshot for snapshot in product_snapshots}
        order_items = [
            OrderItemBase(
                product_snapshot=product_id_to_snapshot[item.product_id],
                quantity=item.quantity,
            )
            for item in request.order_items
        ]
        total_price: Decimal = cast(
            Decimal, sum(snapshot.price for snapshot in product_snapshots)
        )

        order = await self.order_repo.create(
            user_uid=request.user_id,
            shipping_address=request.shipping_address,
            order_items=order_items,
            total_price=total_price,
        )

        return order

    def _validate_address(self, address: Address) -> None:
        if not address.address_line:
            raise self.OrderShippingAddressError(address)

    def _validate_product_prices(
        self,
        order_items: list[OrderItemRequest],
        product_snapshots: list[ProductSnapshot],
    ) -> None:
        order_product_id_to_price = {item.product_id: item.price for item in order_items}
        snapshot_product_id_to_price = {
            snapshot.product_id: snapshot.price for snapshot in product_snapshots
        }

        if order_product_id_to_price != snapshot_product_id_to_price:
            raise self.ProductPriceChangedError()
