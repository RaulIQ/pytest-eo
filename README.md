# pytest-eo

`pytest --eo` — строгий барьер качества в духе [Qulice](https://github.com/yegor256/qulice),
собранный из готовых инструментов. Своих правил пока нет: плагин запускает
инструменты, читает их отчёты и показывает каждый инструмент как отдельный тест.

| Тест          | Инструмент                                   |
|---------------|----------------------------------------------|
| `eo::ruff`        | `ruff check`, все правила (`select = ["ALL"]`) |
| `eo::ruff-format` | `ruff format --check`                          |
| `eo::mypy`        | `mypy --strict`                                |

Конфигурация зашита в пакет (`src/pytest_eo/config/`) и не переопределяется
проектом. Проект может задать только, что проверять и что пропускать:

```toml
[tool.eo]
paths = ["src", "tests"]    # по умолчанию: src и tests, если они есть
exclude = ["generated/"]
```

## Использование

```sh
pip install pytest-eo
pytest --eo
```

Без `--eo` плагин ничего не делает.

## Разработка

```sh
python3 -m venv .venv
.venv/bin/pip install -e .
make check    # pytest --eo на самом плагине
```
