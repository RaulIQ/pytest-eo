from hamcrest import assert_that, equal_to

from pytest_eo.tool_failed_error import ToolFailedError


def test_shows_itself_as_a_tool_failure() -> None:
    assert_that(
        str(ToolFailedError("walrus exited with 9: torn")),
        equal_to("tool failure: walrus exited with 9: torn"),
        "the error isnt shown as a tool failure",
    )
