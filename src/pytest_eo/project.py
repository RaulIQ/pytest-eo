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

    table: Table
    root: Path

    @override
    def paths(self) -> tuple[str, ...]:
        """Directories to check: the configured ones or existing src/tests."""
        return (
            self.table.strings("paths")
            or tuple(
                name for name in ("src", "tests") if (self.root / name).is_dir()
            )
            or (".",)
        )

    @override
    def excludes(self) -> tuple[str, ...]:
        """Glob patterns to skip, as configured."""
        return self.table.strings("exclude")
