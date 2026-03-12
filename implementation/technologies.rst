Technologies
============

Front-end
---------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Technology
     - Used for
   * - Flutter (Dart)
     - Cross-platform client applications (Android, iOS, Web, Desktop, e-ink UI).
   * - PowerSync
     - Offline-first data synchronization between local client storage and backend data sources.

Back-end
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Technology
     - Used for
   * - FastAPI (Python)
     - Backend API for authentication, library management, sync, and configuration endpoints.
   * - Supabase
     - Managed backend capabilities, especially authentication and hosted Postgres integrations.
   * - Redis
     - Caching, transient state, and coordination workloads (for example sessions and rate limiting).
   * - Docker
     - Containerized local development and deployment packaging.

Storage
-------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Technology
     - Used for
   * - PostgreSQL
     - Primary relational storage for metadata (users, books, organization, progress, annotations).

Metadata
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Technology
     - Used for
   * - Google Books API
     - Optional external metadata lookup for books.
   * - Open Library API
     - Optional external metadata lookup for books.

Analytics
---------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Technology
     - Used for
   * - Sentry
     - Optional error monitoring and diagnostics.
   * - Plausible
     - Optional privacy-focused analytics.
