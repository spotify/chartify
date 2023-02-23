from cssutils import cssstylesheets #  to add the abstraction of stylesheets

class UIElement:

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        