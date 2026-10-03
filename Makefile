.PHONY: install install-dev serve build clean lint

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
