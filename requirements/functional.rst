Functional requirements
=======================

These are product commitments, not a list of released capabilities. See
:doc:`index` for status definitions.

1. User management
------------------

.. fr:: Account registration
   :id: FR-1_1
   :status: partial
   :priority: P0
   :links: UC-1_1

   User can create an account using an email address and password.

   **Acceptance criteria:**

   - Email must be valid and unique in the system
   - Password must meet minimum security requirements (8+ characters, mixed case, number)
   - Email verification is sent upon registration
   - Account remains pending verification until the address is verified
   - Registration does not issue an authenticated application session before verification
   - Verification links are single-use, expire after 24 hours, and can be resent with rate limiting
   - Guest use remains available without verification and keeps its own separate library

   **Implementation:** Registration and verification services exist, but
   registration currently creates an authenticated session. Requiring verification
   first needs coordinated changes to the server and the client registration flow.

   Email ownership is required because the address identifies the account and
   supports recovery. See `OWASP authentication guidance
   <https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html>`_.

.. fr:: Email/password login
   :id: FR-1_2
   :status: partial
   :priority: P0
   :links: UC-1_2

   User can log in to the system using email and password.

   **Acceptance criteria:**

   - System validates credentials against stored hash
   - Email verification is required before sign-in
   - Unverified users can request a new verification email without receiving library access
   - Failed attempts are rate-limited (max 5 per minute)
   - Successful login creates a secure session token
   - User is redirected to their library after login

   **Implementation:** Email/password login exists, but the server does not
   currently enforce email verification before issuing a session.

.. fr:: OAuth login (Google)
   :id: FR-1_3
   :status: partial
   :priority: P1
   :links: UC-1_3

   User can log in using their Google account via OAuth 2.0.

   **Acceptance criteria:**

   - Google OAuth flow completes securely
   - New users are automatically registered on first OAuth login
   - Existing users can link Google account to email account
   - Google profile photo and name are imported (optional)
   - Google identity is identified by the validated provider subject, not by email alone
   - Google's verification satisfies the email requirement for Gmail addresses or verified Google Workspace addresses
   - Other addresses require Papyrus email verification before sign-in
   - Linking to an existing account requires proof of control of that account

   See `Google's guidance on email ownership and backend authentication
   <https://developers.google.com/identity/sign-in/android/backend-auth>`_.

.. fr:: Offline mode
   :id: FR-1_4
   :status: partial
   :priority: P0
   :links: UC-1_4

   User can use the application in offline mode without credentials or internet connection.

   **Acceptance criteria:**

   - All reading and library management features work offline
   - Data is stored locally on device
   - No account required for offline-only usage
   - Guest and signed-in libraries remain separate when registering, signing in, or signing out
   - Guest data is never automatically copied, merged, or uploaded into an account
   - Libraries and cached media remain isolated across users and server profiles
   - Offline reading uses locally available files, and search exposes local index coverage

   **Implementation:** Guest and account database scopes are separate.
   This does not establish every offline reading, annotation, or search criterion.

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

   **Implementation:** The server's default reset-link expiry is currently
   60 minutes, which differs from the 24-hour requirement.

.. fr:: Account deletion
   :id: FR-1_6
   :status: partial
   :priority: P1
   :links: UC-1_6

   User can permanently delete their account and all associated data.

   **Acceptance criteria:**

   - In-app deletion uses the current authenticated session without another sign-in
   - The public deletion resource requires password or linked-Google authentication
   - Users can request deletion from the application and from an accessible web resource
   - Before confirmation, show the data affected and the exact permanent-deletion deadline
   - Scheduling deletion revokes active sessions and starts a 30-day recovery window
   - During that window, authenticated recovery allows the user to explicitly cancel deletion and immediately resume their session
   - Signing in for recovery does not silently cancel deletion or restore ordinary account access
   - After the deadline, permanently delete the account and associated server data, including managed media
   - Explain any exceptional retention and backup expiry in the published retention policy
   - Local device data remains unless explicitly deleted

   The recovery window is a Papyrus product decision. Google Play requires
   discoverable deletion requests and actual deletion, but does not prescribe
   this 30-day window. See `Google Play's account deletion requirements
   <https://support.google.com/googleplay/android-developer/answer/13327111?hl=en>`_.

   **Implementation:** Settings and the public server deletion resource support
   deletion through the current app session or password/linked-Google verification
   on the public resource, session revocation, explicit recovery with immediate sign-in,
   and automatic permanent cleanup with retryable media removal. The client warns
   about the 30-day recovery period before confirmation and shows the exact deletion
   date after scheduling. A dated preview before confirmation remains available
   on the public web resource but is not implemented in the simplified client flow.
   Local device data remains. Automated backups are not implemented.
   The planned future backup-retention limit is 30 days after permanent deletion,
   and restore tooling must reapply deletions before serving restored data.
   Self-hosted deployments must configure their actual exceptional-retention notice.
   Live provider and production deployment acceptance remain outstanding.

----

Authentication implementation tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. task:: Define the verification-before-sign-in HTTP contract
   :id: TASK-AUTH-01
   :status: open
   :priority: P0
   :component: docs
   :readiness: ready
   :implements: FR-1_1;FR-1_2;FR-1_3
   :validation: make build; make requirements; review every response against server auth schemas and client token handling

   **Scope:**

   Specify the pending-verification and successful-sign-in request/response
   contracts in the authentication architecture documentation. Inspect the
   existing client and server before choosing response shapes. This task changes
   documentation, not application behavior.

   **Acceptance criteria:**

   - Define registration, login, resend, verify, refresh, and Google exchange outcomes with HTTP codes and payload examples
   - Define how unverified Google addresses complete Papyrus verification without receiving library-access tokens
   - Define expired and reused links, email delivery failures, resend limits, and account-enumeration behavior
   - Explain how verified users and guest libraries are preserved through the change
   - Identify the exact schemas, routes, client models, and tests affected
   - Record a rollout order that keeps client/server changes compatible during deployment
   - Keep password policy changes, account deletion, and full-library search outside this task

.. task:: Enforce verified sign-in in the authentication service
   :id: TASK-AUTH-02
   :status: open
   :priority: P0
   :component: server
   :readiness: ready
   :implements: FR-1_1;FR-1_2;FR-1_3
   :depends_on: TASK-AUTH-01
   :validation: tools/papyrus check server; tools/papyrus test server -- tests/api/routes/test_auth.py tests/services/test_auth.py; use a distinct test database and exclude external provider smoke tests

   **Scope:**

   Implement the accepted verification contract from TASK-AUTH-01 in server
   schemas, routes, and authentication services. Preserve existing ownership,
   session revocation, token rotation, and OAuth identity-linking protections.

   **Acceptance criteria:**

   - Registration creates a pending account and dispatches verification without granting application access
   - Unverified email/password and non-authoritative Google addresses cannot obtain or refresh application access
   - Verification, resend, expiration, and retry behavior match the approved contract
   - Verified Google identities follow the documented authority rules
   - Tests cover successful sign-in, rejected access, expired/reused verification, and existing verified accounts
   - PR describes any migration and deployment ordering needed by the client task
   - Public API changes are exported for a coordinated documentation snapshot update

.. task:: Implement pending-verification client flows
   :id: TASK-AUTH-03
   :status: open
   :priority: P0
   :component: client
   :readiness: ready
   :implements: FR-1_1;FR-1_2;FR-1_3;FR-1_4
   :depends_on: TASK-AUTH-01;TASK-AUTH-02
   :validation: tools/papyrus check client; focused auth/provider/widget tests; web compile; visual check of narrow mobile and desktop authentication layouts

   **Scope:**

   Consume the accepted server contract and guide users through verification.
   Update auth models, repository/provider behavior, registration/login UI,
   callbacks, and tests without changing guest-library ownership.

   **Acceptance criteria:**

   - Pending registration leads to verification guidance rather than the library
   - Resend, expired-link, invalid-link, Google verification, and retry states are actionable
   - No authenticated session or signed-in library is installed before verification succeeds
   - Guest data remains separate during registration, verification, sign-in, cancellation, and sign-out
   - Verified users can complete sign-in using the existing supported platform callbacks
   - Widget and persistence regressions cover success, errors, cancellation, and profile isolation
   - PR provides platform evidence and identifies any unrun device checks

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

   System provides full-text search across the contents of the entire active library.

   **Acceptance criteria:**

   - Search includes books whose files are not downloaded on the current device
   - Search supports text extraction from EPUB, TXT, and PDFs containing extractable text
   - Scanned pages without extractable text require OCR before their contents can be searched
   - Search scope stays within the active guest library or user and server profile
   - Results show matched text with context
   - Search is case-insensitive by default
   - Results link directly to location in book
   - Opening a result can request downloading the book when its file is not available locally
   - Indexing progress, failures, and unsupported content are visible, so incomplete coverage is not presented as a complete search
   - Offline search uses locally available indexes and clearly indicates any unavailable coverage

   Library-wide indexing, remote search, and offline index availability require
   dedicated technical design. This requirement does not select an indexing
   engine or imply that full-text search is currently implemented.

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

   **Implementation:** The client reader adapter currently launches EPUB and PDF.
   Other listed formats remain targets. Metadata import support does not
   establish reader support.

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
   :status: partial
   :priority: P0
   :links: UC-7_3

   System synchronizes reading progress, metadata, and annotations across all logged-in devices via the metadata server.

   **Acceptance criteria:**

   - Reading position syncs within 30 seconds when online
   - Metadata, shelves, tags, annotations sync automatically
   - Offline changes queued and sync when connection restored
   - Conflict resolution uses one server-authoritative last-write-wins policy as defined by :need:`NFR-2_3`
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

   - Options: device local, Google Drive, OneDrive, Dropbox, WebDAV, MinIO/S3, NAS via SMB/NFS, dedicated Papyrus server
   - Multiple backends can be configured simultaneously
   - One backend is designated as primary for new uploads
   - Files can be migrated between backends without data loss
   - Backend configuration accessible from Settings > Storage
   - Connection status and storage usage displayed
   - Backend selection is explicit, with no automatic failover or cross-provider replication requirement

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
