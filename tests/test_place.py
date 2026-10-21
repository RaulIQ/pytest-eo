from hamcrest import assert_that, equal_to

from pytest_eo.place import Place


def test_shows_itself_as_path_line_and_column() -> None:
    assert_that(
        str(Place("lib/heron.py", 31, 9)),
        equal_to("lib/heron.py:31:9"),
        "a place isnt shown as path, line and column",
    )
