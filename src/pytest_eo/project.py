"""The project under check: where its sources are and what to skip."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Project:
    """A directory with an optional ``[tool.eo]`` table in ``pyproject.toml``."""

    root: Path

    def paths(self) -> tuple[str, ...]:
        """Directories to check: ``[tool.eo] paths``, else existing src/tests."""
        configured = self._settings().get("paths")
        if isinstance(configured, list) and configured:
            return tuple(str(item) for item in configured)
        existing = tuple(
            name for name in ("src", "tests") if (self.root / name).is_dir()
        )
        return existing or (".",)

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
