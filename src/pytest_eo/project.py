"""The project under check: where its sources are and what to skip."""

import tomllib
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Protocol, final

from typing_extensions import override


class Layout(Protocol):
    """Which directories of a project to check and which to skip."""

    def paths(self) -> tuple[str, ...]:
        """Directories to check, relative to the project root."""
        ...

    def excludes(self) -> tuple[str, ...]:
        """Glob patterns to skip."""
        ...


@final
@dataclass(frozen=True, slots=True)
class Project(Layout):
    """A directory with an optional ``[tool.eo]`` table in ``pyproject.toml``."""

    root: Path

    @override
    def paths(self) -> tuple[str, ...]:
        """Directories to check: ``[tool.eo] paths``, else existing src/tests."""
        configured = self._settings().get("paths")
        if isinstance(configured, list) and configured:
            return tuple(str(item) for item in configured)
        existing = tuple(
            name for name in ("src", "tests") if (self.root / name).is_dir()
        )
        return existing or (".",)

    @override
    def excludes(self) -> tuple[str, ...]:
        """Glob patterns to skip: ``[tool.eo] exclude``."""
        configured = self._settings().get("exclude")
        if isinstance(configured, list):
            return tuple(str(item) for item in configured)
        return ()

    def _settings(self) -> dict[str, object]:
        file = self.root / "pyproject.toml"
        if not file.is_file():
            return {}
        table = tomllib.loads(file.read_text(encoding="utf-8"))
        tool = table.get("tool", {})
        eo = tool.get("eo", {}) if isinstance(tool, dict) else {}
        return eo if isinstance(eo, dict) else {}


class Files(Protocol):
    """Python files of a project that the gate reads itself."""

    def files(self) -> tuple[Path, ...]:
        """Every file to read, in a stable order."""
        ...


@final
@dataclass(frozen=True, slots=True)
class ProjectFiles(Files):
    """Python files under the checked paths of a layout, minus its excludes."""

    layout: Layout
    root: Path

    @override
    def files(self) -> tuple[Path, ...]:
        """Sorted ``*.py`` files under every checked path that no exclude hides."""
        found = (
            file
            for path in self.layout.paths()
            for file in (self.root / path).rglob("*.py")
        )
        return tuple(sorted({file for file in found if self._kept(file)}))

    def _kept(self, file: Path) -> bool:
        relative = file.relative_to(self.root).as_posix()
        return not any(
            fnmatch(relative, pattern) or relative.startswith(pattern.rstrip("/") + "/")
            for pattern in self.layout.excludes()
        )
