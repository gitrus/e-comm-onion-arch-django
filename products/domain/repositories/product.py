from abc import abstractmethod
from uuid import UUID

from e_comm_onion_arch.domain.repositories import BaseRepoInterface
from e_comm_onion_arch.domain.repositories.interface import BaseRepoNotFoundError
from products.domain.entities import Product


class IProductRepo(BaseRepoInterface):
    class ProductNotFoundError(BaseRepoNotFoundError): ...

    @abstractmethod
    async def get_by_product_ids(
        self,
        product_ids: list[UUID],
    ) -> list[Product]: ...
