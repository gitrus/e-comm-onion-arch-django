from enum import auto

from .common import AutoName


class TestAutoNameEnum:
    def test_auto_name_enum_ok(self):
        class AutoNamed(AutoName):
            PENDING = auto()
            COMPLETED = auto()
            CANCELLED = auto()

        assert AutoNamed.PENDING == "PENDING"
        assert AutoNamed.COMPLETED == "COMPLETED"
        assert AutoNamed.CANCELLED == "CANCELLED"
