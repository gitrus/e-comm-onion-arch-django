from collections.abc import Collection
from typing import ClassVar
from uuid import UUID

from pydantic import TypeAdapter

from e_comm_onion_arch.domain.repositories import BaseRepository
from orders import models as m
from orders.domain.entities.orders import ProductSnapshot
from orders.domain.repositories import IProductSnapshotRepo


class ProductSnapshotRepo(BaseRepository, IProductSnapshotRepo):
    # product_client: ProductClient

    _adapter: ClassVar = TypeAdapter[m.ProductSnapshot]

    async def get_by_product_ids(
        self,
        product_ids: Collection[UUID],
    ) -> list[ProductSnapshot]:
        if len(product_ids) > 1000:
            raise ValueError("Too many product ids")

        unique_product_ids = set(product_ids)
        qs = m.ProductSnapshot.objects.filter(product_id__in=unique_product_ids)

        snapshots = [self._adapter.validate_python(row, from_attributes=True) for row in qs.all()]

        diff = unique_product_ids - {ps.product_id for ps in snapshots}

        if len(diff) == 0:
            return snapshots

        return []
