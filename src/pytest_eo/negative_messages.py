"""TST300: every assertion explains its failure with a negation."""

import ast
import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.message import Message
from pytest_eo.rule import Rule

_NEGATION = re.compile(
    r"\b(?:not|never|no|nothing|cannot|dont|doesnt|didnt|isnt|arent|wasnt"
    r"|werent|wont|cant)\b",
    re.IGNORECASE,
)


@final
@dataclass(frozen=True, slots=True)
class NegativeMessages(Rule):
    """Assertions whose message says what went wrong, such as "x doesnt y"."""

    tree: ast.Module

    @override
    def problems(self) -> Iterator[tuple[int, int, str]]:
        """Report every assertion whose message holds no negation."""
        return (
            (
                line,
                column,
                "TST300 assertion must explain its failure with a negation",
            )
            for node in ast.walk(self.tree)
            for line, column, text in Message().visit(node)
            if not _NEGATION.search(text)
        )
