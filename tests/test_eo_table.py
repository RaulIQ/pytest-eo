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


def test_reads_nothing_without_the_file(tmp_path: Path) -> None:
    assert_that(
        EoTable(tmp_path / "pyproject.toml").strings("paths"),
        empty(),
        "a missing pyproject.toml doesnt read as empty",
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


def test_reads_nothing_from_a_tool_that_isnt_a_table(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('tool = "eo"\n', encoding="utf-8")
    assert_that(
        EoTable(file).strings("paths"),
        empty(),
        "a tool key that isnt a table doesnt read as empty",
    )


def test_reads_nothing_from_an_eo_that_isnt_a_table(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('[tool]\neo = ["lib"]\n', encoding="utf-8")
    assert_that(
        EoTable(file).strings("paths"),
        empty(),
        "an eo key that isnt a table doesnt read as empty",
    )
