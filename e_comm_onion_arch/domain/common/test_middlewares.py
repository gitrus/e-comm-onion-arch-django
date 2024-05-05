import logging
from typing import Generator

import pytest
from _pytest.logging import LogCaptureFixture

from .middlewares import MiddlewaresStack


class TestMiddlewaresStack:

    def _middleware1(self) -> Generator:
        try:
            logging.info("Middleware1 initialization")
            result = yield None
            logging.info(f"Middleware1 result: {result}")

            yield result + "1"
        except Exception as ex:
            logging.info(f"Middleware1 throw: {ex}")
            raise Exception("middleware_exc") from ex

    # @middleware_default_throw_propogation
    def _middleware2(self) -> Generator:
        logging.info("Middleware2 initialization")
        result = yield None
        logging.info(f"Middleware2 result: {result}")

        yield result + "2"

    def test_propogate_value(self, caplog: LogCaptureFixture) -> None:
        """Test that value is propogated through all middlewares"""
        ss = MiddlewaresStack(middlewares=[self._middleware1, self._middleware2])

        with caplog.at_level(logging.INFO), ss as stack:
            result = stack.send("test")

            assert result == "test21"

        assert caplog.messages == [
            "Middleware2 initialization",
            "Middleware1 initialization",
            "Middleware2 result: test",
            "Middleware1 result: test2",
        ]

    def test_propogate_error(self, caplog: LogCaptureFixture) -> None:
        """Test that value is propogated through all middlewares"""
        ss = MiddlewaresStack(middlewares=[self._middleware1, self._middleware2])

        with caplog.at_level(logging.INFO), pytest.raises(Exception) as e:
            with ss:
                raise Exception("throw")

        assert e.value.args == ("middleware_exc",)

        assert caplog.messages == [
            "Middleware2 initialization",
            "Middleware1 initialization",
            "Middleware1 throw: throw",
        ]
