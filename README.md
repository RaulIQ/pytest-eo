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
