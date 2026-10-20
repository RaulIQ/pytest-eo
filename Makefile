PYEO_REPO := https://github.com/RaulIQ/pyeo
PYEO_BRANCH := integration

.PHONY: check bump-pyeo
check:
	.venv/bin/coverage run -m pytest
	.venv/bin/coverage combine --quiet
	.venv/bin/coverage report
	.venv/bin/pytest --eo --deselect tests/

# Pin eo-styleguide to the latest commit of $(PYEO_BRANCH) in the fork
# and reinstall it: pip keeps the old one when only the hash changes.
bump-pyeo:
	@sha=$$(git ls-remote $(PYEO_REPO) refs/heads/$(PYEO_BRANCH) | cut -f1); \
	test -n "$$sha" || { echo "Cannot find branch $(PYEO_BRANCH) in $(PYEO_REPO)"; exit 1; }; \
	sed -i -E "s#(eo-styleguide @ git\+$(PYEO_REPO)@)[0-9a-f]{40}#\1$$sha#" pyproject.toml; \
	grep -q "$$sha" pyproject.toml || { echo "Cannot update the pin of eo-styleguide in pyproject.toml"; exit 1; }; \
	.venv/bin/pip install -q --force-reinstall --no-deps "eo-styleguide @ git+$(PYEO_REPO)@$$sha"; \
	echo "eo-styleguide is pinned to $$sha"
	$(MAKE) check
