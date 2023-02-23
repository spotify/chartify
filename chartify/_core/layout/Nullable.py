from __future__ import annotations

from typing import Any, TypeVar, Union

T = TypeVar("T")


class Nullable(Union[T, None]):
    def __init__(self, type_param: T, default: Union[T, None] = None) -> None:
        super().__init__(type_param, default=default)
