from typing import TypeVar

T = TypeVar("T")


class Required():

    def __init__(self, type_param: T, default: Undefined) -> None:
        super().__init__(type_param, default)
