from functools import partial, reduce, wraps
from typing import Callable

from e_comm_onion_arch.domain.repositories.interface import BaseRepoInterface
from e_comm_onion_arch.domain.repositories.metrics import (
    repository_errors_count_metric,
    repository_execution_time_metric,
)


class BaseRepository(BaseRepoInterface):
    # TODO: rework it. Take/Generalize code from BaseService

    def __init__(self, *args, **kwargs) -> None:
        """ "Wrap all public methods with prometheus metrics and logger"""
        super().__init__(*args, **kwargs)
        for attr_name, attr in self.__class__.__dict__.items():
            if callable(attr) and not attr_name.startswith("_"):
                wrapped_func = reduce(
                    lambda res, wrapper: wrapper(res),
                    [self._logger_wrapper, self._metrics_wrapper],
                    attr,
                )
                wrapped_func = partial(wrapped_func, self)
                setattr(self, attr_name, wrapped_func)

    def _metrics_wrapper(self, func: Callable) -> Callable:
        """Wrap method with prometheus metrics"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            method_name = func.__name__
            repository_name = self.__class__.__name__
            version = ""  # TODO: add version

            with repository_execution_time_metric.labels(
                repository_name, method_name, version
            ).time():
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    repository_errors_count_metric.labels(
                        repository_name, method_name, str(ex), version
                    ).inc()
                    raise ex

        return wrapper

    def _logger_wrapper(self, func: Callable) -> Callable:
        """Wrap method with logger"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                raise ex

        return wrapper
