from pathlib import Path

from hamcrest import assert_that, contains_string, empty, equal_to

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
    assert_that(
        SuppressionCheck(files, ("TID251",)).violations(),
        empty(),
        "a suppression with a reason doesnt pass",
    )


def test_reports_a_suppression_without_a_reason(tmp_path: Path) -> None:
    files = source(tmp_path, "import os  # noqa: F401\n")
    assert_that(
        SuppressionCheck(files, ()).violations()[0].code,
        equal_to("SUP001"),
        "a suppression without a reason doesnt fail",
    )


def test_reports_the_line_of_the_suppression(tmp_path: Path) -> None:
    files = source(tmp_path, "x = 1\nimport os  # noqa: F401\n")
    assert_that(
        SuppressionCheck(files, ()).violations()[0].line,
        equal_to(2),
        "the suppression isnt reported on its own line",
    )


def test_reports_a_code_that_cannot_be_suppressed(tmp_path: Path) -> None:
    files = source(
        tmp_path, "from unittest import mock  # noqa: TID251 - just once\n"
    )
    assert_that(
        SuppressionCheck(files, ("TID251",)).violations()[0].code,
        equal_to("SUP002"),
        "a suppressed forbidden code doesnt fail",
    )


def test_reports_a_forbidden_code_among_others(tmp_path: Path) -> None:
    files = source(tmp_path, "import mock  # noqa: F401, TID251 - legacy\n")
    assert_that(
        SuppressionCheck(files, ("TID",)).violations()[0].code,
        equal_to("SUP002"),
        "a forbidden code among others doesnt fail",
    )


def test_accepts_a_reason_after_a_type_ignore(tmp_path: Path) -> None:
    text = (
        "x: int = y  # type: ignore[assignment]  # noqa: F821 - y is injected\n"
    )
    files = source(tmp_path, text)
    assert_that(
        SuppressionCheck(files, ()).violations(),
        empty(),
        "a reason after a type ignore isnt accepted",
    )


def test_ignores_noqa_inside_a_string(tmp_path: Path) -> None:
    files = source(tmp_path, 'text = "import os  # noqa: F401"\n')
    assert_that(
        SuppressionCheck(files, ()).violations(),
        empty(),
        "a noqa inside a string isnt ignored",
    )


def test_ignores_comments_without_noqa(tmp_path: Path) -> None:
    files = source(tmp_path, "x = 1  # the answer\n")
    assert_that(
        SuppressionCheck(files, ()).violations(),
        empty(),
        "a comment without noqa isnt ignored",
    )


def test_reports_a_ruff_ignore_without_a_reason(tmp_path: Path) -> None:
    files = source(tmp_path, "import os  # ruff: ignore[unused-import]\n")
    assert_that(
        SuppressionCheck(files, ()).violations()[0].code,
        equal_to("SUP001"),
        "a ruff ignore without a reason doesnt fail",
    )


def test_passes_a_ruff_ignore_with_a_reason(tmp_path: Path) -> None:
    files = source(
        tmp_path, "import os  # ruff: ignore[unused-import] - for plugins\n"
    )
    assert_that(
        SuppressionCheck(files, ("banned-api",)).violations(),
        empty(),
        "a ruff ignore with a reason doesnt pass",
    )


def test_reports_a_forbidden_name_in_a_ruff_ignore(tmp_path: Path) -> None:
    files = source(tmp_path, "import mock  # ruff: ignore[banned-api] - once\n")
    assert_that(
        SuppressionCheck(files, ("banned",)).violations()[0].code,
        equal_to("SUP002"),
        "a forbidden name in a ruff ignore doesnt fail",
    )


def test_reports_a_forbidden_code_in_a_ruff_ignore(tmp_path: Path) -> None:
    files = source(tmp_path, "import mock  # ruff: ignore[F401, TID251] - x\n")
    assert_that(
        SuppressionCheck(files, ("TID",)).violations()[0].code,
        equal_to("SUP002"),
        "a forbidden code in a ruff ignore doesnt fail",
    )


def test_reports_a_ruff_ignore_on_its_own_line(tmp_path: Path) -> None:
    files = source(
        tmp_path, "# ruff: ignore[banned-api]\nfrom unittest import mock\n"
    )
    assert_that(
        SuppressionCheck(files, ()).violations()[0].line,
        equal_to(1),
        "a ruff ignore on its own line isnt reported",
    )


def test_reports_a_ruff_ignore_without_spaces(tmp_path: Path) -> None:
    files = source(tmp_path, "import os  #ruff:ignore[unused-import]\n")
    assert_that(
        SuppressionCheck(files, ()).violations()[0].code,
        equal_to("SUP001"),
        "a ruff ignore without spaces isnt reported",
    )


def test_quotes_the_ruff_ignore_in_the_message(tmp_path: Path) -> None:
    files = source(tmp_path, "import os  # ruff: ignore[unused-import]\n")
    assert_that(
        SuppressionCheck(files, ()).violations()[0].message,
        contains_string("`# ruff: ignore[unused-import]`"),
        "the message doesnt quote the ruff ignore",
    )


def test_reports_a_file_wide_ruff_noqa(tmp_path: Path) -> None:
    files = source(tmp_path, "# ruff: noqa: TID251 - old code\nimport mock\n")
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a file-wide ruff noqa doesnt fail",
    )


def test_reports_a_blanket_ruff_noqa(tmp_path: Path) -> None:
    files = source(tmp_path, "# ruff: noqa\nimport os\n")
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a blanket ruff noqa doesnt fail",
    )


def test_reports_a_ruff_file_ignore_even_with_a_reason(tmp_path: Path) -> None:
    files = source(
        tmp_path, "# ruff: file-ignore[unused-import] - plugins\nimport os\n"
    )
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a ruff file-ignore with a reason doesnt fail",
    )


def test_reports_a_ruff_range_once(tmp_path: Path) -> None:
    files = source(
        tmp_path,
        "# ruff: disable[unused-import] - plugins\n"
        "import os\n"
        "import re\n"
        "# ruff: enable[unused-import]\n",
    )
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a ruff range isnt reported exactly once",
    )


def test_reports_the_line_of_a_wide_suppression(tmp_path: Path) -> None:
    files = source(tmp_path, '"""Box."""\n\n# ruff:file-ignore[F401]\n')
    assert_that(
        SuppressionCheck(files, ()).violations()[0].line,
        equal_to(3),
        "a wide suppression isnt reported on its own line",
    )


def test_names_the_form_of_a_wide_suppression(tmp_path: Path) -> None:
    files = source(tmp_path, "# ruff: disable[banned-api]\nimport mock\n")
    assert_that(
        SuppressionCheck(files, ()).violations()[0].message,
        contains_string("`# ruff: disable`"),
        "the message doesnt name the form of the wide suppression",
    )


def test_reports_a_file_wide_flake8_noqa(tmp_path: Path) -> None:
    files = source(tmp_path, "# flake8: noqa\nclass Box:\n    pass\n")
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a file-wide flake8 noqa doesnt fail",
    )


def test_reports_a_mypy_ignore_errors(tmp_path: Path) -> None:
    files = source(tmp_path, "# mypy: ignore-errors\ndef size(x):\n    pass\n")
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a mypy ignore-errors doesnt fail",
    )


def test_reports_a_mypy_disable_error_code(tmp_path: Path) -> None:
    files = source(
        tmp_path, '# mypy: disable-error-code="no-untyped-def"\nimport os\n'
    )
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a mypy disable-error-code doesnt fail",
    )


def test_reports_any_inline_mypy_configuration(tmp_path: Path) -> None:
    files = source(tmp_path, "# mypy: allow-untyped-defs\ndef raw(x): ...\n")
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "an inline mypy configuration doesnt fail",
    )


def test_reports_a_type_ignore_at_the_top_of_a_file(tmp_path: Path) -> None:
    files = source(
        tmp_path, "#!/usr/bin/env python\n# type: ignore\nx: int = ''\n"
    )
    assert_that(
        tuple(found.code for found in SuppressionCheck(files, ()).violations()),
        equal_to(("SUP003",)),
        "a type ignore at the top of a file doesnt fail",
    )


def test_ignores_a_type_ignore_below_the_first_code(tmp_path: Path) -> None:
    files = source(tmp_path, '"""Pipe."""\n# type: ignore\nwidth = 12\n')
    assert_that(
        SuppressionCheck(files, ()).violations(),
        empty(),
        "a type ignore below the first code isnt left alone",
    )


def test_names_a_flake8_form_in_the_message(tmp_path: Path) -> None:
    files = source(tmp_path, "#flake8:noqa\nimport os\n")
    assert_that(
        SuppressionCheck(files, ()).violations()[0].message,
        contains_string("`# flake8:noqa`"),
        "the message doesnt name the flake8 form",
    )
