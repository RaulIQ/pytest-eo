"""Running a Python module: the only place that touches subprocesses."""

import subprocess  # ruff: ignore[suspicious-subprocess-import] - the only module that runs external tools
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import final

from typing_extensions import override

from pytest_eo.command import Command
from pytest_eo.output import Output


@final
@dataclass(frozen=True, slots=True)
class PythonModule(Command):
    """``python -m <module> <args>`` in the interpreter that runs pytest."""

    module: str
    args: tuple[str, ...]
    cwd: Path

    @override
    def run(self) -> Output:
        """Run the module and capture its output."""
        argv = (sys.executable, "-m", self.module, *self.args)
        done = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true] - argv is built from fixed tool names
            argv,
            capture_output=True,
            text=True,
            check=False,
            cwd=self.cwd,
        )
        return Output(done.stdout, done.stderr, done.returncode)
