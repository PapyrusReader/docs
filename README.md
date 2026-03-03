# Papyrus Documentation

Project documentation for [Papyrus](https://github.com/Eoic/Papyrus) — a cross-platform e-book reading and management application.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

Live preview:

```bash
mkdocs serve
```

Build static site:

```bash
mkdocs build
```

The development server runs at **<http://127.0.0.1:8000>** by default.

## Deployment

Deploy to GitHub pages:

```bash
mkdocs gh-deploy --force
```
