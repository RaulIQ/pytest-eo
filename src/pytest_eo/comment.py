"""One comment of a source file."""

import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import final


@final
@dataclass(frozen=True, slots=True)
class Comment:
    """A comment of a file, and whether it stands above the first code."""

    file: Path
    token: tokenize.TokenInfo
    header: bool
