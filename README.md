# Papyrus documentation

Sphinx publishes the product requirements, current architecture, and API reference.
Requirements describe intended capabilities; the implementation chapters describe
current behavior.

## Setup and preview

Install uv, Python 3.12, and Graphviz (`dot` must be on PATH), then run:

```bash
uv sync --locked --extra dev --python 3.12
make serve
```

Preview at <http://127.0.0.1:8000>. `make build` produces `_build/html/` and treats
Sphinx warnings as failures. `make lint` additionally checks external links.
The Deploy workflow builds with the same lock and publishes GitHub Pages on master.

## API snapshot

`_static/openapi.json` is generated from the server revision pinned in
[the CI workflow](.github/workflows/ci.yml). To refresh it from the corresponding
server checkout, run there:

```bash
uv sync --locked
uv run --locked python scripts/export_openapi.py ../docs/_static/openapi.json
uv run --locked python scripts/export_openapi.py ../docs/_static/openapi.json --check
```

The exporter uses deterministic documentation settings and does not start the
application or connect to a database. Update the CI server revision alongside
intentional API snapshot changes; CI checks freshness against that revision.
Deployment-specific API prefixes and debug routes remain documented by each
server's runtime OpenAPI endpoint.

The [Swagger UI](https://swagger.io/docs/open-source-tools/swagger-ui/usage/installation/)
reference uses version-pinned CDN assets and needs network access. The JSON download
remains available without them. Request execution is disabled on the documentation
site; use a running server's API explorer to make requests.
