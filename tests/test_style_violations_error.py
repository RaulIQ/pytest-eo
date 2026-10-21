from hamcrest import assert_that, equal_to

from pytest_eo.place import Place
from pytest_eo.style_violations_error import StyleViolationsError
from pytest_eo.violation import Violation


def test_shows_one_violation_per_line() -> None:
    assert_that(
        str(
            StyleViolationsError(
                Violation("ruff", "F401", Place("lib/kite.py", 4, 1), "unused"),
                Violation(
                    "mypy", "misc", Place("lib/orca.py", 19, 7), "untyped"
                ),
            ),
        ),
        equal_to(
            "lib/kite.py:4:1: [ruff:F401] unused\n"
            "lib/orca.py:19:7: [mypy:misc] untyped",
        ),
        "the violations arent shown one per line",
    )
