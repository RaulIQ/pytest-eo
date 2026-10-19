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
