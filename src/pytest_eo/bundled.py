"""A configuration file shipped inside this package."""

from dataclasses import dataclass
from importlib import resources
from typing import final

from typing_extensions import override


@final
@dataclass(frozen=True, slots=True)
class Bundled:
    """The path of a locked configuration that the gate hands to a tool."""

    name: str

    @override
    def __str__(self) -> str:
        """Show the path of the file inside the installed package."""
        return str(resources.files("pytest_eo") / "config" / self.name)
