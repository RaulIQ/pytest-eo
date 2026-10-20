# pytest-eo

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

The pyeo rules enabled so far:

| Code     | Rule                                         |
|----------|----------------------------------------------|
| `FIN100` | every class is `@final`                      |
| `PEO101` | `__init__` contains only assignments         |
| `PEO102` | `@classmethod` contains only a `cls()` call  |
| `PEO200` | every class is frozen (immutable)            |
| `PEO300` | no class names ending in "-er"               |
| `PEO400` | no static methods                            |
| `PEO601` | no methods starting with `get`               |
| `PEO602` | no getter methods                            |
| `OVR100` | every public method is an `@override` of an interface method ([flake8-override](https://github.com/blablatdinov/flake8-override)) |

mypy runs with `explicit-override` on top of `--strict`, so an `@override`
must override a real method and every overriding method must say so.
Python 3.11 has no `typing.override`; import it from `typing_extensions`.

The package also brings a flake8 plugin of its own, with rules in the spirit
of "Angry Tests" for the files pytest collects (`test_*.py`, `*_test.py`):

| Code     | Rule                                                     |
|----------|----------------------------------------------------------|
| `TST100` | a test ends with its only assertion, or with `pytest.raises` |
| `TST200` | a test module keeps no constants, except `pytest_plugins` |
| `TST300` | an assertion carries a negative message, such as `"x doesnt y"` |

As in Qulice, which rejects plain JUnit assertions, a test asserts through a
Hamcrest matcher, never through a plain `assert`; ruff's `S101` stays on in
tests too. PyHamcrest comes with the package:

```python
from hamcrest import assert_that, equal_to


def test_reads_paths(tmp_path: Path) -> None:
    assert_that(
        Project(tmp_path).paths(),
        equal_to((".",)),
        "Project doesnt read paths",
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
pip install pytest-eo
pytest --eo
```

Without `--eo` the plugin does nothing.

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

`make check` runs the tests under coverage and fails below 100% of lines
and branches, counting the pytest subprocesses of the end-to-end tests too;
then it runs `pytest --eo` on the plugin itself, without the tests again.

pyeo comes from the `integration` branch of the
[RaulIQ/pyeo](https://github.com/RaulIQ/pyeo) fork, pinned by commit.
`make bump-pyeo` pins it to the latest commit of that branch, reinstalls it
and runs `make check`; commit the changed `pyproject.toml` afterwards.
