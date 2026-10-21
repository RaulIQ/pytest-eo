"""The error an item raises when its tool found violations."""

from typing import final

from typing_extensions import override


@final
class StyleViolationsError(Exception):  # noqa: ENC100 - an exception keeps its message in args
    """Raised by an item when its tool found violations; its args are them."""

    @override
    def __str__(self) -> str:
        """Show one violation per line."""
        return "\n".join(str(item) for item in self.args)
