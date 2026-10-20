"""Rules of Angry Tests, which flake8 runs over the test files of pytest."""

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import PurePath
from typing import final

from typing_extensions import override

from pytest_eo.extension import Extension
from pytest_eo.final_assertion import FinalAssertion
from pytest_eo.module_constants import ModuleConstants
from pytest_eo.negative_messages import NegativeMessages


@final
@dataclass(frozen=True, slots=True)
class AngryTests(Extension):
    """Tests that end with their only assertion and share no constants.

    An assertion is a plain ``assert`` or a Hamcrest ``assert_that``; a test
    that ends with ``pytest.raises`` makes its assertion there. Every
    assertion carries a negative message, such as "x doesnt y".
    """

    tree: ast.Module
    filename: str

    @override
    def run(self) -> Iterator[tuple[int, int, str, type[object]]]:
        """Report the tests of a pytest test file that break a rule."""
        if not any(
            PurePath(self.filename).match(pattern)
            for pattern in ("test_*.py", "*_test.py")
        ):
            return
        for rule in (
            FinalAssertion(self.tree),
            ModuleConstants(self.tree),
            NegativeMessages(self.tree),
        ):
            for line, column, text in rule.problems():
                yield line, column, text, AngryTests
