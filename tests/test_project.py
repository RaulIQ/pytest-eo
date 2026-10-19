from pathlib import Path

from pytest_eo.project import Project


def test_checks_src_and_tests_by_default(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    assert Project(tmp_path).paths() == ("src", "tests")


def test_checks_the_whole_directory_without_src_or_tests(tmp_path: Path) -> None:
    assert Project(tmp_path).paths() == (".",)


def test_takes_paths_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[tool.eo]\npaths = ["lib"]\n')
    assert Project(tmp_path).paths() == ("lib",)


def test_takes_excludes_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[tool.eo]\nexclude = ["gen/"]\n')
    assert Project(tmp_path).excludes() == ("gen/",)


def test_excludes_nothing_by_default(tmp_path: Path) -> None:
    assert Project(tmp_path).excludes() == ()
