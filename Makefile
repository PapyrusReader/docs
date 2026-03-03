.PHONY: help install install-dev serve build clean lint

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

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
