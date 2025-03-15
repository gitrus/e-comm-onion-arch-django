from decimal import Decimal
from typing import Annotated, TypeAlias

from pydantic import Field

PositiveDecimal: TypeAlias = Annotated[Decimal, Field(..., gt=0, decimal_places=8)]

PositiveInt: TypeAlias = Annotated[int, Field(..., gt=0)]
