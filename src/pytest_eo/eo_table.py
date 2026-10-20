"""The ``[tool.eo]`` table of a ``pyproject.toml``."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.table import Table


@final
@dataclass(frozen=True, slots=True)
class EoTable(Table):
    """Settings read from ``[tool.eo]``; a missing file gives none."""

    file: Path

    @override
    def strings(self, key: str) -> tuple[str, ...]:
        """Read the list under the key, empty unless the TOML has one."""
        if not self.file.is_file():
            return ()
        tool = tomllib.loads(self.file.read_text(encoding="utf-8")).get("tool")
        eo = tool.get("eo") if isinstance(tool, dict) else {}  # noqa: PEO700 - TOML gives untyped data
        listed = eo.get(key) if isinstance(eo, dict) else ()  # noqa: PEO700 - TOML gives untyped data
        entries = listed if isinstance(listed, list) else ()  # noqa: PEO700 - TOML gives untyped data
        return tuple(str(item) for item in entries)
