"""Nesting of calls, which flake8 checks in every file of the project."""

import argparse
import ast
from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.extension import Extension
from pytest_eo.nested_calls import NestedCalls
from pytest_eo.options import Options


@final
@dataclass(frozen=True, slots=True)
class Nesting(Extension):
    """Expressions that nest calls no deeper than the project allows.

    Six levels let ordinary composition through, and a project may set
    its own limit with ``--max-call-depth``.
    """

    tree: ast.Module  # noqa: PEO301 - flake8 passes it by this very name
    options: argparse.Namespace  # noqa: PEO301 - flake8 passes it by this very name

    @classmethod
    def add_options(cls, options: Options) -> None:
        """Register the limit of nesting with flake8."""
        options.add_option(  # noqa: PEO102 - flake8 takes the options of a plugin through this very hook
            "--max-call-depth",
            type=int,
            default=6,
            help="how deep calls may nest inside each other (default: 6)",
        )

    @override
    def run(self) -> Iterator[tuple[int, int, str, type[object]]]:
        """Report every expression that nests calls past the limit."""
        for line, column, text in NestedCalls(
            self.tree,
            self.options.max_call_depth,
        ).problems():
            yield line, column, text, Nesting
