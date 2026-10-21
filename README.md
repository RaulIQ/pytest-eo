# pytest-eo

[![codecov](https://codecov.io/gh/RaulIQ/pytest-eo/graph/badge.svg)](https://codecov.io/gh/RaulIQ/pytest-eo)

`pytest --eo` is a strict quality gate in the spirit of
[Qulice](https://github.com/yegor256/qulice), built from ready-made tools.
The plugin runs the tools, reads their reports, and shows each tool as a
separate test; its own rules cover only tests and suppressions.

| Test              | Tool                                           |
|-------------------|------------------------------------------------|
| `eo::ruff`        | `ruff check`, all rules (`select = ["ALL"]`)   |
| `eo::ruff-format` | `ruff format --check`                          |
| `eo::mypy`        | `mypy --strict`                                |
| `eo::flake8`      | `flake8` with [pyeo](https://pypi.org/project/eo-styleguide/) (Elegant Objects rules) |
| `eo::suppressions`| `# noqa` and `# ruff: ignore` comments         |

The Elegant Objects rules enabled so far, most of them from
[pyeo](https://github.com/blablatdinov/pyeo) and the rest from its sibling
packages:

| Code     | Rule                                         | Package |
|----------|----------------------------------------------|---------|
| `FIN100` | every class is `@final`                      | pyeo    |
| `PEO101` | `__init__` contains only assignments         | pyeo    |
| `PEO102` | `@classmethod` contains only a `cls()` call  | pyeo    |
| `PEO200` | every class is frozen (immutable)            | pyeo    |
| `PEO300` | no class names ending in "-er"               | pyeo    |
| `PEO400` | no static methods                            | pyeo    |
| `PEO500` | no `@property`, a getter in disguise         | pyeo    |
| `PEO601` | no methods starting with `get`               | pyeo    |
| `PEO602` | no getter methods                            | pyeo    |
| `PEO700` | no introspection, casting, or reflection     | pyeo    |
| `NPM100` | no private functions or methods              | [flake8-no-private-methods](https://github.com/blablatdinov/flake8-no-private-methods) |
| `OVR100` | every public method is an `@override` of an interface method | [flake8-override](https://github.com/blablatdinov/flake8-override) |
| `FOC100` | one public class per module                  | [flake8-one-class](https://github.com/blablatdinov/flake8-one-class) |

mypy runs with `explicit-override` and `warn_unreachable` on top of
`--strict`: an `@override` must override a real method, every overriding
method must say so, and code that can never run is an error.
Python 3.11 has no `typing.override`; import it from `typing_extensions`.

The package also brings a flake8 plugin of its own, with rules in the spirit
of "Angry Tests" for the files pytest collects (`test_*.py`, `*_test.py`):

| Code     | Rule                                                     |
|----------|----------------------------------------------------------|
| `TST100` | a test ends with its only assertion, or with `pytest.raises` |
| `TST200` | a test module keeps no constants, except `pytest_plugins` |
| `TST300` | an assertion carries a negative message, such as `"x doesnt y"` |

One more rule of its own covers every file, tests or not:

| Code     | Rule                                                     |
|----------|----------------------------------------------------------|
| `ENC100` | a class encapsulates one to four attributes; a `Protocol` is exempt |

As in Qulice, which rejects plain JUnit assertions, a test asserts through a
Hamcrest matcher, never through a plain `assert`; ruff's `S101` stays on in
tests too. PyHamcrest comes with the package:

```python
from hamcrest import assert_that, equal_to


def test_checks_the_whole_directory_by_default(tmp_path: Path) -> None:
    assert_that(
        Project(EoTable(tmp_path / "pyproject.toml"), tmp_path).paths(),
        equal_to((".",)),
        "Project doesnt check the whole directory by default",
    )
```

A rule may be suppressed on one line only, with a reason:
`# noqa: PEO200 - pytest.Item is mutable by design`, or
`# ruff: ignore[unused-import] - re-exported for plugins`.
`eo::suppressions` enforces it:

| Code     | Rule                                                     |
|----------|----------------------------------------------------------|
| `SUP001` | a suppression gives a reason after ` - `                 |
| `SUP002` | a suppression never names `TID251` (`banned-api`), the ban on mocks |
| `SUP003` | nothing suppresses past one line: no `# ruff: noqa`, `file-ignore` or `disable`, no `# flake8: noqa`, no `# mypy:` comment, no `# type: ignore` above the code |

ruff already rejects a bare `# noqa` (`PGH004`), a bare `# type: ignore`
(`PGH003`) and an unused `# noqa` for its own codes (`RUF100`).

The configuration is bundled with the package (`src/pytest_eo/config/`)
and cannot be overridden by a project. A project may only say what to
check and what to skip:

```toml
[tool.eo]
paths = ["src", "tests"]    # default: src and tests, if they exist
exclude = ["generated/"]
```

## Usage

```sh
pip install 'pytest-eo @ git+https://github.com/RaulIQ/pytest-eo@0.2.0'
pytest --eo
```

Without `--eo` the plugin does nothing. Pin a tag, not a branch: every
version of the rules is a version of the package, so pip installs new rules
only when the tag in the requirement changes.

## Claude Code hooks

This repository runs the gate on every Claude Code session that works in it:
after Claude edits a `.py`, `.toml`, `.ini` or `.cfg` file, and again before
it finishes. When the gate is red, the findings go back to Claude and it has
to fix them. If the gate is still red after one retry, Claude may stop, and
you see a warning instead.

To get the same in another project:

1. Install pytest-eo into the project's `.venv`.
2. Copy `.claude/hooks/eo-gate.sh` into the same place in that project and
   make it executable.
3. Copy the `hooks` block of `.claude/settings.json` into that project's
   `.claude/settings.json`, merging it with what is already there.
4. Commit both files, so everyone who opens the project with Claude Code gets
   the gate, and run `/hooks` once in an open session to load them.

## Development

```sh
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
make check
```

`make check` runs the tests and `pytest --eo` on the plugin itself; Rultor
merges on it. `make coverage` measures lines and branches, counting the
pytest subprocesses of the end-to-end tests too, and writes `coverage.xml`,
which GitHub Actions sends to Codecov on every push and pull request.

pyeo comes from the `integration` branch of the
[RaulIQ/pyeo](https://github.com/RaulIQ/pyeo) fork, pinned by commit.
`make bump-pyeo` pins it to the latest commit of that branch, reinstalls it
and runs `make check`; commit the changed `pyproject.toml` afterwards.

`pyproject.toml` on `main` always says `version = "0.0.0"`; a real version
exists only in a tag. To release, comment in any issue, with the version in
backticks, since Rultor reads nothing else:

```text
@rultor release, tag is `0.3.0`
```

Rultor writes the version into `pyproject.toml`, runs
`make check`, commits the result on a side branch and pushes only the tag.
Every change to the rules or the bundled configuration ships in a release:
raise the minor number for a new or stricter rule and the patch number for a
fix.
