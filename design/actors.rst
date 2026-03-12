Actors
======

This section defines the user types that interact with Papyrus. Each
actor represents a distinct user group with specific needs, goals, and
interaction patterns.

Actor summary
~~~~~~~~~~~~~

.. list-table::
  :header-rows: 1
  :widths: 15 10 40

  * - Actor
    - Type
    - Description
  * - Reader
    - Primary
    - Core user who reads and manages books
  * - Anonymous user
    - Primary
    - Uses app without account (offline mode)
  * - Registered user
    - Primary
    - Has account for sync and cloud features
  * - System administrator
    - Secondary
    - Manages self-hosted server instances
  * - Developer
    - Secondary
    - Integrates via API or builds extensions

Reader
~~~~~~

The core usee who uses the application for reading and managing their book collection.

**Profile**

Regularly consumes digital and/or physical books, often using multiple devices such as phones, tablets, computers, or e-readers. They value a seamless reading experience across platforms, and their technical expertise ranges from beginner to advanced.

**Goals**

- Read books comfortably on any device
- Organize and manage book collections efficiently
- Track reading progress and build reading habits
- Take notes and highlights while reading
- Achieve personal reading goals

**Use cases**

- :need:`UC-2_1`
- :need:`UC-2_4`
- :need:`UC-2_5`
- :need:`UC-2_6`
- :need:`UC-3_1`
- :need:`UC-3_2`
- :need:`UC-4_1`
- :need:`UC-5_1`
- :need:`UC-6_1`

--------------

Anonymous user
~~~~~~~~~~~~~~

A user who accesses the system without creating an account, using the application entirely offline.

**Profile**

Privacy-conscious individuals who avoid cloud services, users evaluating the application before committing, people in areas with limited or unreliable internet, and those who prefer complete data control.

**Goals**

- Use all reading features without registration
- Maintain complete privacy and local data control
- Access the application without internet dependency
- Optionally convert to registered user later without data loss

**Constraints**

- No cross-device synchronization
- No cloud storage options
- All data stored locally on device
- Must manually transfer data between devices

**Use cases**

- :need:`UC-1_4`
- :need:`UC-2_1`
- :need:`UC-3_1`
- :need:`UC-2_7`

--------------

Registered user
~~~~~~~~~~~~~~~

A user with an account who can access synchronization and cloud features.

**Profile**

Users who need cross-device synchronization and cloud backup for their reading data. They often use multiple devices and value the ability to recover their library and progress if a device is lost. They may utilize the official cloud service or opt for self-hosted server deployments, depending on their privacy preferences and technological literacy.

**Goals**

- Synchronize library and progress across all devices there the app is installed
- Back up reading data securely
- Access books from anywhere
- Recover data if device is lost

**Use cases**

- :need:`UC-1_1`
- :need:`UC-1_2`
- :need:`UC-1_3`
- :need:`UC-1_5`
- :need:`UC-7_1`
- :need:`UC-7_3`

--------------

System administrator
~~~~~~~~~~~~~~~~~~~~

A technical user responsible for deploying and maintaining self-hosted
Papyrus server instances.

**Profile:**

Technically proficient users with expertise in server administration. They manage deployments for personal use or within organizations, taking responsibility for security, maintenance, and overall system health. Their skill set typically includes familiarity with Docker, databases, and networking.

**Goals**

- Deploy Papyrus server with minimal friction
- Ensure system security and data protection
- Monitor performance and resource usage
- Manage user accounts (for organization deployments)
- Perform backups and disaster recovery

--------------

Developer
~~~~~~~~~

A technical user who interacts with the system via API or develops app extensions.

**Profile**

Users who are capable of building integrations, plugins and extensions to enhance the application's functionality, third-party service providers connecting external systems, and researchers or data analysts who access and analyze reading data programmatically.

**Goals**

- Integrate Papyrus with other systems
- Build custom clients or frontends
- Develop plugins for extended functionality
- Export/analyze reading data programmatically

--------------

Actor relationships
-------------------

.. mermaid::

   flowchart TB
       subgraph PapyrusSystem["Papyrus System"]
           subgraph PrimaryActors["Actors"]
               Anonymous["Anonymous User"]
               Reader["Reader<br/>"]
               Registered["Registered user"]
               Anonymous --> Reader
               Registered --> Reader
               Admin["System Administrator"]
               Developer["Developer"]
               Admin <--> Developer
               Anonymous -.->|"May upgrade to"| Registered
           end
       end