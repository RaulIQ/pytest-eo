from pathlib import Path

from hamcrest import assert_that, empty, equal_to

from pytest_eo.project import Project
from tests.support.fake_table import FakeTable


def test_checks_src_and_tests_by_default(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    assert_that(
        Project(FakeTable({}), tmp_path).paths(),
        equal_to(("src", "tests")),
        "Project doesnt check src and tests by default",
    )


def test_checks_the_whole_directory_without_src_or_tests(
    tmp_path: Path,
) -> None:
    assert_that(
        Project(FakeTable({}), tmp_path).paths(),
        equal_to((".",)),
        "Project doesnt check the whole directory without src or tests",
    )


def test_takes_the_configured_paths(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    assert_that(
        Project(FakeTable({"paths": ("lib", "bin")}), tmp_path).paths(),
        equal_to(("lib", "bin")),
        "Project doesnt take the configured paths",
    )


def test_takes_the_configured_excludes(tmp_path: Path) -> None:
    assert_that(
        Project(FakeTable({"exclude": ("gen/",)}), tmp_path).excludes(),
        equal_to(("gen/",)),
        "Project doesnt take the configured excludes",
    )


def test_excludes_nothing_by_default(tmp_path: Path) -> None:
    assert_that(
        Project(FakeTable({"paths": ("lib",)}), tmp_path).excludes(),
        empty(),
        "Project doesnt leave its excludes empty by default",
    )
