from hamcrest import assert_that, equal_to

from pytest_eo.place import Place
from pytest_eo.violation import Violation


def test_shows_its_place_tool_code_and_message() -> None:
    assert_that(
        str(Violation("ruff", "E711", Place("lib/stork.py", 8, 3), "no None")),
        equal_to("lib/stork.py:8:3: [ruff:E711] no None"),
        "a violation isnt shown with its place, tool, code and message",
    )
