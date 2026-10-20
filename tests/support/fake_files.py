"""Files given directly, instead of searched for in a project."""

from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.files import Files


@final
@dataclass(frozen=True, slots=True)
class FakeFiles(Files):
    """Files given directly, instead of searched for in a project."""

    paths: tuple[Path, ...]

    @override
    def files(self) -> tuple[Path, ...]:
        """Return the given files."""
        return self.paths
