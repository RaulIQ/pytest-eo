"""Running an external tool: the only place that touches subprocesses."""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Output:
    """What a finished tool printed and how it exited."""

    stdout: str
    stderr: str
    status: int


@final
class ToolFailedError(RuntimeError):
    """A tool crashed or printed something we cannot understand."""


class Command(Protocol):
    """Something that can be run and produces an :class:`Output`."""

    def run(self) -> Output:
        """Run it and return what it printed."""
        ...


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
        done = subprocess.run(  # noqa: S603 - argv is built from fixed tool names
            argv,
            capture_output=True,
            text=True,
            check=False,
            cwd=self.cwd,
        )
        return Output(done.stdout, done.stderr, done.returncode)
