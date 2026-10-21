import pytest
from hamcrest import assert_that, equal_to

from pytest_eo.output import Output
from pytest_eo.tool_failed_error import ToolFailedError
from pytest_eo.verified import Verified
from tests.support.fake_command import FakeCommand


def test_passes_the_output_of_an_allowed_status() -> None:
    assert_that(
        Verified(FakeCommand(Output("tidy:3", "", 1)), "kraken", (0, 1)).run(),
        equal_to(Output("tidy:3", "", 1)),
        "the output of an allowed status isnt passed on",
    )


def test_fails_loudly_on_a_status_nobody_expects() -> None:
    command = Verified(FakeCommand(Output("", "boom", 3)), "kraken", (0, 1))
    with pytest.raises(
        ToolFailedError, match=r"kraken exited unexpectedly \(status 3\): boom"
    ):
        command.run()
