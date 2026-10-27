"""Settings of the gate, as this package sees them."""

from typing import Protocol


class Table(Protocol):
    """Settings a project gives the gate, by key."""

    def strings(self, key: str) -> tuple[str, ...]:
        """Return the strings listed under the key, or none without them."""
        ...

    def numbers(self, key: str) -> tuple[int, ...]:
        """Return the integer set under the key, or none without one."""
        ...
