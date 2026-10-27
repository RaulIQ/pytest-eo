"""The project under check and its settings."""

from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.layout import Layout
from pytest_eo.table import Table


@final
@dataclass(frozen=True, slots=True)
class Project(Layout):
    """A directory checked as its settings say, or as its layout suggests."""

    _table: Table
    _root: Path

    @override
    def paths(self) -> tuple[str, ...]:
        """Directories to check: the configured ones or existing src/tests."""
        return (
            self._table.strings("paths")
            or tuple(
                name
                for name in ("src", "tests")
                if (self._root / name).is_dir()
            )
            or (".",)
        )

    @override
    def excludes(self) -> tuple[str, ...]:
        """Glob patterns to skip, as configured."""
        return self._table.strings("exclude")

    @override
    def depth(self) -> tuple[int, ...]:
        """How deep calls may nest, as configured."""
        return self._table.numbers("max-call-depth")
