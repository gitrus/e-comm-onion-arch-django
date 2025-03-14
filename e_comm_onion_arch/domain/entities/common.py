from decimal import Decimal
from enum import Enum
from typing import Annotated, TypeVar

from pydantic import Field

T = TypeVar("T", bound=str)


class AutoName(str, Enum):
    @staticmethod
    def _generate_next_value_(name: T, start, count, last_values) -> T:
        """enum auto-value = enum member name"""
        return name


PositiveDecimal = Annotated[Decimal, Field(..., gt=0, decimal_places=8)]
