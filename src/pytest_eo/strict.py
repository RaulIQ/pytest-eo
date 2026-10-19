"""The locked profile: which tools run, with which bundled configuration."""

from dataclasses import dataclass
from importlib import resources
from typing import final

from pytest_eo.check import (
    Check,
    FlakeCheck,
    MypyCheck,
    RuffCheck,
    RuffFormatCheck,
)
from pytest_eo.command import PythonModule
from pytest_eo.project import Project


def _bundled(name: str) -> str:
    return str(resources.files("pytest_eo") / "config" / name)


@final
@dataclass(frozen=True, slots=True)
class Strict:
    """ruff (all rules), ruff format, ``mypy --strict`` and pyeo over a project."""

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
        flake_skipped = (
            ("--extend-exclude", ",".join(self.project.excludes()))
            if self.project.excludes()
            else ()
        )
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
            FlakeCheck(
                PythonModule(
                    "flake8",
                    ("--config", _bundled("flake8.ini"), *flake_skipped, *paths),
                    root,
                ),
            ),
        )
