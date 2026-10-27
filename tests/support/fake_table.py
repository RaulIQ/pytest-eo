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

    _strings: Mapping[str, tuple[str, ...]]
    _numbers: Mapping[str, tuple[int, ...]]

    @override
    def strings(self, key: str) -> tuple[str, ...]:
        """Return the given strings of the key, or none."""
        return self._strings.get(key, ())

    @override
    def numbers(self, key: str) -> tuple[int, ...]:
        """Return the given number of the key, or none."""
        return self._numbers.get(key, ())
