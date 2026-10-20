from hamcrest import assert_that

from pytest_eo.excludes import Excludes


def test_leaves_out_a_path_that_matches_a_pattern() -> None:
    assert_that(
        "src/gen/table_pb2.py" in Excludes(("*_pb2.py",)),
        "a path that matches a pattern isnt left out",
    )


def test_leaves_out_a_path_inside_a_directory() -> None:
    assert_that(
        "src/gen/deep/table.py" in Excludes(("src/gen/",)),
        "a path inside an excluded directory isnt left out",
    )


def test_keeps_a_path_that_matches_nothing() -> None:
    assert_that(
        "src/general.py" not in Excludes(("src/gen", "*_pb2.py")),
        "a path that matches nothing isnt kept",
    )
