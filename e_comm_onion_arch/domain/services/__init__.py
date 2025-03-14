import dataclasses
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable, Generator, Type

from ..common.middlewares import Middleware, MiddlewaresStack
from .metrics import service_execution_time_metric


@dataclasses.dataclass
class BaseService:
    # TODO: rework it. Take/Generalize code from BaseRepository
    error_mapping: dict[Type[Exception], Type[Exception]] = dataclasses.field(
        default_factory=dict
    )

    @staticmethod
    def __new__(cls, *args, **kwargs):
        """Return instance with all public methods wrapped with middleware wrappers:
        async and sync"""

        cls.ServiceErrorType = type(cls.__name__ + "Error", (Exception,), {})

        middlewares = [
            cls._service_exception_middleware,
            cls._metrics_middleware,
        ]

        instance = super().__new__(cls)
        for attr_name, attr in instance.__dict__.items():
            if callable(attr) and not attr_name.startswith("_"):
                setattr(instance, attr_name, cls._middleware_wrapper(attr, middlewares))

        return instance

    def _service_exception_middleware(self, error_type: Type[Exception]) -> Generator:
        """Middleware that catches exceptions and maps them with error_mapping"""

        try:
            res = yield None
            yield res
        except Exception as ex:
            for error, mapped_error in self.error_mapping.items():
                if isinstance(ex, error):
                    raise mapped_error from ex
            raise self.ServiceErrorType from ex

    def _metrics_middleware(self, **kwargs) -> Generator:
        try:
            service_name = kwargs["service_name"] or self.__class__.__name__
            method_name = kwargs["method_name"]
            version = kwargs["version"]
            metric = service_execution_time_metric.labels(
                service_name=service_name, method_name=method_name, version=version
            )
            with metric.time():
                res = yield None
            yield res
        except Exception:
            raise

    @classmethod
    def _middleware_wrapper(cls, func: Callable, middlewares: list[Middleware]) -> Callable:
        """Wrap method with try-catching and map errors with error_mapping"""

        if iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(*args, **kwargs):
                with MiddlewaresStack(middlewares=middlewares) as md_stack:
                    res = await func(*args, **kwargs)

                    md_stack.send(res)

            return wrapper

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                with MiddlewaresStack(middlewares=middlewares) as md_stack:
                    res = func(*args, **kwargs)

                    md_stack.send(res)

            return wrapper
