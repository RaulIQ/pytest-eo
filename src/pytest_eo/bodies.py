"""Function bodies, which flake8 checks in every file of the project."""

import ast
import tokenize
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.blank_lines import BlankLines
from pytest_eo.extension import Extension
from pytest_eo.inline_comments import InlineComments


@final
@dataclass(frozen=True, slots=True)
class Bodies(Extension):
    """Function bodies packed tight, as Qulice asks of Java methods.

    A blank line or a comment inside a body splits it into parts, and a
    method of several parts does too much.
    """

    tree: ast.Module  # noqa: PEO301 - flake8 passes it by this very name
    file_tokens: Sequence[tokenize.TokenInfo]  # noqa: PEO301 - flake8 passes it by this very name

    @override
    def run(self) -> Iterator[tuple[int, int, str, type[object]]]:
        """Report every function body that breaks a rule."""
        for rule in (
            BlankLines(self.tree, self.file_tokens),
            InlineComments(self.tree, self.file_tokens),
        ):
            for line, column, text in rule.problems():
                yield line, column, text, Bodies
