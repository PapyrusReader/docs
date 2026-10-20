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

Planned contracts
-----------------

Email verification before sign-in, recoverable account deletion followed by
permanent cleanup, and full-library content search are requirements with remaining
implementation work. They are not capabilities established by the architecture
diagram above. Additional storage providers remain committed targets, but
automatic failover is outside scope.
