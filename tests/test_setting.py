from pathlib import Path

from hamcrest import assert_that, empty, equal_to

from pytest_eo.setting import Setting


def test_reads_the_value_under_a_key(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text("[tool.eo]\nmax-call-depth = 9\n", encoding="utf-8")
    assert_that(
        tuple(Setting(file, "max-call-depth")),
        equal_to((9,)),
        "the value under a key of [tool.eo] isnt read",
    )


def test_reads_nothing_without_the_file(tmp_path: Path) -> None:
    assert_that(
        tuple(Setting(tmp_path / "pyproject.toml", "paths")),
        empty(),
        "a missing pyproject.toml doesnt read as empty",
    )


def test_reads_nothing_without_the_key(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('[tool.eo]\nexclude = ["gen/"]\n', encoding="utf-8")
    assert_that(
        tuple(Setting(file, "paths")),
        empty(),
        "a missing key doesnt read as empty",
    )


def test_reads_nothing_from_a_tool_that_isnt_a_table(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('tool = "eo"\n', encoding="utf-8")
    assert_that(
        tuple(Setting(file, "paths")),
        empty(),
        "a tool key that isnt a table doesnt read as empty",
    )


def test_reads_nothing_from_an_eo_that_isnt_a_table(tmp_path: Path) -> None:
    file = tmp_path / "pyproject.toml"
    file.write_text('[tool]\neo = ["lib"]\n', encoding="utf-8")
    assert_that(
        tuple(Setting(file, "paths")),
        empty(),
        "an eo key that isnt a table doesnt read as empty",
    )
