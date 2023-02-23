from __future__ import annotations


class UndefinedT:

    def __deepcopy__(self) -> UndefinedT:
        return self

    def __str__(self) -> str:
        return "Undefined"

    def __repr__(self) -> str:
        return "Undefined"


Undefined = UndefinedT()


class IntrinsicT:
    """ Indicates usage of the intrinsic default value of a property. """

    def __deepcopy__(self) -> IntrinsicT:
        return self

    def __str__(self) -> str:
        return "Intrinsic"

    def __repr__(self) -> str:
        return "Intrinsic"


Intrinsic = IntrinsicType()
