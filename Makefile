.PHONY: help install install-dev serve build clean lint

install: 
	pip install -e .

install-dev:
	pip install -e ".[dev]"

serve: 
	zensical serve

build:
	zensical build

clean: 
	rm -rf site/

lint: 
	zensical build
	linkchecker site/index.html --check-extern --no-warnings
