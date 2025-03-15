from abc import abstractmethod
from datetime import datetime
from uuid import UUID

from e_comm_onion_arch.domain.entities.common import PositiveDecimal
from e_comm_onion_arch.domain.repositories.interface import (
    BaseRepoInterface,
    BaseRepoNotFoundError,
)
from orders.domain.entities.orders import Order, OrderItemBase
from orders.domain.entities.value_objects import Address


class IOrderRepo(BaseRepoInterface):
    class OrderNotFoundError(BaseRepoNotFoundError): ...

    @abstractmethod
    async def create(
        self,
        user_uid: UUID,
        shipping_address: Address,
        order_items: list[OrderItemBase],
        total_price: PositiveDecimal,
    ) -> Order: ...

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order: ...

    @abstractmethod
    async def get_by_user_id(
        self, user_id: UUID, date_range: tuple[datetime, datetime]
    ) -> list[Order]: ...
