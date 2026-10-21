import ast
import io
import tokenize

from hamcrest import assert_that, equal_to

from pytest_eo.bodies import Bodies


def test_reports_a_blank_line_as_its_own_plugin() -> None:
    code = "async def trout():\n    await river()\n\n    return 2\n"
    assert_that(
        tuple(
            (line, text.split()[0], plugin)
            for line, _, text, plugin in Bodies(
                ast.parse(code),
                tuple(tokenize.generate_tokens(io.StringIO(code).readline)),
            ).run()
        ),
        equal_to(((3, "BOD100", Bodies),)),
        "a blank line isnt reported by the plugin of bodies",
    )
