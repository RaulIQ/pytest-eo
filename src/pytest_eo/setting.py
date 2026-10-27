"""One value that a project sets in its ``[tool.eo]`` table."""

import tomllib
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Setting(Iterable[object]):
    """The value under one key of ``[tool.eo]``, if the project sets it.

    TOML gives untyped data, so the value comes as it is, and the reader
    decides what it accepts.
    """

    _file: Path
    _key: str

    @override
    def __iter__(self) -> Iterator[object]:
        """Yield the value under the key, or nothing without one."""
        if not self._file.is_file():
            return
        tool = tomllib.loads(self._file.read_text(encoding="utf-8")).get("tool")
        eo = tool.get("eo") if isinstance(tool, dict) else {}  # noqa: PEO700 - TOML gives untyped data
        if isinstance(eo, dict) and self._key in eo:  # noqa: PEO700 - TOML gives untyped data
            yield eo[self._key]
