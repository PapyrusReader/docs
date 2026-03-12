Server architecture
===================

This document describes the back-end architecture,
including the self-hostable server, file storage backends, and
synchronization mechanisms that enable cross-device functionality.

Architecture overview
---------------------

.. mermaid::

   flowchart TB
       subgraph Clients["Clients"]
           Android["Android"]
           iOS["iOS"]
           Web["Web"]
           Desktop["Desktop"]
       end

       subgraph Server["Server"]
           subgraph Metadata["Metadata storage"]
               M1["User accounts"]
               M2["Book metadata"]
               M3["Reading progress"]
               M4["Annotations & bookmarks"]
               M5["Shelves, tags, series"]
               M6["Reading goals"]
               M7["Sync coordination"]
           end

           subgraph FileStorage["File storage (optional)"]
               F1["Book files"]
               F2["Cover images"]
           end
       end

       subgraph AltStorage["Alternative file storage"]
           direction LR
           G["Google Drive"]
           O["OneDrive"]
           D["Dropbox"]
           W["WebDAV"]
           S3["S3"]
           L["Local device only"]
           G --- O
           O --- D
           D --- W
           W --- S3
           S3 --- L
       end

       Android --> Server
       iOS --> Server
       Web --> Server
       Desktop --> Server
       Server -.->|"OR (user's choice)"| AltStorage
       linkStyle 0,1,2,3,4 stroke:transparent,stroke-width:0px;

API endpoints
~~~~~~~~~~~~~

The Papyrus Server exposes a RESTful API:

.. list-table::
   :header-rows: 1

   * - Category
     - Endpoints
     - Description
   * - **Auth**
     - ``/api/v1/auth/*``
     - Register, login, OAuth, refresh tokens
   * - **Users**
     - ``/api/v1/users/*``
     - Profile, preferences, account deletion
   * - **Books**
     - ``/api/v1/books/*``
     - CRUD operations, metadata, cover images
   * - **Shelves**
     - ``/api/v1/shelves/*``
     - Create, update, organize books
   * - **Tags**
     - ``/api/v1/tags/*``
     - Tag management
   * - **Series**
     - ``/api/v1/series/*``
     - Series management and ordering
   * - **Annotations**
     - ``/api/v1/annotations/*``
     - Highlights, notes, bookmarks
   * - **Progress**
     - ``/api/v1/progress/*``
     - Reading position, sessions, statistics
   * - **Goals**
     - ``/api/v1/goals/*``
     - Goal creation and tracking
   * - **Sync**
     - ``/api/v1/sync/*``
     - Change synchronization
   * - **Storage**
     - ``/api/v1/storage/*``
     - Backend configuration
   * - **Files**
     - ``/api/v1/files/*``
     - File upload/download (when server is file backend)

Full server's API specification in described in the :doc:`API </api/index>` section.