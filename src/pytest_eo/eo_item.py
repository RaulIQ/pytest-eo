"""A test item that passes when its tool reports nothing."""

from pathlib import Path
from typing import final

import pytest
from typing_extensions import override

from pytest_eo.check import Check
from pytest_eo.style_violations_error import StyleViolationsError


@final
class EoItem(pytest.Item):  # noqa: PEO200 - pytest.Item is mutable by design
    """A test that passes when its tool reports nothing."""

    def __init__(self, *, check: Check, **kwargs: object) -> None:
        """Bind the item to one check; pytest requires the super() call."""
        super().__init__(**kwargs)  # type: ignore[arg-type]  # noqa: PEO101 - pytest needs it
        self._check = check  # noqa: PEO101 - flagged only because of super()

    @override
    def runtest(self) -> None:
        """Run the tool; fail with its findings."""
        found = self._check.violations()
        if found:
            raise StyleViolationsError(*found)

    @override
    def repr_failure(
        self,
        excinfo: pytest.ExceptionInfo[BaseException],
        style: object = None,
    ) -> str:
        """Let the error show itself instead of a Python traceback."""
        return str(excinfo.value)

    @override
    def reportinfo(self) -> tuple[Path, int, str]:
        """Show ``eo::<tool>`` as the item location."""
        return self.path, 0, f"eo::{self._check.name}"
