"""The command-line options of flake8, as a plugin extends them."""

from typing import Protocol


class Options(Protocol):
    """The options of flake8, which a plugin extends with its own."""

    def add_option(self, *args: str, **kwargs: object) -> None:
        """Add one option, given as to ``argparse``."""
        ...
