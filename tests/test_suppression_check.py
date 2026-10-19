from pathlib import Path

from pytest_eo.suppression import SuppressionCheck
from tests.fakes import FakeFiles


def source(tmp_path: Path, text: str) -> FakeFiles:
    file = tmp_path / "app.py"
    file.write_text(text, encoding="utf-8")
    return FakeFiles((file,))


def test_passes_a_suppression_with_a_reason(tmp_path: Path) -> None:
    files = source(
        tmp_path, "import os  # noqa: F401 - re-exported for plugins\n"
    )
    assert SuppressionCheck(files, ("TID251",)).violations() == ()


def test_reports_a_suppression_without_a_reason(tmp_path: Path) -> None:
    files = source(tmp_path, "import os  # noqa: F401\n")
    assert SuppressionCheck(files, ()).violations()[0].code == "SUP001"


def test_reports_the_line_of_the_suppression(tmp_path: Path) -> None:
    files = source(tmp_path, "x = 1\nimport os  # noqa: F401\n")
    assert SuppressionCheck(files, ()).violations()[0].line == 2


def test_reports_a_code_that_cannot_be_suppressed(tmp_path: Path) -> None:
    files = source(
        tmp_path, "from unittest import mock  # noqa: TID251 - just once\n"
    )
    assert SuppressionCheck(files, ("TID251",)).violations()[0].code == "SUP002"


def test_reports_a_forbidden_code_among_others(tmp_path: Path) -> None:
    files = source(tmp_path, "import mock  # noqa: F401, TID251 - legacy\n")
    assert SuppressionCheck(files, ("TID",)).violations()[0].code == "SUP002"


def test_accepts_a_reason_after_a_type_ignore(tmp_path: Path) -> None:
    text = (
        "x: int = y  # type: ignore[assignment]  # noqa: F821 - y is injected\n"
    )
    files = source(tmp_path, text)
    assert SuppressionCheck(files, ()).violations() == ()


def test_ignores_noqa_inside_a_string(tmp_path: Path) -> None:
    files = source(tmp_path, 'text = "import os  # noqa: F401"\n')
    assert SuppressionCheck(files, ()).violations() == ()


def test_ignores_comments_without_noqa(tmp_path: Path) -> None:
    files = source(tmp_path, "x = 1  # the answer\n")
    assert SuppressionCheck(files, ()).violations() == ()
