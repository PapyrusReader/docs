GitHub project and agent workflow
==================================

The `Papyrus project <https://github.com/orgs/PapyrusReader/projects/1>`_ collects
requirements and implementation work across the organization.

Ownership
---------

The documentation is authoritative for product requirements and acceptance
criteria. Requirement tracking issues live in ``PapyrusReader/docs``.
Implementation task issues belong to the repository that owns the change.
Project status describes work execution, while requirement status describes
implemented and verified product behavior.

.. list-table::
   :header-rows: 1

   * - Repository
     - Owns
   * - client
     - Flutter UI, local persistence, reader integration, and client sync
   * - server
     - API, authentication, PostgreSQL, media, and server sync
   * - reader
     - Reading engines and public reader API
   * - docs
     - Specifications, contracts, user manual, and requirements tooling
   * - website
     - Public website and account-related web entry points
   * - papyrus
     - Workspace tooling and cross-component integration

A requirement may have several tasks. Use cases provide context and are not
automatically converted into duplicate tasks.

Defining executable work
-------------------------

Write ``task`` entries alongside the relevant requirements. Each task needs a
stable ``TASK-AREA-NN`` ID, one owning ``component``, ``priority``, ``readiness``,
``implements`` links, validation instructions, scope, and acceptance criteria.
Use ``depends_on`` for prerequisite tasks.

Keep each task small enough for an independently reviewable pull request. Split
cross-component work into tasks with an agreed contract and explicit dependency
order. When a contract is undecided, create a documentation/design task first.
Keep unresolved implementation tasks out of the Ready queue.

The exporter rejects missing fields, invalid requirement references, invalid task
dependencies, and cycles. The initial authentication tasks demonstrate the format
in :doc:`/requirements/functional`.

Export and synchronize
----------------------

From the docs repository:

.. code-block:: bash

   make requirements
   make test
   make project-plan
   make project-sync

``project-plan`` reads GitHub and previews issue creation and updates.
``project-sync`` writes them and requires a clean, committed docs checkout.
Push the specification commit before synchronization so its source links can be
opened on GitHub.

The commands use ``gh`` authentication with repository and Projects access:

.. code-block:: bash

   gh auth refresh -h github.com -s project

``github-project.json`` identifies the organization, project, and allowed
repositories. CI validates the export and uploads JSON as a build artifact.
Generated JSON stays in ``_build`` and is not committed. Synchronization is run
locally on demand, with no hosted agent or personal token stored in CI.
Run one synchronization at a time across all machines. The command detects
existing duplicate IDs, but issue creation is not a cross-machine lock.

Stable IDs embedded in issues prevent duplicates. The synchronizer owns the
marked specification section and title. It preserves text outside that section,
comments, assignees, and ongoing execution states. It creates native sub-issue
links and blocking dependencies.

Changed specifications receive ``spec-changed``. Open affected tasks become
Blocked until a maintainer checks the change, clears the label, and deliberately
restores readiness. Closed issues are not silently reopened. Removed requirements
are reported for explicit review, and issues or dependencies are not silently
deleted. Renaming a stable ID is a migration, not a normal edit.

Project states
--------------

- **Backlog:** scope or implementation work has not been scheduled.
- **Ready:** scoped task whose dependencies and specification have been checked.
- **In progress:** claimed by a contributor or agent.
- **In review:** a pull request and validation evidence are available.
- **Blocked:** a dependency, changed specification, or decision prevents progress.
- **Done:** accepted work is complete.

Closing a task as completed makes it Done on the next synchronization. Closing
as not planned does not satisfy dependent tasks. A requirement becomes verified
only through a documentation change with acceptance evidence.

Launching a local agent
-----------------------

From the docs repository:

.. code-block:: bash

   uv run --locked python scripts/work_issue.py https://github.com/PapyrusReader/docs/issues/NUMBER --launch

Use ``--check`` to validate eligibility without claiming the task.
Omit ``--launch`` to prepare the checkout and prompt for another local agent.
Use ``--directory`` to change the default checkout parent
``~/Projects/papyrus-tasks``.

The launcher checks the task's project status, readiness, source-change marker,
assignment, and dependency completion. It also checks that the pinned specification
files match the docs repository's ``development`` branch. Merge the specification
PR before launching its tasks. It creates the remote
``agent/issue-NUMBER`` branch as an atomic claim, assigns the issue to the current
GitHub user, and moves the task to In progress. It then clones an isolated checkout
from ``development`` and saves the prompt in that checkout's Git directory.

The optional launch opens an interactive Codex session with workspace-write
sandboxing and the user's configured model and authentication. It does not start
an unattended execution service. See `Codex CLI documentation
<https://learn.chatgpt.com/docs/cli>`_.

If preparation fails after claiming, the branch and assignment are retained so
another machine cannot silently start duplicate work. Inspect the branch and
checkout before releasing the claim. To retry from scratch, remove only an unused
claim branch, unassign the issue, and return it to Ready. Preserve any actual work.

Agents must read the owning repository's instructions and the linked contracts,
use pinned tools, and run the specified checks. Database tests require a distinct
test database and must not overlap. The launcher does not run those tests itself.
Agents open PRs targeting ``development`` and report test results and remaining
limitations. They do not merge, deploy, or mark requirements verified.

Pull requests and completion
----------------------------

Link the owning issue and covered requirement IDs in each PR. Use fully qualified
issue references when crossing repositories. GitHub closing keywords only take
effect when the PR reaches the repository's default branch, which is
``development`` for Papyrus components.

Preserve the existing release process: promote ``development`` to ``master`` with
a release PR and merge commit. Ordinary work does not bump versions or change
workspace submodule pointers solely to record a component PR.

After merging, record the acceptance evidence, close the implementation issue as
completed, and synchronize the project. Review the parent requirement's remaining
criteria before changing its status.
