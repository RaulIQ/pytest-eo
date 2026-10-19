from pathlib import Path

from pytest_eo.command import PythonModule


def test_strict_profile_source_gives_ruff_no_warning() -> None:
    package = Path(__file__).parent.parent / "src" / "pytest_eo"
    output = PythonModule(
        "ruff",
        (
            "check",
            "--no-cache",
            "--config",
            str(package / "config" / "ruff.toml"),
            "strict.py",
        ),
        package,
    ).run()
    assert "warning" not in output.stderr, (
        "ruff dont stay silent about strict.py"
    )
