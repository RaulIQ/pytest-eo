from pathlib import Path

from hamcrest import assert_that, empty, equal_to

from pytest_eo.project import Project


def test_checks_src_and_tests_by_default(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    assert_that(
        Project(tmp_path).paths(),
        equal_to(("src", "tests")),
        "Project doesnt check src and tests by default",
    )


def test_checks_the_whole_directory_without_src_or_tests(
    tmp_path: Path,
) -> None:
    assert_that(
        Project(tmp_path).paths(),
        equal_to((".",)),
        "Project doesnt check the whole directory without src or tests",
    )


def test_takes_paths_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[tool.eo]\npaths = ["lib"]\n')
    assert_that(
        Project(tmp_path).paths(),
        equal_to(("lib",)),
        "Project doesnt read [tool.eo] paths",
    )


def test_takes_excludes_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[tool.eo]\nexclude = ["gen/"]\n')
    assert_that(
        Project(tmp_path).excludes(),
        equal_to(("gen/",)),
        "Project doesnt read [tool.eo] exclude",
    )


def test_excludes_nothing_by_default(tmp_path: Path) -> None:
    assert_that(
        Project(tmp_path).excludes(),
        empty(),
        "Project doesnt leave its excludes empty by default",
    )
