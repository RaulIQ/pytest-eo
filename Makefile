.PHONY: check coverage
check:
	.venv/bin/pytest --eo

coverage:
	.venv/bin/coverage run -m pytest
	.venv/bin/coverage combine --quiet
	.venv/bin/coverage report
	.venv/bin/coverage xml
