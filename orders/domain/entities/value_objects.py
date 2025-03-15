from enum import auto
from uuid import UUID

from pydantic import BaseModel

from e_comm_onion_arch.domain.entities.auto_name import AutoName


class OrderStatus(AutoName):
    PENDING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

    @classmethod
    def get_transitions(cls) -> dict["OrderStatus", set["OrderStatus"]]:
        return {
            cls.PENDING: {cls.COMPLETED, cls.CANCELLED},
            cls.COMPLETED: set(),
            cls.CANCELLED: set(),
        }

    @classmethod
    def is_transition_allowed(cls, from_status: "OrderStatus", to_status: "OrderStatus") -> bool:
        return to_status in cls.get_transitions()[from_status]


class Address(BaseModel):
    address_id: UUID
    address_line: str
