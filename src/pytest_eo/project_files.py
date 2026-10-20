"""Python files under the checked paths of a project."""

from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.excludes import Excludes
from pytest_eo.files import Files
from pytest_eo.layout import Layout


@final
@dataclass(frozen=True, slots=True)
class ProjectFiles(Files):
    """Python files under the checked paths of a layout, minus its excludes."""

    layout: Layout
    root: Path

    @override
    def files(self) -> tuple[Path, ...]:
        """Sorted ``*.py`` files under the checked paths, minus excludes."""
        found = (
            file
            for path in self.layout.paths()
            for file in (self.root / path).rglob("*.py")
        )
        excludes = Excludes(self.layout.excludes())
        return tuple(
            sorted(
                {
                    file
                    for file in found
                    if file.relative_to(self.root).as_posix() not in excludes
                },
            ),
        )
