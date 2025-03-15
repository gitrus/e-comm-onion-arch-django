from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl

from e_comm_onion_arch.domain.entities.common import PositiveDecimal


class Product(BaseModel):
    product_id: UUID

    name: str
    short_description: str
    price: PositiveDecimal
    image_url: HttpUrl | None = None

    weight: Annotated[int, Field(ge=0)]  # in grams

    sku: Annotated[str, Field(max_length=50)]
    ean: Annotated[str, Field(min_length=13, max_length=13)]

    created_at: datetime
    updated_at: datetime
