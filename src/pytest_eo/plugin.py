"""The pytest plugin: ``pytest --eo`` adds one test item per aggregated tool."""

from pathlib import Path
from typing import final

import pytest

from pytest_eo.check import Check
from pytest_eo.command import ToolFailedError
from pytest_eo.project import Project
from pytest_eo.strict import Strict


@final
class StyleViolationsError(Exception):
    """Raised by an item when its tool found violations; its args are them."""


@final
class EoItem(pytest.Item):  # noqa: PEO200 - pytest.Item is mutable by design
    """A test that passes when its tool reports nothing."""

    def __init__(self, *, check: Check, **kwargs: object) -> None:
        """Bind the item to one check; pytest requires the super() call."""
        super().__init__(**kwargs)  # type: ignore[arg-type]  # noqa: PEO101
        self._check = check  # noqa: PEO101 - flagged only because of super()

    def runtest(self) -> None:
        """Run the tool; fail with its findings."""
        found = self._check.violations()
        if found:
            raise StyleViolationsError(*found)

    def repr_failure(
        self,
        excinfo: pytest.ExceptionInfo[BaseException],
        style: object = None,  # noqa: ARG002 - signature is fixed by pytest
    ) -> str:
        """Print one violation per line instead of a Python traceback."""
        error = excinfo.value
        if isinstance(error, StyleViolationsError):
            return "\n".join(str(item) for item in error.args)
        if isinstance(error, ToolFailedError):
            return f"tool failure: {error}"
        return str(error)

    def reportinfo(self) -> tuple[Path, int, str]:
        """Show ``eo::<tool>`` as the item location."""
        return self.path, 0, f"eo::{self._check.name}"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register ``--eo``."""
    parser.getgroup("eo").addoption(
        "--eo",
        action="store_true",
        default=False,
        help="also run the strict style gate (ruff, ruff format, mypy --strict)",
    )


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Append one item per tool when ``--eo`` is given."""
    if not config.getoption("--eo"):
        return
    project = Project(Path(config.rootpath))
    items.extend(
        EoItem.from_parent(
            session,
            name=check.name,
            nodeid=f"eo::{check.name}",
            check=check,
        )
        for check in Strict(project).checks()
    )
