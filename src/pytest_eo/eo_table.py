"""The ``[tool.eo]`` table of a ``pyproject.toml``."""

from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.setting import Setting
from pytest_eo.table import Table


@final
@dataclass(frozen=True, slots=True)
class EoTable(Table):
    """Settings read from ``[tool.eo]``; a missing file gives none."""

    _file: Path

    @override
    def strings(self, key: str) -> tuple[str, ...]:
        """Read the list under the key, empty unless the TOML has one."""
        return tuple(
            str(item)
            for listed in Setting(self._file, key)
            if isinstance(listed, list)  # noqa: PEO700 - TOML gives untyped data
            for item in listed
        )

    @override
    def numbers(self, key: str) -> tuple[int, ...]:
        """Read the integer under the key, none unless the TOML has one."""
        return tuple(
            value
            for value in Setting(self._file, key)
            if isinstance(value, int)  # noqa: PEO700 - TOML gives untyped data
        )
