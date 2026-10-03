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
