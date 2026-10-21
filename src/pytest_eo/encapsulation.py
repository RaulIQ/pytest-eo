"""Encapsulation, which flake8 runs over every file of the project."""

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.capacity import Capacity
from pytest_eo.extension import Extension


@final
@dataclass(frozen=True, slots=True)
class Encapsulation(Extension):
    """Classes that encapsulate as little as possible, but something.

    Elegant Objects asks for one to four attributes per class: fewer is a
    bag of procedures, more is a class that does too much.
    """

    tree: ast.Module

    @override
    def run(self) -> Iterator[tuple[int, int, str, type[object]]]:
        """Report every class that holds no attributes or more than four."""
        for node in ast.walk(self.tree):
            for line, column, text in Capacity().visit(node):
                yield line, column, text, Encapsulation
