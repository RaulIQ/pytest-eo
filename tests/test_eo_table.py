from pathlib import Path

from hamcrest import assert_that, empty, equal_to

from pytest_eo.eo_table import EoTable


def test_reads_the_strings_listed_under_a_key(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('[tool.eo]\npaths = ["lib", "bin/x"]\n', encoding="utf-8")
    assert_that(
        EoTable(file).strings("paths"),
        equal_to(("lib", "bin/x")),
        "the strings under a key of [tool.eo] arent read",
    )


def test_reads_nothing_without_the_key(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('[tool.eo]\nexclude = ["gen/"]\n', encoding="utf-8")
    assert_that(
        EoTable(file).strings("paths"),
        empty(),
        "a missing key doesnt read as empty",
    )


def test_reads_nothing_from_a_value_that_isnt_a_list(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('[tool.eo]\npaths = "lib"\n', encoding="utf-8")
    assert_that(
        EoTable(file).strings("paths"),
        empty(),
        "a value that isnt a list doesnt read as empty",
    )


def test_reads_the_integer_under_a_key(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text("[tool.eo]\nmax-call-depth = 8\n", encoding="utf-8")
    assert_that(
        EoTable(file).numbers("max-call-depth"),
        equal_to((8,)),
        "the integer under a key of [tool.eo] isnt read",
    )


def test_reads_no_number_from_a_string(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('[tool.eo]\nmax-call-depth = "8"\n', encoding="utf-8")
    assert_that(
        EoTable(file).numbers("max-call-depth"),
        empty(),
        "a string doesnt read as no number",
    )
