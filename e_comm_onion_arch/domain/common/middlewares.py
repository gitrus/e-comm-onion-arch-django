import dataclasses
import functools
from typing import Generator, Protocol, TypeVar

V = TypeVar("V")


class Middleware(Protocol):
    def __call__(self, *args, **kwargs) -> Generator: ...


def middleware_default_throw_propogation(func: Middleware) -> Middleware:
    """Middleware decorator that catches exceptions and propogates them to the next middleware"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            yield from func(*args, **kwargs)
        except Exception:
            raise
        except BaseException:
            raise  # TODO: do something with this type of exceptions

    return wrapper


@dataclasses.dataclass()
class MiddlewaresStack:
    """
    MiddlewaresStack is a stack of middlewares that can be used as context manager.
    It allows to send value through all middlewares and propagate exceptions.
    """

    middlewares: list[Middleware]

    def __enter__(self, **kwargs) -> "MiddlewaresStack":

        self._middleware_gens = list(reversed([m(**kwargs) for m in self.middlewares]))
        [next(m) for m in self._middleware_gens]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self._exception_propagation(exc=exc_val)
        else:
            self._close()

    def send(self, value: V) -> V:
        return self._value_propagation(value=value)

    def _value_propagation(self, value: V) -> V:
        """Propagate value through all middlewares"""
        v = value
        for m in self._middleware_gens:
            v = m.send(v)

        return v

    def _exception_propagation(self, exc: Exception) -> Exception:
        """Propagate value through all middlewares"""
        e = exc
        for m in self._middleware_gens:
            try:
                e = m.throw(e)
            except StopIteration:
                pass
            except Exception as ex:
                e = ex
        else:
            if e != exc:
                raise e from exc
        return e

    def _close(self):
        """Propagate value through all middlewares"""
        for m in self._middleware_gens:
            m.close()
