#!/usr/bin/env python3
"""Validate Sphinx requirements and synchronize owned GitHub issue sections."""

import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- papyrus:managed:start -->"
END = "<!-- papyrus:managed:end -->"
META = re.compile(r"<!-- papyrus-work (\{[^\n]+\}) -->")
STATUSES = {"open", "partial", "in_progress", "implemented", "verified", "deferred"}


def command(args, *, payload=None, cwd=None):
    result = subprocess.run(
        args, input=json.dumps(payload) if payload is not None else None,
        text=True, capture_output=True, cwd=cwd,
    )

    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())

    return result.stdout


class GitHub:
    def __init__(self):
        self.last_write = 0.0

    def api(self, path, *, method="GET", payload=None):
        args = ["gh", "api", path, "--method", method]
        is_write = method != "GET" and (
            path != "graphql" or payload.get("query", "").lstrip().startswith("mutation")
        )

        if is_write:
            time.sleep(max(0, 1 - (time.monotonic() - self.last_write)))

        if payload is not None:
            args += ["--input", "-"]

        output = command(args, payload=payload)

        if is_write:
            self.last_write = time.monotonic()

        return json.loads(output) if output.strip() else None

    def graphql(self, query, **variables):
        response = self.api("graphql", method="POST", payload={"query": query, "variables": variables})

        if response.get("errors"):
            raise RuntimeError(json.dumps(response["errors"]))

        return response["data"]

    def issues(self, repository):
        pages = json.loads(command([
            "gh", "api", f"repos/{repository}/issues?state=all&per_page=100",
            "--paginate", "--slurp",
        ]))
        return [issue for page in pages for issue in page if "pull_request" not in issue]

    def project(self, config):
        result = self.graphql(
            """query($owner:String!,$number:Int!){
              organization(login:$owner){projectV2(number:$number){
                id url fields(first:100){nodes{
                  ... on ProjectV2Field{id name}
                  ... on ProjectV2SingleSelectField{id name options{id name}}
                }}
              }}
            }""", owner=config["owner"], number=config["number"],
        )["organization"]["projectV2"]

        if not result:
            raise ValueError("Configured GitHub Project does not exist")

        return result

    def project_items(self, project_id):
        cursor = None
        result = {}

        while True:
            page = self.graphql(
                """query($id:ID!,$cursor:String){
                  node(id:$id){... on ProjectV2{
                    items(first:100,after:$cursor){
                      nodes{id content{... on Issue{id}}
                        fieldValues(first:30){nodes{
                          ... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2SingleSelectField{name}}}
                          ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2Field{name}}}
                        }}
                      }
                      pageInfo{hasNextPage endCursor}
                    }
                  }}
                }""", id=project_id, cursor=cursor,
            )["node"]["items"]

            for item in page["nodes"]:
                if (item.get("content") or {}).get("id"):
                    result[item["content"]["id"]] = item

            if not page["pageInfo"]["hasNextPage"]:
                return result

            cursor = page["pageInfo"]["endCursor"]

    def set_field(self, project, item_id, name, value):
        self.set_fields(project, item_id, {name: value})

    def set_fields(self, project, item_id, values):
        variables = {"project": project["id"], "item": item_id}
        declarations = ["$project:ID!", "$item:ID!"]
        mutations = []

        for index, (name, value) in enumerate(values.items()):
            field = next(field for field in project["fields"]["nodes"] if field.get("name") == name)
            encoded = {"text": value}

            if "options" in field:
                option = next((option for option in field["options"] if option["name"] == value), None)

                if option is None:
                    raise ValueError(f"Project field {name} has no option {value}")

                encoded = {"singleSelectOptionId": option["id"]}

            variables[f"field{index}"] = field["id"]
            variables[f"value{index}"] = encoded
            declarations.extend([f"$field{index}:ID!", f"$value{index}:ProjectV2FieldValue!"])
            mutations.append(
                f"field{index}:updateProjectV2ItemFieldValue(input:{{projectId:$project,itemId:$item,"
                f"fieldId:$field{index},value:$value{index}}}){{projectV2Item{{id}}}}"
            )

        if mutations:
            self.graphql(f"mutation({','.join(declarations)}){{{' '.join(mutations)}}}", **variables)


def metadata(body):
    match = META.search(body or "")
    return json.loads(match[1]) if match else None


def replace_managed(body, section):
    if START not in body or END not in body or body.count(START) != 1 or body.count(END) != 1:
        raise ValueError("Managed issue section is missing or ambiguous")

    before, rest = body.split(START, 1)
    _, after = rest.split(END, 1)
    return before + section + after


def fingerprint(item):
    return hashlib.sha256(json.dumps(item, sort_keys=True).encode()).hexdigest()


def export_items(data, config):
    versions = data.get("versions", {})

    if len(versions) != 1:
        raise ValueError("Export must contain exactly one current requirements version")

    needs = next(iter(versions.values()))["needs"]
    items = {}

    for identifier, need in needs.items():
        if need["type"] not in {"fr", "nfr", "task"}:
            continue

        if need.get("priority") not in {"P0", "P1", "P2", "P3"} or need.get("status") not in STATUSES:
            raise ValueError(f"{identifier}: invalid priority or implementation status")

        if not need.get("content", "").strip() or "**Acceptance criteria:**" not in need["content"]:
            raise ValueError(f"{identifier}: acceptance criteria are required")

        is_task = need["type"] == "task"
        component = need.get("component") if is_task else "docs"

        if component not in config["repositories"]:
            raise ValueError(f"{identifier}: invalid component")

        requirements = need.get("implements", []) if is_task else [identifier]
        dependencies = need.get("depends_on", [])

        if is_task:
            if need.get("readiness") not in {"draft", "ready"}:
                raise ValueError(f"{identifier}: readiness must be draft or ready")

            if not requirements or not need.get("validation", "").strip():
                raise ValueError(f"{identifier}: requirements and validation are mandatory")

            if "**Scope:**" not in need["content"]:
                raise ValueError(f"{identifier}: explicit scope is required")

            for target in requirements:
                if target not in needs or needs[target]["type"] not in {"fr", "nfr"}:
                    raise ValueError(f"{identifier}: invalid requirement {target}")

        for target in dependencies:
            if target not in needs or needs[target]["type"] != "task":
                raise ValueError(f"{identifier}: invalid task dependency {target}")

        item = {
            "id": identifier, "kind": "Task" if is_task else "Requirement",
            "repository": f'{config["owner"]}/{component}',
            "title": need["title"], "priority": need["priority"],
            "implementation_status": need["status"],
            "readiness": need.get("readiness") or "draft",
            "requirements": requirements, "dependencies": dependencies,
            "source_path": need["docname"] + ".rst", "content": need["content"],
            "validation": need.get("validation") or "",
        }

        if is_task:
            item["requirement_content"] = {target: needs[target]["content"] for target in requirements}

        item["source_paths"] = sorted({item["source_path"]} | {
            needs[target]["docname"] + ".rst" for target in requirements
        })
        item["fingerprint"] = fingerprint(item)
        items[identifier] = item

    visiting = set()
    visited = set()

    def visit(identifier):
        if identifier in visiting:
            raise ValueError(f"Task dependency cycle at {identifier}")

        if identifier in visited:
            return

        visiting.add(identifier)

        for target in items[identifier]["dependencies"]:
            visit(target)

        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in items:
        visit(identifier)

    return items


def completed(issue):
    return issue["state"] == "closed" and issue.get("state_reason") == "completed"


def desired_status(item, issue, project_item, issues, changed):
    current = None

    if project_item:
        current = next((
            value["name"] for value in project_item["fieldValues"]["nodes"]
            if value.get("field", {}).get("name") == "Status"
        ), None)

    if issue["state"] == "closed":
        return "Done" if completed(issue) else "Blocked"

    if item["kind"] == "Task" and (
        changed or any(label["name"] == "spec-changed" for label in issue.get("labels", []))
    ):
        return "Blocked"

    if current in {"In progress", "In review", "Blocked"}:
        return current

    if item["kind"] != "Task" or item["readiness"] != "ready":
        return "Backlog"

    if any(not completed(issues[target]) for target in item["dependencies"]):
        return "Blocked"

    return "Ready"


def section(item, revision, config, issues):
    info = {key: item[key] for key in (
        "id", "kind", "fingerprint", "requirements", "dependencies", "readiness", "source_paths",
    )}
    info.update({"source_revision": revision, "repository": item["repository"]})
    source = f'https://github.com/{config["source_repository"]}/blob/{revision}/{item["source_path"]}'
    content = item["content"].replace("``", "`")
    content = re.sub(r":need:`([^`]+)`", lambda match: f'[{match[1]}]({issues[match[1]]["html_url"]})'
                     if match[1] in issues else match[1], content)
    content = re.sub(r":doc:`([^`]+)`", lambda match: f'`{match[1]}`', content)
    dependencies = "\n".join(
        f'- {issues[target]["html_url"]}' if target in issues else f"- {target}"
        for target in item["dependencies"]
    ) or "None."
    requirements = ", ".join(
        f'[{target}]({issues[target]["html_url"]})' if target in issues else target
        for target in item["requirements"]
    )
    return (
        f"{START}\n<!-- papyrus-work {json.dumps(info, sort_keys=True)} -->\n"
        f"[Specification]({source}) · **{item['priority']}** · Target branch: `development`\n\n"
        f"Requirements: {requirements}\n\n"
        f"Implementation status in docs: `{item['implementation_status']}`. "
        "This is separate from issue execution status.\n\n"
        f"{content}\n\n"
        f"### Validation\n\n{item['validation'] or 'Track acceptance through linked implementation tasks and evidence.'}\n\n"
        f"### Dependencies\n\n{dependencies}\n\n"
        f"{END}"
    )


def synchronize(items, config, revision, *, apply=False, github=None):
    github = github or GitHub()
    project = github.project(config)
    project_items = github.project_items(project["id"])
    issues = {}

    for component in config["repositories"]:
        repository = f'{config["owner"]}/{component}'

        for issue in github.issues(repository):
            info = metadata(issue.get("body"))

            if not info:
                continue

            identifier = info["id"]

            if identifier in issues:
                raise ValueError(f"Duplicate managed issue ID: {identifier}")

            issues[identifier] = issue

    for identifier, item in items.items():
        if identifier in issues and issues[identifier]["repository_url"].split("/repos/")[-1] != item["repository"]:
            raise ValueError(f"{identifier}: repository changed, migrate the issue explicitly")

        if identifier in issues:
            replace_managed(issues[identifier]["body"], "")

    if not apply:
        for identifier, item in items.items():
            existing = issues.get(identifier)
            action = "create"

            if existing is not None:
                body = replace_managed(existing["body"], section(item, revision, config, issues))
                title = f'[{identifier}] {item["title"]}'
                action = "update" if body != existing["body"] or title != existing["title"] else "keep"

            print(f'{action:6} {item["repository"]:22} {identifier}: {item["title"]}')

        for identifier in sorted(issues.keys() - items.keys()):
            print(f"review removed specification: {identifier} {issues[identifier]['html_url']}")

        return issues

    github.api(f'repos/{config["source_repository"]}/commits/{revision}')

    for component in config["repositories"]:
        repository = f'{config["owner"]}/{component}'
        labels = github.api(f"repos/{repository}/labels?per_page=100")
        existing_names = {label["name"] for label in labels}

        for name, color, description in [
            ("requirement", "5654A8", "Product requirement maintained in the documentation"),
            ("agent-task", "0E8A16", "Bounded task with specification and acceptance checks"),
            ("spec-changed", "D93F0B", "Specification changed after this issue was created"),
        ]:
            if name not in existing_names:
                github.api(f"repos/{repository}/labels", method="POST",
                           payload={"name": name, "color": color, "description": description})

    changed_ids = set()

    for identifier, item in items.items():
        existing = issues.get(identifier)

        if existing and metadata(existing["body"])["fingerprint"] != item["fingerprint"]:
            changed_ids.add(identifier)

        if existing is None:
            body = section(item, revision, config, issues) + "\n\n### Implementation notes\n\n"
            issues[identifier] = github.api(
                f'repos/{item["repository"]}/issues', method="POST",
                payload={"title": f'[{identifier}] {item["title"]}', "body": body,
                         "labels": ["agent-task" if item["kind"] == "Task" else "requirement"]},
            )
            print(f'Created {issues[identifier]["html_url"]}', flush=True)

    for identifier, item in items.items():
        issue = issues[identifier]
        body = replace_managed(issue["body"], section(item, revision, config, issues))

        title = f'[{identifier}] {item["title"]}'

        if body != issue["body"] or title != issue["title"]:
            github.api(f'repos/{item["repository"]}/issues/{issue["number"]}', method="PATCH",
                       payload={"body": body, "title": title})

        if identifier in changed_ids:
            github.api(f'repos/{item["repository"]}/issues/{issue["number"]}/labels',
                       method="POST", payload={"labels": ["spec-changed"]})

        project_item = project_items.get(issue["node_id"])

        if project_item is None:
            project_item = github.graphql(
                """mutation($project:ID!,$issue:ID!){
                  addProjectV2ItemById(input:{projectId:$project,contentId:$issue}){item{id}}
                }""", project=project["id"], issue=issue["node_id"],
            )["addProjectV2ItemById"]["item"]
            project_item["fieldValues"] = {"nodes": []}

        updates = {}

        for name, value in {
            "Work ID": identifier, "Requirement": ", ".join(item["requirements"]),
            "Priority": item["priority"], "Kind": item["kind"],
            "Status": desired_status(item, issue, project_item, issues, identifier in changed_ids),
        }.items():
            current = next((
                field.get("text", field.get("name"))
                for field in project_item["fieldValues"]["nodes"]
                if field.get("field", {}).get("name") == name
            ), None)

            if current != value:
                updates[name] = value

        github.set_fields(project, project_item["id"], updates)

        if item["kind"] == "Task":
            parent = issues[item["requirements"][0]]
            children = github.api(f'repos/{config["source_repository"]}/issues/{parent["number"]}/sub_issues?per_page=100')

            if not any(child["id"] == issue["id"] for child in children):
                github.api(
                    f'repos/{config["source_repository"]}/issues/{parent["number"]}/sub_issues',
                    method="POST", payload={"sub_issue_id": issue["id"]},
                )

            blockers = github.api(
                f'repos/{item["repository"]}/issues/{issue["number"]}/dependencies/blocked_by?per_page=100'
            )

            for target in item["dependencies"]:
                if not any(blocker["id"] == issues[target]["id"] for blocker in blockers):
                    github.api(
                        f'repos/{item["repository"]}/issues/{issue["number"]}/dependencies/blocked_by',
                        method="POST", payload={"issue_id": issues[target]["id"]},
                    )

        print(f'Synchronized {identifier}: {issue["html_url"]}', flush=True)

    for identifier in sorted(issues.keys() - items.keys()):
        print(f"Specification removed, retained for explicit review: {issues[identifier]['html_url']}")

    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["export", "plan", "sync"])
    parser.add_argument("--needs", type=Path, default=ROOT / "_build/needs/needs.json")
    parser.add_argument("--output", type=Path, default=ROOT / "_build/work-items.json")
    args = parser.parse_args()
    config = json.loads((ROOT / "github-project.json").read_text())

    if args.action != "export":
        if args.needs.resolve() != (ROOT / "_build/needs/needs.json").resolve():
            raise ValueError("Synchronization must use the freshly built specification export")

        command(["uv", "run", "--locked", "sphinx-build", "-W", "--keep-going",
                 "-b", "needs", ".", "_build/needs"], cwd=ROOT)

    items = export_items(json.loads(args.needs.read_text()), config)
    revision = command(["git", "rev-parse", "HEAD"], cwd=ROOT).strip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"source_revision": revision, "items": items}, indent=2) + "\n")

    if args.action == "export":
        print(f"Validated {len(items)} work items: {args.output}")
        return

    if args.action == "sync" and command(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise ValueError("Commit the docs before synchronization so issue links identify the exact specification")

    synchronize(items, config, revision, apply=args.action == "sync")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        raise SystemExit(str(error)) from error
