API
===

This section contains the complete REST API documentation for the Papyrus Server.

Overview
--------

The Papyrus Server provides a RESTful API for:

- **Authentication** -- User registration, login, OAuth, and session management
- **Books** -- CRUD operations for book metadata and file references
- **Organization** -- Shelves, tags, and series management
- **Annotations** -- Highlights, notes, and bookmarks
- **Progress** -- Reading sessions and statistics
- **Goals** -- Reading goal tracking
- **Sync** -- Cross-device synchronization
- **Storage** -- File storage backend configuration
- **Files** -- File upload/download (when server is file backend)

Authentication
--------------

Most endpoints require authentication via JWT Bearer token:

.. code-block:: text

   Authorization: Bearer <access_token>

Obtain tokens through the ``/auth/login`` or ``/auth/oauth/google`` endpoints. Access tokens expire after 1 hour. Use the refresh token to obtain new access tokens via ``/auth/refresh``.

Base URL
--------

.. list-table::
   :header-rows: 1

   * - Environment
     - URL
   * - Production
     - ``https://api.papyrus.app/v1``
   * - Staging
     - ``https://staging-api.papyrus.app/v1``
   * - Local
     - ``http://localhost:8080/v1``

Download specification
----------------------

- `OpenAPI Specification (YAML) <_static/openapi.yaml>`_ -- Full API specification file

Related documentation
---------------------

- :doc:`/design/server-architecture` -- System design and architecture
- :doc:`/design/database-model` -- Data schema and relationships
- :doc:`/design/entities` -- Entity definitions and attributes
