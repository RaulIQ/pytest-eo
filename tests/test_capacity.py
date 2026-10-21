import ast

from hamcrest import assert_that, empty, equal_to

from pytest_eo.capacity import Capacity


def test_reports_a_class_with_more_than_four_fields() -> None:
    assert_that(
        Capacity().visit(
            ast.parse(
                "class Hive:\n"
                "    bees: int\n    wax: str\n    honey: float\n"
                "    queen: str\n    keeper: str\n",
            ).body[0],
        ),
        equal_to(
            (
                (
                    1,
                    0,
                    (
                        "ENC100 class must encapsulate one to four attributes, "
                        "not 5"
                    ),
                ),
            ),
        ),
        "a class with five fields isnt reported",
    )


def test_reports_a_class_without_fields() -> None:
    assert_that(
        Capacity().visit(
            ast.parse(
                "class Void:\n    def hum(self):\n        print(1)\n"
            ).body[0],
        ),
        equal_to(
            (
                (
                    1,
                    0,
                    (
                        "ENC100 class must encapsulate one to four attributes, "
                        "not 0"
                    ),
                ),
            ),
        ),
        "a class without fields isnt reported",
    )


def test_passes_a_class_with_four_fields() -> None:
    assert_that(
        Capacity().visit(
            ast.parse(
                "class Nest:\n"
                "    twigs: int\n    eggs: int\n"
                "    def __init__(self, a, b):\n"
                "        self.moss = a\n        self.down = b\n",
            ).body[0],
        ),
        empty(),
        "a class with four fields doesnt pass",
    )


def test_passes_a_protocol() -> None:
    assert_that(
        Capacity().visit(
            ast.parse(
                "class Song(Protocol):\n    def tune(self) -> str: ...\n",
            ).body[0],
        ),
        empty(),
        "a protocol without fields isnt left alone",
    )


def test_ignores_a_node_that_isnt_a_class() -> None:
    assert_that(
        Capacity().visit(ast.parse("def chirp():\n    print(2)\n").body[0]),
        empty(),
        "a function isnt left alone",
    )
