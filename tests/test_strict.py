from pathlib import Path

from hamcrest import assert_that, equal_to

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
    assert_that(
        output.stderr.count("warning"),
        equal_to(0),
        "ruff dont stay silent about strict.py",
    )
