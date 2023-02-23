'''
various kinds of layout components
'''


from typing import TypeAlias, Tuple, List, Any
from chartify import Color, Nullable

from abc import ABC, abstractmethod

from bokeh import Optional
from core import UIElement

Auto: TypeAlias = Enum(auto)
Null: TypeAlias = None
Float: TypeAlias = float
Bool: TypeAlias = bool
Int: TypeAlias = int
Str: TypeAlias = str


class LayoutDOM(UIElement):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    width: int | None = Nullable(NonNegative(int))

    height: int | None = Nullable(NonNegative(int))

    min_width = Nullable(NonNegative(int))

    min_height = Nullable(Nonnegative(int))

    margin = Nullable(Any(Int, Tuple(Int, Int), Tuple(Int, Int, Int, Int)))

    width_policy = Any(Auto, Enum(SizingMode), default="auto")

    height_policy = Any(Auto, Enum(SizingMode), default="auto")

    aspect_ratio = Any(Null, Auto, Float)

    flow_mode = Enum(FlowMode, default="block")

    sizing_mode = Nullable(Enum(SizingMode))

    align = Any(Auto, Enum(Align), Tuple(
        Enum(Align), Enum(Align)), default="auto")

    css_class = List(str)

    resizable = Any(Bool, Enum(Dimensions), default=False)


