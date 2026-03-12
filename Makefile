.PHONY: help install install-dev serve build clean lint

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

serve:
	sphinx-autobuild . _build/html --port 8000

build:
	sphinx-build -b html . _build/html

clean:
	rm -rf _build/

lint:
	sphinx-build -b html . _build/html
	linkchecker _build/html/index.html --check-extern --no-warnings
