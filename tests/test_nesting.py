import argparse
import ast

from hamcrest import assert_that, equal_to

from pytest_eo.nesting import Nesting
from tests.support.fake_options import FakeOptions


def test_reports_nested_calls_as_its_own_plugin() -> None:
    assert_that(
        tuple(
            (line, text.split()[0], plugin)
            for line, _, text, plugin in Nesting(
                ast.parse("osprey = kite(harrier(buzzard()))\n"),
                argparse.Namespace(max_call_depth=2),
            ).run()
        ),
        equal_to(((1, "NST100", Nesting),)),
        "nested calls arent reported by the plugin of nesting",
    )


def test_allows_six_nested_calls_by_default() -> None:
    defaults: dict[str, object] = {}
    Nesting.add_options(FakeOptions(defaults))
    assert_that(
        defaults,
        equal_to({"--max-call-depth": 6}),
        "the plugin of nesting doesnt allow six nested calls by default",
    )
