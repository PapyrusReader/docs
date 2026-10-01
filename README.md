# Papyrus documentation

The documentation site is built with Sphinx.

## Setup

Use Python 3.12 to match the deployment workflow. Install Graphviz and ensure
its `dot` executable is on your `PATH` to render the requirement diagrams.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

Run these commands from the repository root with the virtual environment active.

Live preview:

```bash
make serve
```

Build the static site:

```bash
make build
```

The development server runs at **<http://127.0.0.1:8000>** by default.
The generated site is written to `_build/html/`.

## Deployment

The [Deploy workflow](.github/workflows/deploy.yml) builds the site with Sphinx
and deploys `_build/html/` to GitHub Pages when changes are pushed to `master`.
It can also be run manually from GitHub Actions.
