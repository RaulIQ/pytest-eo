from pathlib import Path

from hamcrest import assert_that, contains_string

from pytest_eo.bundled import Bundled


def test_points_at_a_configuration_shipped_with_the_package() -> None:
    assert_that(
        Path(str(Bundled("mypy.ini"))).read_text(encoding="utf-8"),
        contains_string("strict = True"),
        "the bundled configuration isnt found",
    )
