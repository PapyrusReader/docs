Functional requirements
=======================

1. User management
------------------

.. fr:: Account registration
   :id: FR-1_1
   :status: open
   :priority: P0
   :links: UC-1_1

   User can create an account using an email address and password.

   **Acceptance criteria:**

   - Email must be valid and unique in the system
   - Password must meet minimum security requirements (8+ characters, mixed case, number)
   - Email verification is sent upon registration
   - Account is created in inactive state until email is verified

.. fr:: Email/password login
   :id: FR-1_2
   :status: open
   :priority: P0
   :links: UC-1_2

   User can log in to the system using email and password.

   **Acceptance criteria:**

   - System validates credentials against stored hash
   - Failed attempts are rate-limited (max 5 per minute)
   - Successful login creates a secure session token
   - User is redirected to their library after login

.. fr:: OAuth login (Google)
   :id: FR-1_3
   :status: open
   :priority: P1
   :links: UC-1_3

   User can log in using their Google account via OAuth 2.0.

   **Acceptance criteria:**

   - Google OAuth flow completes securely
   - New users are automatically registered on first OAuth login
   - Existing users can link Google account to email account
   - Google profile photo and name are imported (optional)

.. fr:: Offline mode
   :id: FR-1_4
   :status: open
   :priority: P0
   :links: UC-1_4

   User can use the application in offline mode without credentials or internet connection.

   **Acceptance criteria:**

   - All reading and library management features work offline
   - Data is stored locally on device
   - No account required for offline-only usage
   - Offline users can later create account and migrate data

.. fr:: Password recovery
   :id: FR-1_5
   :status: open
   :priority: P1
   :links: UC-1_5

   User can reset their password via email recovery link.

   **Acceptance criteria:**

   - Recovery link is sent to registered email
   - Link expires after 24 hours
   - Link is single-use and invalidated after password change
   - User must set new password meeting security requirements

.. fr:: Account deletion
   :id: FR-1_6
   :status: open
   :priority: P1
   :links: UC-1_6

   User can permanently delete their account and all associated data.

   **Acceptance criteria:**

   - Deletion requires password confirmation
   - User is warned about data loss
   - All user data is removed from server within 30 days
   - Local device data remains unless explicitly deleted

----

2. Book management
------------------

.. fr:: Format conversion
   :id: FR-2_1
   :status: open
   :priority: P2
   :links: UC-2_2

   User can convert e-book files between supported formats (EPUB, PDF, MOBI).

   **Acceptance criteria:**

   - Conversion preserves content and basic formatting
   - Original file is retained after conversion
   - Progress indicator shown for large files
   - Conversion errors are reported clearly

.. fr:: Manual metadata editing
   :id: FR-2_2
   :status: open
   :priority: P0
   :links: UC-2_3

   User can manually edit book metadata (title, author, description, etc.).

   **Acceptance criteria:**

   - Editable fields: title, subtitle, author, co-authors, publisher, publication date, ISBN, language, description, series, series number
   - Changes are saved immediately
   - Cover image can be replaced from file or URL

.. fr:: Custom metadata fields
   :id: FR-2_3
   :status: open
   :priority: P2
   :links: UC-2_3

   User can add and remove custom metadata fields to books.

   **Acceptance criteria:**

   - Custom fields have user-defined names
   - Field values can be text, number, date, or boolean
   - Custom fields are searchable
   - Batch editing of custom fields is supported

.. fr:: Book file export
   :id: FR-2_4
   :status: open
   :priority: P0
   :links: UC-2_7

   User can export selected book files from the system.

   **Acceptance criteria:**

   - Single or multiple books can be selected
   - Export as individual files or ZIP archive
   - Original file format is preserved
   - Export includes embedded metadata

.. fr:: Library data export
   :id: FR-2_5
   :status: open
   :priority: P1
   :links: UC-2_7

   User can export library data in structured, human-readable formats.

   **Acceptance criteria:**

   - Export formats: JSON, CSV, OPML
   - Includes all metadata, shelves, tags, and reading progress
   - Annotations and notes can be included optionally
   - Export can be filtered by shelf or tags

.. fr:: Book import
   :id: FR-2_6
   :status: open
   :priority: P0
   :links: UC-2_1

   User can import books from files, URLs, or cloud storage.

   **Acceptance criteria:**

   - Supported import sources: local files, URLs, Google Drive, OneDrive, Dropbox
   - Bulk import of multiple files/folders
   - Metadata is automatically extracted from file
   - Duplicate detection with merge options

.. fr:: Full-text search
   :id: FR-2_7
   :status: open
   :priority: P1
   :links: UC-2_6

   System provides full-text search within book contents.

   **Acceptance criteria:**

   - Search works for EPUB, TXT formats (PDF requires OCR)
   - Results show matched text with context
   - Search is case-insensitive by default
   - Results link directly to location in book

.. fr:: Advanced search
   :id: FR-2_8
   :status: open
   :priority: P0
   :links: UC-2_6

   System supports searching by metadata, tags, categories, and content.

   **Acceptance criteria:**

   - Searchable fields: title, author, description, ISBN, tags, shelves
   - Filters: reading status, format, date added, publication date, rating
   - Search results are sortable
   - Recent searches are saved

.. fr:: Shelf organization
   :id: FR-2_9
   :status: open
   :priority: P0
   :links: UC-2_4

   User can create shelves to group books into collections.

   **Acceptance criteria:**

   - Shelves have name, description, and optional color
   - Books can belong to multiple shelves
   - Default shelves: "Currently Reading", "Want to Read", "Finished"
   - Shelves can be nested (sub-shelves)
   - Drag-and-drop organization

.. fr:: Book tagging
   :id: FR-2_10
   :status: open
   :priority: P0
   :links: UC-2_5

   User can assign colored tags to books for organization and filtering.

   **Acceptance criteria:**

   - Tags have title and color (from palette or custom)
   - Books can have 0-10 tags
   - Tags are visible in library view
   - Quick tag assignment via context menu
   - Batch tagging supported

.. fr:: Query language filters
   :id: FR-2_11
   :status: open
   :priority: P2
   :links: UC-2_6

   User can create complex filters using a query language.

   **Acceptance criteria:**

   - Query syntax similar to Jira/GitHub (e.g., ``author:"Name" AND year:>2000``)
   - Supports AND, OR, NOT operators
   - Date ranges, numeric comparisons
   - Filters can be saved and named
   - Graphical filter builder as alternative

.. fr:: ISBN barcode scanning
   :id: FR-2_12
   :status: open
   :priority: P2
   :links: UC-2_8

   User can scan ISBN barcodes to add physical books with fetched metadata.

   **Acceptance criteria:**

   - Camera-based barcode scanning (mobile/desktop with camera)
   - ISBN lookup from multiple sources
   - User can edit fetched metadata before saving
   - Works offline with manual ISBN entry fallback

.. fr:: Metadata fetching
   :id: FR-2_13
   :status: open
   :priority: P1
   :links: UC-2_3

   System can automatically fetch metadata from online sources.

   **Acceptance criteria:**

   - Sources: Open Library, Google Books (configurable)
   - Fetch triggered manually or on import
   - User reviews and confirms changes before applying
   - Cover images can be fetched automatically

.. fr:: Physical book tracking
   :id: FR-2_14
   :status: open
   :priority: P1
   :links: UC-2_9

   User can add and track physical books in their library.

   **Acceptance criteria:**

   - Manual entry of all metadata fields
   - Physical books appear in library alongside digital
   - Reading status and progress tracking
   - Location field (e.g., "Shelf 3", "Lent to John")

----

3. Integrated viewer
--------------------

.. fr:: E-book reading
   :id: FR-3_1
   :status: open
   :priority: P0
   :links: UC-3_1

   User can read e-books using the integrated viewer.

   **Acceptance criteria:**

   - Supports: EPUB, PDF, MOBI, AZW3, TXT, CBR, CBZ
   - Responsive layout adapts to screen size
   - Reading position is automatically saved
   - Table of contents navigation
   - Page/chapter navigation

.. fr:: Viewer customization
   :id: FR-3_2
   :status: open
   :priority: P0
   :links: UC-3_2

   User can customize the viewer appearance and behavior.

   **Acceptance criteria:**

   - Typography: font family, size (8-72pt), weight, line height, letter spacing, paragraph spacing
   - Colors: background, text, links (presets + custom)
   - Layout: margins, padding, single/dual page, pagination/scroll
   - Navigation: tap zones, swipe, volume keys, on-screen buttons
   - Brightness: in-app control independent of system

.. fr:: Reading profiles
   :id: FR-3_3
   :status: open
   :priority: P1
   :links: UC-3_3

   User can create and manage named reading profiles.

   **Acceptance criteria:**

   - Profile contains all viewer customization settings
   - Quick switch between profiles
   - One profile can be set as default
   - Profiles can be exported/imported
   - Device-specific default profiles

.. fr:: Bookmarks
   :id: FR-3_4
   :status: open
   :priority: P0
   :links: UC-3_4

   User can create and manage bookmarks within books.

   **Acceptance criteria:**

   - Create bookmark at current position with optional note
   - List all bookmarks for a book
   - Jump to bookmark location
   - Delete bookmarks
   - Bookmarks sync across devices

----

4. Annotations and notes
------------------------

.. fr:: Text highlighting
   :id: FR-4_1
   :status: open
   :priority: P0
   :links: UC-4_1

   User can highlight text while reading with optional notes.

   **Acceptance criteria:**

   - Select text and choose highlight color
   - Multiple color options (at least 5)
   - Optional note attached to highlight
   - Highlights visible in text
   - View all highlights in dedicated panel

.. fr:: Book notes
   :id: FR-4_2
   :status: open
   :priority: P0
   :links: UC-4_2

   User can create free-form notes associated with books.

   **Acceptance criteria:**

   - Notes have title and content
   - Rich text or Markdown support
   - Notes are not tied to specific text location
   - Multiple notes per book
   - Notes are searchable

.. fr:: Annotation editing
   :id: FR-4_3
   :status: open
   :priority: P0
   :links: UC-4_3

   User can edit and delete existing annotations and notes.

   **Acceptance criteria:**

   - Edit highlight color and attached note
   - Edit note title and content
   - Delete with confirmation
   - Undo delete within session

.. fr:: Annotation export
   :id: FR-4_4
   :status: open
   :priority: P1
   :links: UC-4_4

   User can export annotations and notes to external formats.

   **Acceptance criteria:**

   - Export formats: plain text, Markdown, PDF, HTML
   - Include highlighted text with context
   - Group by book or export all
   - Include metadata (book title, date, page)

.. fr:: Annotation search
   :id: FR-4_5
   :status: open
   :priority: P1
   :links: UC-4_5

   User can search through all annotations and notes.

   **Acceptance criteria:**

   - Search across all books or specific book
   - Search in highlight text and note content
   - Filter by color, date, book
   - Results link to source location

----

5. Progress tracking
--------------------

.. fr:: Reading statistics
   :id: FR-5_1
   :status: open
   :priority: P0
   :links: UC-5_1

   User can view comprehensive reading progress and statistics.

   **Acceptance criteria:**

   - Metrics: total time read, books completed, pages read, current streaks
   - Per-book stats: time spent, sessions, reading velocity
   - Visual charts and graphs
   - Comparison to previous periods

.. fr:: Statistics filtering
   :id: FR-5_2
   :status: open
   :priority: P1
   :links: UC-5_2

   User can filter statistics by time frame and book selection.

   **Acceptance criteria:**

   - Time frames: today, week, month, year, custom range
   - Filter by: specific books, shelves, tags
   - Export statistics data
   - Save filter presets

.. fr:: Cross-device sync
   :id: FR-5_3
   :status: open
   :priority: P0
   :links: UC-7_3

   System synchronizes reading progress, metadata, and annotations across all logged-in devices via the metadata server.

   **Acceptance criteria:**

   - Reading position syncs within 30 seconds when online
   - Metadata, shelves, tags, annotations sync automatically
   - Offline changes queued and sync when connection restored
   - Conflict resolution: latest timestamp wins for position, merge for metadata
   - Sync status indicator visible in app (synced, syncing, offline, error)
   - Requires metadata server connection (self-hosted or official)

   See :doc:`/design/server-architecture` for sync details.

----

6. Goal management
------------------

.. fr:: Reading goals
   :id: FR-6_1
   :status: open
   :priority: P1
   :links: UC-6_1

   User can create time-based reading goals.

   **Acceptance criteria:**

   - Goal types: books per period, pages per period, time per period
   - Periods: daily, weekly, monthly, yearly, custom
   - Multiple active goals allowed
   - Goal templates for quick creation

.. fr:: Manual goal updates
   :id: FR-6_2
   :status: open
   :priority: P1
   :links: UC-6_2

   User can manually update goal progress values.

   **Acceptance criteria:**

   - Increment/decrement progress
   - Set exact value
   - Add notes to progress updates
   - History of manual updates

.. fr:: Automatic goal progress
   :id: FR-6_3
   :status: open
   :priority: P1
   :links: UC-6_2

   System automatically updates goal progress based on reading activity.

   **Acceptance criteria:**

   - Book completion updates book-count goals
   - Reading time updates time-based goals
   - Pages read updates page-count goals
   - Progress is calculated in real-time

.. fr:: Goal notifications
   :id: FR-6_4
   :status: open
   :priority: P2
   :links: UC-6_2

   System sends notifications about goal progress and reminders.

   **Acceptance criteria:**

   - Reminder notifications (configurable frequency)
   - Milestone notifications (50%, 75%, complete)
   - Streak notifications
   - Notifications can be disabled per goal

----

7. Storage and synchronization
------------------------------

.. fr:: File storage backend selection
   :id: FR-7_1
   :status: open
   :priority: P0
   :links: UC-7_1

   User can choose where book files are stored from application settings.

   **Acceptance criteria:**

   - Options: device local, Google Drive, OneDrive, Dropbox, WebDAV, MinIO/S3, dedicated Papyrus server
   - Multiple backends can be configured simultaneously
   - One backend is designated as primary for new uploads
   - Files can be migrated between backends without data loss
   - Backend configuration accessible from Settings > Storage
   - Connection status and storage usage displayed

   See :doc:`/design/server-architecture` for details.

.. fr:: Metadata server configuration
   :id: FR-7_1_1
   :status: open
   :priority: P0
   :links: UC-7_1

   User can configure connection to a metadata server for cross-device synchronization.

   **Acceptance criteria:**

   - Default: use official hosted server (optional)
   - Self-hosted option: user provides server URL
   - Server URL validation and connection testing
   - Login/registration on metadata server
   - Clear indication when offline or disconnected
   - Works without metadata server (local-only mode)

.. fr:: File upload
   :id: FR-7_2
   :status: open
   :priority: P0
   :links: UC-2_1

   User can upload book files from their device.

   **Acceptance criteria:**

   - File picker with format filtering
   - Drag-and-drop support (desktop/web)
   - Progress indicator for large files
   - Duplicate detection

.. fr:: OCR processing
   :id: FR-7_3
   :status: open
   :priority: P2
   :links: UC-7_2

   System can apply OCR to scanned documents for text extraction.

   **Acceptance criteria:**

   - Processes PDF files with scanned images
   - Text becomes searchable after OCR
   - Processing happens in background
   - Quality/confidence indicator shown
   - Multiple language support

.. fr:: Plugin system
   :id: FR-7_4
   :status: open
   :priority: P3

   System supports optional plugins for extended functionality.

   **Acceptance criteria:**

   - Plugin types: metadata sources, storage backends, reader features
   - Plugins are sandboxed for security
   - Enable/disable individual plugins
   - Plugin marketplace/repository

.. fr:: OPDS catalog support
   :id: FR-7_5
   :status: open
   :priority: P2
   :links: UC-7_4

   User can browse and download books from OPDS catalogs.

   **Acceptance criteria:**

   - Add OPDS catalog URLs
   - Browse catalog hierarchy
   - Search within catalogs
   - Download books directly to library
   - Authentication for protected catalogs
