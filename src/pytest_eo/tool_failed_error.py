"""The error of a tool that crashed or printed nonsense."""

from typing import final

from typing_extensions import override


@final
class ToolFailedError(RuntimeError):  # noqa: ENC100 - an exception keeps its message in args
    """A tool crashed or printed something we cannot understand."""

    @override
    def __str__(self) -> str:
        """Show the message as a failure of the tool, not of the code."""
        return f"tool failure: {super().__str__()}"
