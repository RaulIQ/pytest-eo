"""Settings given directly, instead of read from a file."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.table import Table


@final
@dataclass(frozen=True, slots=True)
class FakeTable(Table):
    """Settings given directly, instead of read from a file."""

    _entries: Mapping[str, tuple[str, ...]]

    @override
    def strings(self, key: str) -> tuple[str, ...]:
        """Return the given strings of the key, or none."""
        return self._entries.get(key, ())
