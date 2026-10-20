"""The locked profile: which tools run, with which bundled configuration."""

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.check import Check
from pytest_eo.flake_check import FlakeCheck
from pytest_eo.layout import Layout
from pytest_eo.mypy_check import MypyCheck
from pytest_eo.profile import Profile
from pytest_eo.project_files import ProjectFiles
from pytest_eo.python_module import PythonModule
from pytest_eo.ruff_check import RuffCheck
from pytest_eo.ruff_format_check import RuffFormatCheck
from pytest_eo.suppression_check import SuppressionCheck

# The rule a suppression may never name, by code or by name: the ban on mocks.
UNSUPPRESSIBLE = ("TID251", "banned-api")


def _bundled(name: str) -> str:
    return str(resources.files("pytest_eo") / "config" / name)


@final
@dataclass(frozen=True, slots=True)
class Strict(Profile):
    """ruff, ruff format, ``mypy --strict``, pyeo and suppressions."""

    layout: Layout
    root: Path

    @override
    def checks(self) -> tuple[Check, ...]:
        """Build the checks; nothing runs until ``violations()`` is called."""
        root = self.root
        paths = self.layout.paths()
        skipped = tuple(
            arg
            for pattern in self.layout.excludes()
            for arg in ("--extend-exclude", pattern)
        )
        ruff_config = ("--config", _bundled("ruff.toml"), *skipped)
        flake_skipped = (
            ("--extend-exclude", ",".join(self.layout.excludes()))
            if self.layout.excludes()
            else ()
        )
        mypy_skipped = tuple(
            arg
            for pattern in self.layout.excludes()
            for arg in ("--exclude", pattern)
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
                    (
                        "--config",
                        _bundled("flake8.ini"),
                        *flake_skipped,
                        *paths,
                    ),
                    root,
                ),
            ),
            SuppressionCheck(ProjectFiles(self.layout, root), UNSUPPRESSIBLE),
        )
