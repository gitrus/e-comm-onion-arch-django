from enum import IntEnum, StrEnum
from typing import Type, TypeVar

ChoiceEnum = TypeVar("ChoiceEnum", bound=StrEnum | IntEnum)


def enum_to_choices(enum: Type[ChoiceEnum]) -> tuple[tuple[str | int, str | int], ...]:
    return tuple((name, enum_value.value) for name, enum_value in enum.__members__.items())
