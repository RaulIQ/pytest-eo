"""What a finished tool printed and how it exited."""

from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, slots=True)
class Output:
    """What a finished tool printed and how it exited."""

    stdout: str
    stderr: str
    status: int
