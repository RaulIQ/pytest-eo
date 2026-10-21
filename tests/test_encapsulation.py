import ast

from hamcrest import assert_that, equal_to

from pytest_eo.encapsulation import Encapsulation


def test_reports_every_class_beyond_the_limit_where_it_starts() -> None:
    assert_that(
        tuple(
            (line, text.split()[0])
            for line, _, text, _ in Encapsulation(
                ast.parse(
                    "class Den:\n    fox: int\n\n\n"
                    "class Burrow:\n    pass\n\n\n"
                    "class Lair:\n    wolf: int\n    cub: int\n",
                ),
            ).run()
        ),
        equal_to(((5, "ENC100"),)),
        "the class beyond the limit isnt reported where it starts",
    )
