from uuid import UUID

from e_comm_onion_arch.domain.services import BaseService
from products.domain.entities import Product
from products.domain.repositories import IProductRepo


class ProductService(BaseService):
    product_repo: IProductRepo

    async def get_by_ids(self, product_ids: list[UUID]) -> list[Product]:
        products = await self.product_repo.get_by_product_ids(product_ids=product_ids)

        return products
