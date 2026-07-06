all: test

install:
	uv sync

clean:
	rm -rf build dist
	find . -type d -name '__pycache__' -not -path './.venv/*' -exec rm -rf {} +

format-style:
	uv run ruff check --fix .
	uv run ruff format .

check-style:
	uv run ruff check .
	uv run ruff format --check .
	uv run yamllint .

test: check-style
	uv run openfisca test --country-package openfisca_czechia openfisca_czechia/tests

build: clean
	@# Build and test the packaged (wheel) version, the same we put in the
	@# hands of users and reusers. `--no-sync` keeps uv from re-syncing the
	@# environment back to the editable install before the test runs.
	uv build
	uv pip install --force-reinstall dist/*.whl
	uv run --no-sync openfisca test --country-package openfisca_czechia openfisca_czechia/tests

serve-local:
	uv run openfisca serve --country-package openfisca_czechia
