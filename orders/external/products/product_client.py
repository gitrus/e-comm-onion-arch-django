import dataclasses
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Field
from typing_extensions import Annotated

from products.domain.services.products import ProductService


class ProductScm(BaseModel):
    product_id: UUID

    name: str
    short_description: str
    price: Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]
    image_url: AnyUrl

    updated_at: datetime
    created_at: datetime


@dataclasses.dataclass
class ProductClient:
    """
    We try to cut the edge between the module-domain and the external module
     by creating a client that can be replaced by a real client in the future.
    """

    product_service: ProductService

    async def get_products(self, product_ids: list[UUID]) -> list[ProductScm]:
        row_products = await self.product_service.get_by_ids(product_ids=product_ids)

        products = [ProductScm.model_validate(p, from_attributes=True) for p in row_products]

        return products
