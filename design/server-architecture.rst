Server architecture
===================

The current implementation uses FastAPI, PostgreSQL and self-hosted PowerSync.
The Flutter client keeps a local SQLite library and profile-scoped media cache;
the reader package owns transient EPUB/PDF sessions and the host persists positions.

.. mermaid::

   flowchart LR
       Client["Flutter client / SQLite"] -->|"Auth, uploads, media, OPDS"| API["FastAPI"]
       API --> DB["PostgreSQL"]
       DB --> Sync["PowerSync service"]
       Sync -->|"Library replication"| Client
       API --> Media["Server media storage"]
       API --> Catalogs["OPDS catalogs / acquisition integrations"]

The API prefix is configurable. The server's example configuration uses ``/v1``,
not ``/api/v1``. Authentication, library entities, reading profiles, saved filters,
media and acquisition routes are documented in the generated :doc:`/api/index`.
Development sandbox routes are available only in debug configurations.

Account ownership is validated by services. Offline uploads are serialized per
owner and committed atomically; tombstones prevent delayed writes from restoring
deleted data. Physical media cleanup runs after commit. These contracts belong to
the server services and their regression tests, not a copied endpoint table.

Local media and Papyrus-managed server storage are implemented. Other cloud
provider adapters are product goals and should not be inferred from stored
storage-profile configuration. The requirement and entity diagrams elsewhere in
this documentation describe target behavior; consult the server models and Alembic
revisions for the deployed schema.

Synchronization policy
----------------------

The target conflict policy is specified in :need:`NFR-2_3`. The Papyrus API
decides which writes to accept. PowerSync carries queued uploads and replicates
the committed result. Client timestamps are not a global ordering mechanism.

The current library mutation handler discards client-supplied ``updated_at``,
applies supplied fields, and assigns a server update time. Tombstones protect
deleted entities. JSON payloads are not recursively merged. Owner serialization,
atomic batches, and history validation remain part of the server contract.
Reading history is an immutable ledger: corrections append reversals, and progress
is projected from eligible time intervals and document coverage. Tracking writes
are staged locally until the server advertises the current schema contract.

Timers use versioned transitions under the same owner lock. The first accepted
branch wins; stale branches are acknowledged without applying their effects. Saving
a timer, appending its activities and updating book progress form one transaction.
Conflicting saves discard the whole batch. Terminal rows prevent delayed offline
writes from reviving completed timers. Native notification actions are journaled
on the device and replayed through the client repository; they do not write to
PowerSync independently.

These mechanisms need acceptance coverage across the full set of mutable fields
before the whole requirement can be marked verified.

See `PowerSync conflict handling
<https://docs.powersync.com/handling-writes/handling-update-conflicts>`_.

Guest and account boundaries
----------------------------

Guest libraries remain separate from account libraries. Registration and sign-in
switch the active library without transferring guest data. Server profiles and
users also have separate database and media scopes. Becoming connected does not
turn a guest library into a synchronized account library.

Profile photos
--------------

``POST /v1/users/me/avatar`` accepts a multipart JPEG/PNG ``file`` and
``display_name``. The server bounds each photo to 5 MiB, checks its image
signature, serializes writes on the owner row, and commits the photo reference
and name together. Photos use a separate fixed allowance from library storage.
The client resizes photos to at most 512 pixels on the longest side and removes
source metadata before uploading.

The existing ``avatar_url`` field stores an API-prefix-relative reference such
as ``/users/me/avatar/{uuid}``. Fetching it requires the owner's access token
against the configured server. External provider photo URLs remain supported,
but are fetched without Papyrus credentials. Downloads are private and marked
``no-store``. Replacing a photo removes the previous file after commit, and
permanent account deletion removes the entire owner media directory, including
photos. Failed writes retain the previous reference and file.

Account deletion and recovery
-----------------------------

In-app deletion uses the current authenticated session. Public deletion requests
and sign-in to an account awaiting deletion use a short-lived, single-use
credential. Scheduling revokes existing sessions. Explicit recovery cancels the
request and issues fresh tokens in one transaction, without another sign-in.
Email notices are queued in the account transaction and delivered asynchronously
with retries. Notices are retained and delivered in event order for each account,
then removed after delivery, seven days, or permanent account deletion.
See :need:`FR-1_6` for the policy and :doc:`/manual/index` for the user flow.

After the 30-day recovery window, a worker deletes account-owned records and
queues physical media cleanup in the same database transaction. Cleanup runs at
startup and every 60 seconds. Durable jobs survive restarts and retry storage
failures, with row locks coordinating multiple workers. Local device libraries
and external provider files remain outside this cleanup. Previously issued
PowerSync tokens remain usable until expiry and cannot be renewed.

Verification before sign-in
----------------------------

Registration creates a pending account and queues verification mail without
issuing an application session. Login, refresh and authenticated API access require
verification of the account's current primary email. Verification consumes a
single-use email-bound token; the client then signs in separately. Google sign-in
uses provider authority for eligible Gmail/Workspace identities and Papyrus email
verification for other addresses. Guest data stays separate throughout these flows.

The generated :doc:`/api/index` defines the wire schemas. Auth services and their
regression tests own eligibility, token consumption and delivery behavior.

Planned capabilities
--------------------

Full-library content search and additional storage providers remain product
targets. Their presence in requirements or diagrams does not establish implemented
behavior. Automatic storage failover is outside scope.
