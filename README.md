# pytest-eo

`pytest --eo` is a strict quality gate in the spirit of
[Qulice](https://github.com/yegor256/qulice), built from ready-made tools.
It has no rules of its own yet: the plugin runs the tools, reads their
reports, and shows each tool as a separate test.

| Test              | Tool                                           |
|-------------------|------------------------------------------------|
| `eo::ruff`        | `ruff check`, all rules (`select = ["ALL"]`)   |
| `eo::ruff-format` | `ruff format --check`                          |
| `eo::mypy`        | `mypy --strict`                                |
| `eo::flake8`      | `flake8` with [pyeo](https://pypi.org/project/eo-styleguide/) (Elegant Objects rules) |

The pyeo rules enabled so far:

| Code     | Rule                                         |
|----------|----------------------------------------------|
| `FIN100` | every class is `@final`                      |
| `PEO101` | `__init__` contains only assignments         |
| `PEO102` | `@classmethod` contains only a `cls()` call  |
| `PEO200` | every class is frozen (immutable)            |
| `PEO400` | no static methods                            |
| `PEO601` | no methods starting with `get`               |
| `PEO602` | no getter methods                            |
| `OVR100` | every public method is an `@override` of an interface method ([flake8-override](https://github.com/blablatdinov/flake8-override)) |

mypy runs with `explicit-override` on top of `--strict`, so an `@override`
must override a real method and every overriding method must say so.
Python 3.11 has no `typing.override`; import it from `typing_extensions`.

A rule may be suppressed on one line only, with a reason:
`# noqa: PEO200 - pytest.Item is mutable by design`.

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
.venv/bin/pip install -e .
make check    # pytest --eo on the plugin itself
```

pyeo comes from the `integration` branch of the
[RaulIQ/pyeo](https://github.com/RaulIQ/pyeo) fork, pinned by commit.
`make bump-pyeo` pins it to the latest commit of that branch, reinstalls it
and runs `make check`; commit the changed `pyproject.toml` afterwards.
