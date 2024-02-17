from abc import abstractmethod
from typing import Any

from meiga import AnyResult, NotImplementedMethodError

from petisco.base.application.use_case.meta_use_case import MetaUseCase


class AsyncUseCase(metaclass=MetaUseCase):
    """
    A base class for creating your async use cases.
    """

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
