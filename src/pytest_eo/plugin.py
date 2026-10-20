"""The pytest plugin: ``pytest --eo`` adds one test item per aggregated tool."""

from pathlib import Path

import pytest

from pytest_eo.eo_item import EoItem
from pytest_eo.eo_table import EoTable
from pytest_eo.project import Project
from pytest_eo.strict import Strict


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register ``--eo``."""
    parser.getgroup("eo").addoption(
        "--eo",
        action="store_true",
        default=False,
        help=(
            "also run the strict style gate (ruff, ruff format, mypy --strict)"
        ),
    )


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Append one item per tool when ``--eo`` is given."""
    if not config.getoption("--eo"):
        return
    root = Path(config.rootpath)
    items.extend(
        EoItem.from_parent(
            session,
            name=check.name,
            nodeid=f"eo::{check.name}",
            check=check,
        )
        for check in Strict(
            Project(EoTable(root / "pyproject.toml"), root),
            root,
        ).checks()
    )
