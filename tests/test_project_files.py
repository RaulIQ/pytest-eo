from pathlib import Path

from pytest_eo.project import Project, ProjectFiles


def tree(tmp_path: Path, *names: str) -> Path:
    for name in names:
        file = tmp_path / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("", encoding="utf-8")
    return tmp_path


def test_finds_python_files_in_the_checked_paths(tmp_path: Path) -> None:
    root = tree(tmp_path, "src/app.py", "src/pkg/core.py")
    found = ProjectFiles(Project(root), root).files()
    assert found == (root / "src/app.py", root / "src/pkg/core.py"), (
        "ProjectFiles doesnt find the python files of the checked paths"
    )


def test_skips_files_that_are_not_python(tmp_path: Path) -> None:
    root = tree(tmp_path, "src/app.py", "src/notes.md")
    assert ProjectFiles(Project(root), root).files() == (
        root / "src/app.py",
    ), "ProjectFiles doesnt skip files that are not python"


def test_skips_excluded_directories(tmp_path: Path) -> None:
    root = tree(tmp_path, "src/app.py", "src/gen/table.py")
    (root / "pyproject.toml").write_text('[tool.eo]\nexclude = ["src/gen/"]\n')
    assert ProjectFiles(Project(root), root).files() == (
        root / "src/app.py",
    ), "ProjectFiles doesnt skip excluded directories"
