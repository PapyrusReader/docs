Entities
========

This section describes the core objects and how they connect
to each other. Together, these entities define the structure of the
library, reading experience, progress tracking, and synchronization
features used across the product. Each entity focuses on meaning and behavior: what the object represents,
which information it carries, and how it relates to other objects in
the system.

Entity overview
---------------

.. list-table::
   :header-rows: 1
   :widths: 20 45

   * - Entity
     - Purpose
   * - User
     - Represents a person using Papyrus (anonymous or registered)
   * - Book
     - Represents a physical or digital book in a user library
   * - Shelf
     - User-defined collection used to organize books
   * - Tag
     - User-defined label used to categorize books
   * - Series
     - Optional grouping of books that belong to a sequence
   * - Annotation
     - Highlighted text segment with optional user note
   * - Note
     - Free-form note attached to a book
   * - Bookmark
     - Saved location in a book
   * - Reading session
     - Recorded reading activity over time
   * - Reading goal
     - User-defined reading objective and progress
   * - Reading profile
     - Named set of reader/viewer display settings
   * - Metadata server config
     - Metadata sync connection and sync behavior settings
   * - File storage backend
     - Configured file storage target for digital book files
   * - Saved filter
     - Reusable search/filter definition

Domain relationship map
-----------------------

.. mermaid::

   classDiagram
       User "1" --> "0..*" Book : owns
       User "1" --> "0..*" Shelf : manages
       User "1" --> "0..*" Tag : manages
       User "1" --> "0..*" Series : manages
       User "1" --> "0..*" Annotation : creates
       User "1" --> "0..*" Note : writes
       User "1" --> "0..*" Bookmark : creates
       User "1" --> "0..*" ReadingSession : records
       User "1" --> "0..*" ReadingGoal : sets
       User "1" --> "0..*" ReadingProfile : saves
       User "1" --> "0..1" MetadataServerConfig : configures
       User "1" --> "0..*" FileStorageBackend : configures
       User "1" --> "0..*" SavedFilter : saves

       Book "0..*" --> "0..*" Shelf : organized_in
       Book "0..*" --> "0..*" Tag : tagged_with
       Book "0..*" --> "0..1" Series : belongs_to
       Book "1" --> "0..*" Annotation : has
       Book "1" --> "0..*" Note : has
       Book "1" --> "0..*" Bookmark : has
       Book "1" --> "0..*" ReadingSession : has
       Book "0..*" --> "0..1" FileStorageBackend : stored_in

       Shelf "0..1" --> "0..*" Shelf : parent_child

Entity definitions
------------------

User
~~~~

Represents a person using Papyrus, either anonymously (local-only) or with a registered account.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Display name
     - String
     - Required
     - Name shown in the interface.
   * - Email
     - String
     - Optional, unique when present
     - Login and communication address for registered users.
   * - Password hash
     - String
     - Optional
     - Password credential for email/password login.
   * - External login ID
     - String
     - Optional, unique when present
     - Provider-specific login identifier (for example Google OAuth).
   * - Anonymous flag
     - Boolean
     - Required
     - Distinguishes anonymous and registered usage modes.
   * - Active flag
     - Boolean
     - Required
     - Indicates whether account access is enabled.
   * - Email verified flag
     - Boolean
     - Required for email-based login
     - Indicates whether email ownership was verified.
   * - Preferences
     - Object
     - Optional
     - User-level app preferences.
   * - Last login at
     - Datetime
     - Optional
     - Last successful authentication time.

Book
~~~~

Represents one item in the library, digital or physical.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns the book in their library.
   * - Title
     - String
     - Required
     - Main display title.
   * - Subtitle
     - String
     - Optional
     - Secondary title.
   * - Authors
     - List of strings
     - At least one value
     - Book authors.
   * - Publisher
     - String
     - Optional
     - Publisher name.
   * - Publication date
     - Date
     - Optional
     - Publication date.
   * - Language
     - String
     - Optional
     - Language code or language name.
   * - ISBN-10
     - String
     - Optional
     - Ten-digit ISBN.
   * - ISBN-13
     - String
     - Optional
     - Thirteen-digit ISBN.
   * - Description
     - Text
     - Optional
     - Summary or notes about the book.
   * - Cover image
     - URI/path
     - Optional
     - Link or local path to cover image.
   * - Book type
     - Enum
     - Required: ``digital`` or ``physical``
     - Distinguishes storage and reader behavior.
   * - Digital file path
     - String
     - Optional, required for digital imports
     - Location of the digital file.
   * - File format
     - String
     - Optional
     - Format such as EPUB, PDF, MOBI.
   * - File size
     - Integer
     - Optional, non-negative
     - Size in bytes.
   * - File hash
     - String
     - Optional
     - Checksum for duplicate detection and integrity.
   * - Physical location
     - String
     - Optional
     - User-defined location of physical copy.
   * - Lent to
     - String
     - Optional
     - Borrower information for physical books.
   * - Lent at
     - Datetime
     - Optional
     - Lending timestamp.
   * - Reading status
     - Enum
     - Required: ``not_started``, ``in_progress``, ``completed``, ``paused``, ``abandoned``
     - Current reading state.
   * - Current page
     - Integer
     - Optional, non-negative
     - Latest known page for page-based formats.
   * - Current position
     - Decimal
     - Optional, range 0.0 to 1.0
     - Progress for position-based formats.
   * - Current CFI/locator
     - String
     - Optional
     - Format-specific digital locator.
   * - Favorite flag
     - Boolean
     - Required
     - Marks user-favorite books.
   * - Rating
     - Integer
     - Optional, range 1 to 5
     - User-assigned rating.
   * - Started at
     - Datetime
     - Optional
     - First reading timestamp.
   * - Completed at
     - Datetime
     - Optional
     - Completion timestamp.
   * - Added at
     - Datetime
     - Required
     - Time added to library.
   * - Last read at
     - Datetime
     - Optional
     - Most recent reading activity time.
   * - Series reference
     - Series reference
     - Optional
     - Series the book belongs to.
   * - Series number
     - Number
     - Optional
     - Position within series.
   * - Storage backend reference
     - Storage backend reference
     - Optional
     - Backend where the digital file is stored.
   * - Custom metadata
     - Object
     - Optional
     - User-defined metadata fields.
   * - OCR processed flag
     - Boolean
     - Required
     - Indicates OCR processing status.
   * - OCR confidence
     - Decimal
     - Optional, range 0.0 to 1.0
     - OCR quality estimate.

Shelf
~~~~~

Represents a user-defined collection of books.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns the shelf.
   * - Parent shelf
     - Shelf reference
     - Optional
     - Parent shelf for nested structures.
   * - Name
     - String
     - Required
     - Shelf name visible in navigation.
   * - Description
     - Text
     - Optional
     - Optional explanatory text.
   * - Color
     - String
     - Optional
     - Visual color marker.
   * - Icon
     - String
     - Optional
     - Visual icon marker.
   * - Default flag
     - Boolean
     - Required
     - Indicates built-in/default shelf.
   * - Smart shelf flag
     - Boolean
     - Required
     - Indicates whether membership is query-driven.
   * - Smart query
     - String
     - Optional, required when smart shelf flag is true
     - Filter expression for dynamic membership.
   * - Sort order
     - Integer
     - Optional, non-negative
     - Display ordering hint.

Tag
~~~

Represents a reusable label used for categorization.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns the tag namespace.
   * - Name
     - String
     - Required, unique within a user
     - Label name.
   * - Color
     - String
     - Required
     - Display color.
   * - Description
     - Text
     - Optional
     - Optional explanatory text.
   * - Usage count
     - Integer
     - Optional, non-negative
     - Number of books currently using the tag.

Series
~~~~~~

Represents an ordered sequence or grouping of related books.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns the series definition.
   * - Name
     - String
     - Required
     - Series name.
   * - Description
     - Text
     - Optional
     - Optional description.
   * - Author
     - String
     - Optional
     - Optional primary author for grouping context.
   * - Total books
     - Integer
     - Optional, non-negative
     - Expected number of books in the series.
   * - Complete flag
     - Boolean
     - Required
     - Indicates whether the series is complete from the user perspective.

Annotation
~~~~~~~~~~

Represents a highlighted text fragment with optional note content.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Book
     - Book reference
     - Required
     - Book containing the annotation.
   * - Creator
     - User reference
     - Required
     - User who created the annotation.
   * - Selected text
     - Text
     - Required
     - Highlighted text content.
   * - Note
     - Text
     - Optional
     - Optional comment tied to highlight.
   * - Highlight color
     - String
     - Required
     - Chosen highlight color.
   * - Start position
     - String
     - Required
     - Start locator in book content.
   * - End position
     - String
     - Required
     - End locator in book content.
   * - Chapter title
     - String
     - Optional
     - Chapter context.
   * - Chapter index
     - Integer
     - Optional, non-negative
     - Chapter number/index.
   * - Page number
     - Integer
     - Optional, non-negative
     - Page context when available.

Note
~~~~

Represents free-form user notes attached to a book.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Book
     - Book reference
     - Required
     - Book the note belongs to.
   * - Creator
     - User reference
     - Required
     - User who wrote the note.
   * - Title
     - String
     - Required
     - Note title.
   * - Content
     - Text
     - Required
     - Note content (plain text or markdown).
   * - Pinned flag
     - Boolean
     - Required
     - Indicates quick-access pinning.

Bookmark
~~~~~~~~

Represents a saved navigation point in a book.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Book
     - Book reference
     - Required
     - Book the bookmark belongs to.
   * - Creator
     - User reference
     - Required
     - User who created the bookmark.
   * - Position
     - String
     - Required
     - Locator (page, offset, CFI, or equivalent).
   * - Page number
     - Integer
     - Optional, non-negative
     - Page context when available.
   * - Chapter title
     - String
     - Optional
     - Chapter context.
   * - Note
     - String
     - Optional
     - Short optional memo.
   * - Color
     - String
     - Optional
     - Display color.

Reading session
~~~~~~~~~~~~~~~

Represents one tracked period of reading activity.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - User
     - User reference
     - Required
     - Reader who performed the session.
   * - Book
     - Book reference
     - Required
     - Book read in the session.
   * - Start time
     - Datetime
     - Required
     - Session start timestamp.
   * - End time
     - Datetime
     - Optional
     - Session end timestamp.
   * - Start position
     - Number
     - Optional
     - Reading position at session start.
   * - End position
     - Number
     - Optional
     - Reading position at session end.
   * - Pages read
     - Integer
     - Optional, non-negative
     - Number of pages progressed.
   * - Duration minutes
     - Integer
     - Optional, non-negative
     - Session duration in minutes.
   * - Device type
     - String
     - Optional
     - Device category (phone, tablet, desktop, e-ink).
   * - Device name
     - String
     - Optional
     - User-visible device identifier.

Reading goal
~~~~~~~~~~~~

Represents a measurable reading objective with progress.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns the goal.
   * - Title
     - String
     - Required
     - Goal title.
   * - Description
     - Text
     - Optional
     - Optional explanatory details.
   * - Goal type
     - Enum
     - Required: ``books_count``, ``pages_count``, ``reading_time``
     - Metric used to evaluate progress.
   * - Target value
     - Integer
     - Required, positive
     - Goal target amount.
   * - Current value
     - Integer
     - Required, non-negative
     - Current progress amount.
   * - Time period
     - Enum
     - Required: ``daily``, ``weekly``, ``monthly``, ``yearly``, ``custom``
     - Goal recurrence or window type.
   * - Start date
     - Date
     - Required
     - Goal start.
   * - End date
     - Date
     - Required, must be on or after start date
     - Goal end.
   * - Active flag
     - Boolean
     - Required
     - Indicates whether goal participates in tracking.
   * - Completed flag
     - Boolean
     - Required
     - Indicates whether goal is completed.
   * - Completed at
     - Datetime
     - Optional
     - Completion timestamp.

Reading profile
~~~~~~~~~~~~~~~

Represents a saved set of reader appearance and behavior settings.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns the profile.
   * - Name
     - String
     - Required
     - Profile name.
   * - Default flag
     - Boolean
     - Required
     - Indicates default profile.
   * - Font family
     - String
     - Optional
     - Reader font family.
   * - Font size
     - Integer
     - Optional, typically 8 to 72
     - Reader font size.
   * - Font weight
     - Integer
     - Optional
     - Reader font weight.
   * - Line height
     - Decimal
     - Optional, positive
     - Line spacing.
   * - Letter spacing
     - Decimal
     - Optional
     - Character spacing.
   * - Paragraph spacing
     - Decimal
     - Optional
     - Paragraph spacing.
   * - Text alignment
     - Enum
     - Optional: ``left``, ``right``, ``center``, ``justify``
     - Alignment mode.
   * - Horizontal margin
     - Integer
     - Optional, non-negative
     - Horizontal margin.
   * - Vertical margin
     - Integer
     - Optional, non-negative
     - Vertical margin.
   * - Background color
     - String
     - Optional
     - Background color value.
   * - Text color
     - String
     - Optional
     - Foreground text color.
   * - Link color
     - String
     - Optional
     - Link color.
   * - Selection color
     - String
     - Optional
     - Text selection color.
   * - Theme mode
     - Enum
     - Optional: ``light``, ``dark``, ``sepia``, ``custom``
     - Theme selection.
   * - Reading mode
     - Enum
     - Optional: ``paginated``, ``continuous``
     - Navigation/layout mode.
   * - Page turn animation
     - Boolean
     - Optional
     - Enables or disables page-turn animation.
   * - Column count
     - Integer
     - Optional, positive
     - Number of columns.
   * - Hyphenation
     - Boolean
     - Optional
     - Hyphenation behavior.

Metadata server configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents how a user connects to metadata synchronization services.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required, at most one per user
     - User whose sync config this is.
   * - Server URL
     - URI
     - Required
     - Endpoint used for metadata sync.
   * - Server type
     - Enum
     - Required: ``official``, ``self_hosted``
     - Service classification.
   * - Auth token
     - String
     - Optional, sensitive
     - Access credential.
   * - Refresh token
     - String
     - Optional, sensitive
     - Token refresh credential.
   * - Connected flag
     - Boolean
     - Required
     - Indicates whether connection is currently established.
   * - Sync enabled
     - Boolean
     - Required
     - Enables background synchronization.
   * - Sync interval seconds
     - Integer
     - Optional, positive
     - Background sync interval.
   * - Last sync at
     - Datetime
     - Optional
     - Last successful sync time.
   * - Sync status
     - Enum
     - Optional: ``idle``, ``syncing``, ``error``
     - Current sync state.
   * - Sync error message
     - String
     - Optional
     - Last error details when status is ``error``.

File storage backend
~~~~~~~~~~~~~~~~~~~~

Represents a configured destination for digital book files.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns backend configuration.
   * - Backend type
     - Enum
     - Required (for example local, Google Drive, WebDAV, S3-compatible)
     - Storage provider type.
   * - Name
     - String
     - Required
     - Display name.
   * - Primary flag
     - Boolean
     - Required; at most one primary backend per user
     - Preferred backend for uploads.
   * - Active flag
     - Boolean
     - Required
     - Whether backend is enabled.
   * - Connection config
     - Object
     - Required
     - Provider-specific connection settings.
   * - Credentials
     - Object
     - Optional, sensitive
     - Provider credentials or tokens.
   * - Base path
     - String
     - Optional
     - Root directory/container path.
   * - Used bytes
     - Integer
     - Optional, non-negative
     - Currently used storage.
   * - Quota bytes
     - Integer
     - Optional, non-negative
     - Available quota.
   * - Last accessed at
     - Datetime
     - Optional
     - Last successful backend interaction.
   * - Connection status
     - Enum
     - Optional: ``connected``, ``disconnected``, ``error``
     - Operational connection state.
   * - Error message
     - String
     - Optional
     - Last connection/storage error.

Saved filter
~~~~~~~~~~~~

Represents a reusable search/filter definition.

.. list-table:: Attributes
   :header-rows: 1
   :widths: 18 16 20 46

   * - Attribute
     - Type
     - Constraints
     - Description
   * - Owner
     - User reference
     - Required
     - User who owns the filter.
   * - Name
     - String
     - Required
     - Display name.
   * - Description
     - Text
     - Optional
     - Optional explanatory text.
   * - Query
     - String
     - Required
     - Filter expression.
   * - Filter type
     - Enum
     - Optional: ``search``, ``shelf``, ``custom``
     - Classification used by UI and behavior.
   * - Icon
     - String
     - Optional
     - Optional UI icon.
   * - Color
     - String
     - Optional
     - Optional UI color.
   * - Pinned flag
     - Boolean
     - Required
     - Indicates sidebar/home pinning.
   * - Usage count
     - Integer
     - Optional, non-negative
     - Number of times filter was used.
   * - Last used at
     - Datetime
     - Optional
     - Most recent use timestamp.

Relationship rules
------------------

- A book may be on multiple shelves and a shelf may contain multiple books.
- A book may have multiple tags and a tag may be reused across many books.
- Shelf hierarchy is optional and supports nested organization.
- A user may use the app without sync (no metadata server configuration).
- A user may configure multiple storage backends, with one preferred backend for uploads.
- Physical and digital books share the same Book entity; format-specific attributes are optional depending on type.
