from enum import StrEnum
from typing import TypeVar

T = TypeVar("T", bound=str)


class AutoName(StrEnum):
    @staticmethod
    def _generate_next_value_(name: T, start, count, last_values) -> T:
        """enum auto-value = enum member name"""
        return name
