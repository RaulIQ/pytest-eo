from hamcrest import assert_that, equal_to

from pytest_eo.output import Output


def test_reads_as_the_lines_of_its_stdout() -> None:
    assert_that(
        tuple(Output("owl:1\nowl:2\n", "hoot", 1)),
        equal_to(("owl:1", "owl:2")),
        "an output doesnt read as the lines of its stdout",
    )


def test_tells_that_it_exited_with_an_expected_status() -> None:
    assert_that(
        Output("", "", 7).exited((0, 7)),
        "an expected status isnt recognized",
    )


def test_tells_that_it_exited_with_another_status() -> None:
    assert_that(
        not Output("", "", 9).exited((0, 7)),
        "an unexpected status isnt told from an expected one",
    )


def test_explains_a_failure_with_its_status_and_stderr() -> None:
    assert_that(
        str(
            Output("", "  disk full \n", 5).failure("lark exited unexpectedly")
        ),
        equal_to(
            "tool failure: lark exited unexpectedly (status 5): disk full"
        ),
        "a failure isnt explained with the status and the stderr",
    )
