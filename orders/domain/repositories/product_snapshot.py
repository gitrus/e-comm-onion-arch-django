from abc import abstractmethod
from collections.abc import Collection
from uuid import UUID

from e_comm_onion_arch.domain.repositories import BaseRepoInterface
from e_comm_onion_arch.domain.repositories.interface import BaseRepoNotFoundError
from orders.domain.entities.orders import ProductSnapshot


class IProductSnapshotRepo(BaseRepoInterface):
    class ProductSnapshotNotFoundError(BaseRepoNotFoundError): ...

    @abstractmethod
    async def get_by_product_ids(
        self,
        product_ids: Collection[UUID],
    ) -> list[ProductSnapshot]: ...
