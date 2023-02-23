from __future__ import annotations

from typing import Any, TypeVar, Union

T = TypeVar("T", bound=Union[int, float])


class NonNegative():

    def __init__(self, type_param: T, default: Intrinsic) -> None:
        super().__init__(type_param, default=default)
