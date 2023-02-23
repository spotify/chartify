String: TypeAlias = str


class StyleSheet():
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class InlineStyleSheet(StyleSheet):

    """
    Inline style sheet equivalent to ``<style type="text/css">${css}</style>``
    """

    css = Required(String)


class ImportedStyleSheet(StyleSheet):

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    url = Required(String, help="""
    The location of an external stylesheet.
    """)
