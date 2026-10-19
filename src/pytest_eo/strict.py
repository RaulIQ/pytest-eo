"""The locked profile: which tools run, with which bundled configuration."""

from dataclasses import dataclass
from importlib import resources
from typing import final

from pytest_eo.check import Check, MypyCheck, RuffCheck, RuffFormatCheck
from pytest_eo.command import PythonModule
from pytest_eo.project import Project


def _bundled(name: str) -> str:
    return str(resources.files("pytest_eo") / "config" / name)


@final
@dataclass(frozen=True, slots=True)
class Strict:
    """ruff (all rules), ruff format and ``mypy --strict`` over a project."""

    project: Project

    def checks(self) -> tuple[Check, ...]:
        """Build the checks; nothing runs until ``violations()`` is called."""
        root = self.project.root
        paths = self.project.paths()
        skipped = tuple(
            arg
            for pattern in self.project.excludes()
            for arg in ("--extend-exclude", pattern)
        )
        ruff_config = ("--config", _bundled("ruff.toml"), *skipped)
        mypy_skipped = tuple(
            arg for pattern in self.project.excludes() for arg in ("--exclude", pattern)
        )
        return (
            RuffCheck(
                PythonModule(
                    "ruff",
                    (
                        "check",
                        "--output-format",
                        "json",
                        "--no-cache",
                        *ruff_config,
                        *paths,
                    ),
                    root,
                ),
            ),
            RuffFormatCheck(
                PythonModule(
                    "ruff",
                    (
                        "format",
                        "--check",
                        "--output-format",
                        "concise",
                        "--no-cache",
                        *ruff_config,
                        *paths,
                    ),
                    root,
                ),
            ),
            MypyCheck(
                PythonModule(
                    "mypy",
                    (
                        "--strict",
                        "--config-file",
                        _bundled("mypy.ini"),
                        "--output",
                        "json",
                        *mypy_skipped,
                        *paths,
                    ),
                    root,
                ),
            ),
        )
