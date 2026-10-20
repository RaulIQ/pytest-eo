"""The error an item raises when its tool found violations."""

from typing import final


@final
class StyleViolationsError(Exception):
    """Raised by an item when its tool found violations; its args are them."""
