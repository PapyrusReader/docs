# Papyrus documentation

Sphinx publishes a user manual and technical specification. Requirements describe
intended capabilities, while implementation notes describe current behavior.
The [Papyrus GitHub Project](https://github.com/orgs/PapyrusReader/projects/1)
tracks requirements and tasks across the component repositories.

Published documentation: <https://docs.papyrus-reader.com/>.

## Setup and preview

Install uv, Python 3.12, and Graphviz (`dot` must be on PATH), then run:

```bash
uv sync --locked --extra dev --python 3.12
make serve
```

Preview at <http://127.0.0.1:8000>. `make build` produces `_build/html/` and treats
Sphinx warnings as failures. `make lint` additionally checks external links.
Feature/fix PRs target the default `development` branch. CI checks PRs and
integration pushes without publishing. When ready, promote `development` to
`master` with a release PR using **Create a merge commit**, then bring `master`
back into `development`. The Deploy workflow builds with the same lock and
publishes GitHub Pages only from `master`, including manual runs. Keep both
long-lived branches and do not squash release promotions.

## Hosting and custom domain

GitHub Pages hosts the documentation independently of the application server.
In this repository's **Settings → Pages**, use **GitHub Actions** as the build
source and set the custom domain to `docs.papyrus-reader.com`.
The DNS record is:

| Type | Name | Target |
| --- | --- | --- |
| CNAME | `docs` | `papyrusreader.github.io` |

Use DNS-only routing while GitHub validates the domain and issues its TLS
certificate, then enable **Enforce HTTPS** in Pages settings. The CNAME target
must not include `/docs` or a URL scheme. Actions deployments use the custom
domain from Pages settings, not a repository `CNAME` file. `html_baseurl` in
`conf.py` sets canonical page URLs to the same HTTPS domain.

After a production deployment, check the homepage, a nested manual page, and
their styles and navigation at the custom domain. DNS and certificate issuance
must finish before HTTPS can be verified.

## Requirements and local agents

Run `make requirements` to validate and export the structured requirements and
tasks, and `make test` to test the synchronization and task eligibility rules.
CI also performs these checks and uploads the generated JSON as an artifact.

With GitHub CLI authenticated for repository and Projects access:

```bash
make project-plan
make project-sync
uv run --locked python scripts/work_issue.py https://github.com/PapyrusReader/docs/issues/NUMBER --launch
```

Synchronization requires committed, pushed documentation. It preserves discussion
outside the managed issue section and does not automatically close requirements.
Local launches claim only Ready tasks with completed dependencies and prepare an
isolated checkout. See [the workflow](implementation/github-workflow.rst) for field
ownership, changed specifications, claim recovery, and PR completion.

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
