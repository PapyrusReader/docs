.PHONY: install install-dev serve build clean lint requirements test project-plan project-sync

install:
	uv sync --locked

install-dev:
	uv sync --locked --extra dev

serve:
	uv run --locked sphinx-autobuild . _build/html --port 8000

build:
	uv run --locked sphinx-build -W --keep-going -b html . _build/html

clean:
	rm -rf _build/

lint: build
	uv run --locked linkchecker _build/html/index.html --check-extern --no-warnings

requirements:
	uv run --locked sphinx-build -W --keep-going -b needs . _build/needs
	uv run --locked python scripts/github_work.py export

test:
	uv run --locked python -m unittest discover -s tests -v

project-plan:
	uv run --locked python scripts/github_work.py plan

project-sync:
	uv run --locked python scripts/github_work.py sync
