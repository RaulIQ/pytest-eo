"""The error of a tool that crashed or printed nonsense."""

from typing import final


@final
class ToolFailedError(RuntimeError):
    """A tool crashed or printed something we cannot understand."""
