import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from github_work import (
    END, START, GitHub, completed, desired_status, export_items, metadata, replace_managed, section, synchronize,
)
from work_issue import eligible, prepare

CONFIG = {
    "owner": "PapyrusReader", "number": 1, "source_repository": "PapyrusReader/docs",
    "repositories": ["docs", "client", "server"],
}


def requirement():
    return {
        "id": "FR-1_1", "type": "fr", "title": "Registration",
        "status": "partial", "priority": "P0", "docname": "requirements/functional",
        "content": "**Acceptance criteria:**\n\n- Verify email",
    }


def task(identifier="TASK-AUTH-01", dependencies=None):
    return {
        "id": identifier, "type": "task", "title": "Verify sign-in",
        "status": "open", "priority": "P0", "docname": "requirements/functional",
        "content": "**Scope:**\n\nAuth only.\n\n**Acceptance criteria:**\n\n- Reject unverified sign-in",
        "component": "server", "readiness": "ready", "validation": "Focused auth tests",
        "implements": ["FR-1_1"], "depends_on": dependencies or [],
    }


def exported(*entries):
    return {"versions": {"": {"needs": {entry["id"]: entry for entry in entries}}}}


def project_item(status):
    return {"id": "ITEM", "fieldValues": {"nodes": [{"name": status, "field": {"name": "Status"}}]}}


def issue(identifier="TASK-AUTH-01", **overrides):
    item = export_items(exported(requirement(), task(identifier)), CONFIG)[identifier]
    body = section(item, "a" * 40, CONFIG, {})
    result = {
        "id": 1, "node_id": "ISSUE", "number": 1, "state": "open", "state_reason": None,
        "assignees": [], "labels": [], "title": "Task", "body": body,
        "repository_url": "https://api.github.com/repos/PapyrusReader/server",
        "html_url": "https://github.com/PapyrusReader/server/issues/1",
    }
    result.update(overrides)
    return result


class ExportTests(unittest.TestCase):
    def test_exports_requirements_and_tasks_but_not_use_cases(self):
        use_case = {**requirement(), "id": "UC-1_1", "type": "uc"}
        items = export_items(exported(requirement(), task(), use_case), CONFIG)
        self.assertEqual(set(items), {"FR-1_1", "TASK-AUTH-01"})
        self.assertEqual(items["TASK-AUTH-01"]["repository"], "PapyrusReader/server")

    def test_requirement_change_invalidates_task_fingerprint(self):
        data = exported(requirement(), task())
        before = export_items(data, CONFIG)["TASK-AUTH-01"]["fingerprint"]
        data["versions"][""]["needs"]["FR-1_1"]["content"] += "\n- No access token"
        after = export_items(data, CONFIG)["TASK-AUTH-01"]["fingerprint"]
        self.assertNotEqual(before, after)

    def test_missing_acceptance_is_rejected(self):
        data = requirement()
        data["content"] = "Implement something."
        with self.assertRaisesRegex(ValueError, "acceptance"):
            export_items(exported(data), CONFIG)

    def test_unknown_requirement_is_rejected(self):
        data = task()
        data["implements"] = ["FR-99_1"]
        with self.assertRaisesRegex(ValueError, "invalid requirement"):
            export_items(exported(requirement(), data), CONFIG)

    def test_unknown_repository_is_rejected(self):
        data = task()
        data["component"] = "../elsewhere"
        with self.assertRaisesRegex(ValueError, "component"):
            export_items(exported(requirement(), data), CONFIG)

    def test_cycle_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cycle"):
            export_items(exported(
                requirement(), task("TASK-AUTH-01", ["TASK-AUTH-02"]),
                task("TASK-AUTH-02", ["TASK-AUTH-01"]),
            ), CONFIG)

    def test_unknown_dependency_and_missing_validation_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "dependency"):
            export_items(exported(requirement(), task(dependencies=["TASK-MISSING-01"])), CONFIG)
        data = task()
        data["validation"] = ""
        with self.assertRaisesRegex(ValueError, "validation"):
            export_items(exported(requirement(), data), CONFIG)

    def test_ambiguous_versions_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            export_items({"versions": {"old": {}, "new": {}}}, CONFIG)


class SyncTests(unittest.TestCase):
    def test_repeat_sync_preserves_notes_and_does_not_write_unchanged_items(self):
        class FakeGitHub:
            def __init__(self):
                self.stored = None
                self.item = None
                self.writes = []

            def project(self, config):
                return {"id": "PROJECT"}

            def project_items(self, identifier):
                return {"ISSUE": copy.deepcopy(self.item)} if self.item else {}

            def issues(self, repository):
                return [copy.deepcopy(self.stored)] if self.stored and repository.endswith("/docs") else []

            def api(self, path, *, method="GET", payload=None):
                if method == "GET":
                    if "/labels?" in path:
                        return [{"name": name} for name in ["requirement", "agent-task", "spec-changed"]]
                    return {}

                self.writes.append((method, path, payload))

                if method == "POST" and path.endswith("/issues"):
                    self.stored = issue(
                        body=payload["body"], title=payload["title"],
                        repository_url="https://api.github.com/repos/PapyrusReader/docs",
                    )
                elif method == "PATCH":
                    self.stored.update(payload)
                elif path.endswith("/labels"):
                    self.stored["labels"] = [{"name": label} for label in payload["labels"]]
                else:
                    raise AssertionError(path)

                return copy.deepcopy(self.stored)

            def graphql(self, query, **variables):
                self.writes.append(("project-add", variables))
                self.item = {"id": "ITEM", "fieldValues": {"nodes": []}}
                return {"addProjectV2ItemById": {"item": copy.deepcopy(self.item)}}

            def set_fields(self, project, item_id, values):
                if values:
                    self.writes.append(("fields", values))
                    self.item["fieldValues"]["nodes"] = [
                        {"name": value, "field": {"name": name}} for name, value in values.items()
                    ]

        github = FakeGitHub()
        items = export_items(exported(requirement()), CONFIG)
        synchronize(items, CONFIG, "a" * 40, apply=True, github=github)
        github.stored["body"] += "\nHuman acceptance evidence"
        github.writes.clear()
        synchronize(items, CONFIG, "a" * 40, apply=True, github=github)
        self.assertEqual(github.writes, [])
        self.assertIn("Human acceptance evidence", github.stored["body"])
        changed = requirement()
        changed["content"] += "\n- A new criterion"
        synchronize(export_items(exported(changed), CONFIG), CONFIG, "b" * 40, apply=True, github=github)
        self.assertIn("Human acceptance evidence", github.stored["body"])
        self.assertIn({"name": "spec-changed"}, github.stored["labels"])
        self.assertFalse(any(write[0] == "project-add" for write in github.writes))

    def test_project_fields_are_encoded_in_one_mutation(self):
        github = GitHub()
        project = {"id": "PROJECT", "fields": {"nodes": [
            {"id": "STATUS", "name": "Status", "options": [{"id": "READY", "name": "Ready"}]},
            {"id": "WORK", "name": "Work ID"},
        ]}}
        with patch.object(github, "graphql") as graphql:
            github.set_fields(project, "ITEM", {"Status": "Ready", "Work ID": "TASK-AUTH-01"})
            graphql.assert_called_once()
            self.assertEqual(graphql.call_args.kwargs["value0"], {"singleSelectOptionId": "READY"})
            self.assertEqual(graphql.call_args.kwargs["value1"], {"text": "TASK-AUTH-01"})

    def test_replacement_preserves_human_text(self):
        body = f"Human preface\n{START}\nold\n{END}\nHuman notes"
        replacement = f"{START}\nnew\n{END}"
        self.assertEqual(replace_managed(body, replacement),
                         f"Human preface\n{replacement}\nHuman notes")

    def test_missing_or_duplicate_markers_are_rejected(self):
        for body in ["plain body", START + START + END]:
            with self.assertRaises(ValueError):
                replace_managed(body, "new")

    def test_changed_task_blocks_even_while_in_progress(self):
        item = export_items(exported(requirement(), task()), CONFIG)["TASK-AUTH-01"]
        self.assertEqual(desired_status(item, issue(), project_item("In progress"), {}, True), "Blocked")
        self.assertEqual(desired_status(item, issue(), project_item("In progress"), {}, False), "In progress")
        self.assertEqual(desired_status(
            item, issue(labels=[{"name": "spec-changed"}]), project_item("Ready"), {}, False,
        ), "Blocked")

    def test_not_planned_does_not_unblock_dependencies(self):
        parent = issue(state="closed", state_reason="not_planned")
        self.assertFalse(completed(parent))
        item = export_items(exported(requirement(), task()), CONFIG)["TASK-AUTH-01"]
        item["dependencies"] = ["TASK-OTHER-01"]
        self.assertEqual(desired_status(item, issue(), None, {"TASK-OTHER-01": parent}, False), "Blocked")

    def test_closed_issue_is_not_reopened_for_spec_change(self):
        item = export_items(exported(requirement(), task()), CONFIG)["TASK-AUTH-01"]
        self.assertEqual(desired_status(
            item, issue(state="closed", state_reason="completed"), project_item("Done"), {}, True,
        ), "Done")

    def test_manually_blocked_task_stays_blocked(self):
        item = export_items(exported(requirement(), task()), CONFIG)["TASK-AUTH-01"]
        self.assertEqual(desired_status(item, issue(), project_item("Blocked"), {}, False), "Blocked")

    def test_duplicate_ids_fail_before_mutation(self):
        class DuplicateGitHub:
            def project(self, config):
                return {"id": "PROJECT"}

            def project_items(self, identifier):
                return {}

            def issues(self, repository):
                return [issue()]

        with self.assertRaisesRegex(ValueError, "Duplicate"):
            synchronize({}, CONFIG, "a" * 40, apply=True, github=DuplicateGitHub())

    def test_section_can_be_rendered_before_dependencies_exist(self):
        item = export_items(exported(requirement(), task()), CONFIG)["TASK-AUTH-01"]
        item["dependencies"] = ["TASK-OTHER-01"]
        rendered = section(item, "a" * 40, CONFIG, {})
        self.assertIn("TASK-OTHER-01", rendered)
        self.assertEqual(metadata(rendered)["source_revision"], "a" * 40)


class EligibilityTests(unittest.TestCase):
    def test_only_ready_unassigned_tasks_can_run(self):
        current = issue()
        eligible(current, metadata(current["body"]), project_item("Ready"), [])

        for overrides in [
            {"state": "closed"}, {"assignees": [{"login": "someone"}]},
            {"labels": [{"name": "spec-changed"}]},
        ]:
            with self.assertRaises(ValueError):
                eligible(issue(**overrides), metadata(current["body"]), project_item("Ready"), [])

        with self.assertRaises(ValueError):
            eligible(current, metadata(current["body"]), project_item("In progress"), [])

        with self.assertRaises(ValueError):
            eligible(current, {"kind": "Requirement"}, project_item("Ready"), [])

    def test_outside_repository_is_rejected_without_api_access(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            prepare("https://github.com/someone/other/issues/1", Path("/unused"), CONFIG)

    def test_check_only_never_claims_and_detects_stale_specification(self):
        class FakeGitHub:
            source_changed = False

            def api(self, path, **kwargs):
                if kwargs.get("method"):
                    raise AssertionError("Check mode must not mutate")
                if "/contents/" in path:
                    return {"sha": "different" if self.source_changed and "ref=development" in path else "same"}
                if "/dependencies/" in path:
                    return []
                return issue()

            def project(self, config):
                return {"id": "PROJECT"}

            def project_items(self, identifier):
                return {"ISSUE": project_item("Ready")}

            def issues(self, repository):
                return [issue()] if repository.endswith("/server") else []

        github = FakeGitHub()
        self.assertEqual(prepare(
            "https://github.com/PapyrusReader/server/issues/1", Path("/unused"), CONFIG,
            check=True, github=github,
        ), 0)
        github.source_changed = True
        with self.assertRaisesRegex(ValueError, "differs"):
            prepare("https://github.com/PapyrusReader/server/issues/1", Path("/unused"),
                    CONFIG, check=True, github=github)

    def test_duplicate_claim_stops_before_assignment_or_clone(self):
        class ClaimedGitHub:
            def api(self, path, *, method="GET", payload=None):
                if method != "GET":
                    if path.endswith("/git/refs"):
                        raise RuntimeError("Reference already exists")
                    raise AssertionError("No writes are allowed after a failed claim")
                if path == "user":
                    return {"login": "contributor"}
                if "/git/ref/" in path:
                    return {"object": {"sha": "a" * 40}}
                if "/contents/" in path:
                    return {"sha": "same"}
                if "/dependencies/" in path:
                    return []
                return issue()

            def project(self, config):
                return {"id": "PROJECT"}

            def project_items(self, identifier):
                return {"ISSUE": project_item("Ready")}

            def issues(self, repository):
                return [issue()] if repository.endswith("/server") else []

        with tempfile.TemporaryDirectory() as directory, patch("work_issue.command") as command:
            with self.assertRaisesRegex(RuntimeError, "Reference already exists"):
                prepare("https://github.com/PapyrusReader/server/issues/1", Path(directory),
                        CONFIG, github=ClaimedGitHub())
            command.assert_not_called()


if __name__ == "__main__":
    unittest.main()
