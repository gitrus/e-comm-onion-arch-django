import inspect
from functools import wraps
from types import MethodType
from typing import ParamSpec, TypeVar, cast

from e_comm_onion_arch.domain.repositories.interface import BaseRepoInterface
from e_comm_onion_arch.domain.repositories.metrics import (
    repository_errors_count_metric,
    repository_execution_time_metric,
)

P = ParamSpec("P")
R = TypeVar("R")


class BaseRepository(BaseRepoInterface):
    # TODO: rework it. Take/Generalize code from BaseService

    def __new__(cls, *args, **kwargs) -> "BaseRepository":
        """ "Wrap all public methods with prometheus metrics and logger"""
        instance = super().__new__(*args, **kwargs)
        cls.__wrapper(instance)

        return instance

    @classmethod
    def __wrapper(cls, instance: "BaseRepository") -> None:
        for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
            if name.startswith("_"):
                continue

            wrapped_method = method
            for wrapper in [instance._logger_wrapper, instance._metrics_wrapper]:
                wrapped_method = wrapper(wrapped_method)

            # Set the wrapped method back to the instance
            setattr(instance, name, wrapped_method)

    def _metrics_wrapper(self, func: MethodType) -> MethodType:
        """Wrap method with prometheus metrics"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            method_name = func.__name__
            repository_name = self.__class__.__name__

            with repository_execution_time_metric.labels(repository_name, method_name).time():
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    repository_errors_count_metric.labels(
                        repository_name, method_name, str(exc)
                    ).inc()
                    raise exc

        return cast(MethodType, wrapper)

    def _logger_wrapper(self, func: MethodType) -> MethodType:
        """Wrap method with logger"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                raise exc

        return cast(MethodType, wrapper)
