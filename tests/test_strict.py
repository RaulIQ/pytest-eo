from pathlib import Path

from hamcrest import assert_that, equal_to

from pytest_eo.python_module import PythonModule


def test_strict_profile_source_gives_ruff_no_warning() -> None:
    package = Path(__file__).parent.parent / "src" / "pytest_eo"
    failure = (
        PythonModule(
            "ruff",
            (
                "check",
                "--no-cache",
                "--config",
                str(package / "config" / "ruff.toml"),
                "strict.py",
            ),
            package,
        )
        .run()
        .failure("ruff printed")
    )
    assert_that(
        str(failure).count("warning"),
        equal_to(0),
        "ruff dont stay silent about strict.py",
    )
