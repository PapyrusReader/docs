Requirements overview
=====================

This section provides an overview of the requirements specification for Papyrus, including the structure, notation, and traceability between requirements, use cases, and entities.

Requirement notation
--------------------

Identifiers
~~~~~~~~~~~

- **FR-X_Y** - functional requirement (e.g., *FR-2_1: format conversion*)
- **NFR-X_Y** - non-functional requirement (e.g., *NFR-4_1: startup time*)
- **UC-X_Y** - use case (e.g., *UC-2_1: import books*).

Priority levels
~~~~~~~~~~~~~~~

- **P0** - critical (v0.x).
- **P1** - high (v1.0).
- **P2** - medium (v1.x).
- **P3** - low (v2.x+).

----

All requirements
----------------

.. needtable::
   :columns: id;title;status;priority
   :style: table
   :sort: id

Functional requirements by category
------------------------------------

.. list-table::
   :header-rows: 1

   * - Category
     - Scope
     - Description
   * - User management
     - FR-1.x
     - Account, auth, offline mode
   * - Book management
     - FR-2.x
     - Import, organize, search
   * - Integrated viewer
     - FR-3.x
     - Reading, customization, profiles
   * - Annotations and notes
     - FR-4.x
     - Highlights, notes, export
   * - Progress tracking
     - FR-5.x
     - Statistics, sync
   * - Goal management
     - FR-6.x
     - Goals, progress, notifications
   * - Storage and sync
     - FR-7.x
     - Metadata server, file storage backends, OPDS

Non-functional requirements by category
----------------------------------------

.. list-table::
   :header-rows: 1

   * - Category
     - Scope
     - Description
   * - Storage
     - NFR-1.x
     - File size, backends, encryption
   * - Synchronization
     - NFR-2.x
     - Offline, conflicts, performance
   * - Platform Support
     - NFR-3.x
     - Web, desktop, mobile, e-ink
   * - Performance
     - NFR-4.x
     - Startup, open, search, scale
   * - Usability
     - NFR-5.x
     - Design, accessibility, i18n
   * - Security
     - NFR-6.x
     - Auth, encryption, privacy
   * - Reliability
     - NFR-7.x
     - Uptime, integrity, backup
   * - Extensibility
     - NFR-8.x
     - Plugin architecture
   * - Maintainability
     - NFR-9.x
     - Code quality, logging

----

Dependency graphs
-----------------

User management
~~~~~~~~~~~~~~~

.. needflow::
   :filter: id.startswith('FR-1_') or id.startswith('UC-1_')
   :config: lefttoright,furo

Book management
~~~~~~~~~~~~~~~

.. needflow::
   :filter: id.startswith('FR-2_') or id.startswith('UC-2_')
   :config: lefttoright,furo

Integrated viewer
~~~~~~~~~~~~~~~~~

.. needflow::
   :filter: id.startswith('FR-3_') or id.startswith('UC-3_')
   :config: lefttoright,furo

Annotations & notes
~~~~~~~~~~~~~~~~~~~

.. needflow::
   :filter: id.startswith('FR-4_') or id.startswith('UC-4_')
   :config: lefttoright,furo

Progress & goals
~~~~~~~~~~~~~~~~

.. needflow::
   :filter: id.startswith('FR-5_') or id.startswith('FR-6_') or id.startswith('UC-5_') or id.startswith('UC-6_')
   :config: lefttoright,furo

Storage & sync
~~~~~~~~~~~~~~

.. needflow::
   :filter: id.startswith('FR-7_') or id.startswith('UC-7_')
   :config: lefttoright,furo

----

Core principles
---------------

**User data ownership**

All user data, such as books, notes, annotations, can be exported in open formats, avoiding vendor lock-in and enabling self-hosting options for those who prefer full control over their data.

**Cross-platform accessibility**

Consistent experience and a full set of features across all devices and platforms, with additional platform-specific features, such as themes suitable for e-ink screens.

**Offline functionality**

No account or internet connection is required to use application's core. Non-essential features, such as data synchronization and cloud file storage is optional.

**Privacy first**

Local-first architecture with no analytics or tracking enabled by default. A user can avoid relying on cloud services and use the system offline or with a self-hosted server instance.

**Developer friendly**

The system is fully open source and makes it easy to self-host the server for file storage and data sync. Documented REST API allows users to easily build their own clients and book management solutions.

----

Related documents
-----------------

- :doc:`functional`
- :doc:`non-functional`
- :doc:`/design/use-cases`
- :doc:`/design/entities`
- :doc:`/design/database-model`
- :doc:`/design/server-architecture`
