from pathlib import Path

from hamcrest import assert_that, equal_to

from pytest_eo.project import Project
from pytest_eo.project_files import ProjectFiles
from tests.support.fake_table import FakeTable


def tree(tmp_path: Path, *names: str) -> Path:
    for name in names:
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("", encoding="utf-8")
    return tmp_path


def test_finds_python_files_in_the_checked_paths(tmp_path: Path) -> None:
    root = tree(tmp_path, "src/app.py", "src/pkg/core.py")
    found = ProjectFiles(Project(FakeTable({}), root), root).files()
    assert_that(
        found,
        equal_to((root / "src/app.py", root / "src/pkg/core.py")),
        "ProjectFiles doesnt find the python files of the checked paths",
    )


def test_skips_files_that_are_not_python(tmp_path: Path) -> None:
    root = tree(tmp_path, "src/app.py", "src/notes.md")
    assert_that(
        ProjectFiles(Project(FakeTable({}), root), root).files(),
        equal_to((root / "src/app.py",)),
        "ProjectFiles doesnt skip files that are not python",
    )


def test_skips_excluded_directories(tmp_path: Path) -> None:
    root = tree(tmp_path, "src/app.py", "src/gen/table.py")
    assert_that(
        ProjectFiles(
            Project(FakeTable({"exclude": ("src/gen/",)}), root),
            root,
        ).files(),
        equal_to((root / "src/app.py",)),
        "ProjectFiles doesnt skip excluded directories",
    )
