"""Options that remember their defaults, instead of parsing anything."""

from dataclasses import dataclass
from typing import final

from typing_extensions import override

from pytest_eo.options import Options


@final
@dataclass(frozen=True, slots=True)
class FakeOptions(Options):
    """Options that remember their defaults, instead of parsing anything."""

    _defaults: dict[str, object]

    @override
    def add_option(self, *args: str, **kwargs: object) -> None:
        """Remember the default of the option under each of its names."""
        self._defaults.update(dict.fromkeys(args, kwargs["default"]))
