from abc import ABCMeta
from typing import Type


class BaseRepoError(Exception): ...


class BaseRepoNotFoundError(BaseRepoError): ...


class BaseRepoInterface(ABCMeta):
    error_mapping: dict[Type[Exception], BaseRepoError] = {}
