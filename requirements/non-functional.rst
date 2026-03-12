Non-functional Requirements
===========================

1. Storage
----------

.. nfr:: Maximum file size
   :id: NFR-1_1
   :status: open
   :priority: P0

   Maximum allowed file size shall not exceed 2048 MB (2 GB) per book file.

   **Acceptance criteria:**

   - Files up to 2 GB upload successfully
   - Files exceeding 2 GB are rejected with clear error message
   - Large file uploads show progress indicator
   - Upload can be resumed after interruption (for files > 100 MB)

.. nfr:: Storage backend support
   :id: NFR-1_2
   :status: open
   :priority: P0

   The system shall support multiple storage backends.

   **Supported Backends:**

   1. Local storage (device file system)
   2. Cloud storage: Google Drive, OneDrive, Dropbox
   3. Self-hosted server (MinIO, local file system)
   4. Network-attached storage (NAS via SMB/NFS)

   **Acceptance criteria:**

   - Each backend can be configured independently
   - User can switch between backends without data loss
   - Backend credentials are stored securely (encrypted)
   - Connection status is visible to user

.. nfr:: Multi-backend configuration
   :id: NFR-1_3
   :status: open
   :priority: P1

   The system shall support multiple storage backends per user with automatic failover.

   **Acceptance criteria:**

   - User can configure up to 3 storage backends
   - One backend is designated as primary
   - Automatic failover to secondary if primary is unavailable
   - Manual override to force specific backend

.. nfr:: File encryption
   :id: NFR-1_4
   :status: open
   :priority: P2

   File encryption shall be available for sensitive content with user-controlled keys.

   **Acceptance criteria:**

   - AES-256 encryption for files at rest
   - User-managed encryption keys
   - Encrypted files are decrypted on-device only
   - Key recovery mechanism available

----

2. Synchronization
------------------

.. nfr:: Online/offline parity
   :id: NFR-2_1
   :status: open
   :priority: P0

   The system shall work in online and offline mode with full feature parity for core reading features.

   **Acceptance criteria:**

   - All reading features work offline
   - Library management works offline
   - Annotations and notes work offline
   - Only sync and cloud features require connectivity
   - Clear indicator of online/offline status

.. nfr:: Offline change indicators
   :id: NFR-2_2
   :status: open
   :priority: P0

   Any changes made offline shall have an appropriate visual indicator.

   **Acceptance criteria:**

   - Unsynced items show sync-pending icon
   - Last sync timestamp visible in settings
   - Number of pending changes displayed
   - User can manually trigger sync when online

.. nfr:: Conflict resolution
   :id: NFR-2_3
   :status: open
   :priority: P1

   Synchronization conflicts shall be resolved with user-selectable strategies.

   **Resolution Strategies:**

   1. Server wins (default)
   2. Client wins
   3. Manual resolution (user chooses)
   4. Merge (where possible)

   **Acceptance criteria:**

   - User can set default strategy in settings
   - Per-conflict override option
   - Conflict history log
   - No silent data loss

.. nfr:: Sync performance
   :id: NFR-2_4
   :status: open
   :priority: P0

   Cross-device synchronization shall complete within 30 seconds under normal network conditions (>= 1 Mbps).

   **Acceptance criteria:**

   - Reading position syncs within 30 seconds
   - Metadata changes sync within 1 minute
   - Book files sync based on file size and bandwidth
   - Background sync does not impact reading performance

----

3. Platform support
-------------------

.. nfr:: Web browser support
   :id: NFR-3_1
   :status: open
   :priority: P0

   The system shall be available in modern web browsers.

   **Supported Browsers:**

   - Chrome 90+
   - Firefox 90+
   - Safari 14+
   - Edge 90+

   **Acceptance criteria:**

   - All core features work in supported browsers
   - Progressive Web App (PWA) installable
   - Offline capability via service worker
   - Responsive design for all viewport sizes

.. nfr:: Desktop operating system support
   :id: NFR-3_2
   :status: open
   :priority: P0

   The system shall be available on major desktop operating systems.

   **Supported Operating Systems:**

   - Windows 10 or later
   - macOS 10.15 (Catalina) or later
   - Major Linux distributions (Ubuntu 20.04+, Fedora 35+, Debian 11+)

   **Acceptance criteria:**

   - Native application available for each platform
   - Platform-specific keyboard shortcuts
   - System tray/menu bar integration
   - File association for supported formats

.. nfr:: Mobile operating system support
   :id: NFR-3_3
   :status: open
   :priority: P0

   The system shall work on mobile devices.

   **Supported Platforms:**

   - Android 8.0 (API level 26) or later
   - iOS 12.0 or later

   **Acceptance criteria:**

   - App available in Google Play Store and Apple App Store
   - Touch-optimized interface
   - Support for device orientation changes
   - Background sync support
   - Push notifications (optional)

.. nfr:: E-ink device support
   :id: NFR-3_4
   :status: open
   :priority: P1

   The system shall support e-ink readers and tablets with touch interfaces.

   **Target Devices:**

   - Kobo readers (via sideloading)
   - Android-based e-ink devices (Boox, Hisense)
   - reMarkable (future consideration)

   **Acceptance criteria:**

   - E-ink optimized UI mode (high contrast, grayscale)
   - Reduced/disabled animations
   - Larger touch targets (minimum 48px)
   - Support for hardware page-turn buttons
   - Reduced screen refresh for battery efficiency
   - Dark-on-light and light-on-dark themes optimized for e-ink

----

4. Performance
--------------

.. nfr:: Application startup
   :id: NFR-4_1
   :status: open
   :priority: P0

   Application startup time shall not exceed 3 seconds on supported devices.

   **Acceptance criteria:**

   - Cold start < 3 seconds on mid-range devices (2020+)
   - Warm start < 1 second
   - Library view loads within 2 seconds of app start
   - Progress indicator shown if startup exceeds 1 second

.. nfr:: Book opening
   :id: NFR-4_2
   :status: open
   :priority: P0

   Book opening time shall not exceed 2 seconds for files up to 50 MB.

   **Acceptance criteria:**

   - EPUB < 50 MB opens in < 2 seconds
   - PDF < 50 MB opens in < 3 seconds
   - Progress indicator for larger files
   - Last reading position restored automatically
   - Opening performance measured on mid-range devices

.. nfr:: Search performance
   :id: NFR-4_3
   :status: open
   :priority: P0

   Search results shall be returned within 1 second for libraries up to 10,000 books.

   **Acceptance criteria:**

   - Metadata search returns in < 500ms
   - Full-text search returns in < 1 second
   - Results are paginated for large result sets
   - Search is cancelable
   - Incremental results shown as available

.. nfr:: Library scalability
   :id: NFR-4_4
   :status: open
   :priority: P1

   The system shall support libraries with up to 50,000 books without performance degradation.

   **Acceptance criteria:**

   - Library view loads in < 3 seconds with 50,000 books
   - Search remains under 2 seconds
   - Scrolling remains smooth (60 FPS on capable devices)
   - Memory usage scales linearly with library size
   - Virtual scrolling for large lists

.. nfr:: E-ink performance
   :id: NFR-4_5
   :status: open
   :priority: P1

   The system shall be optimized for e-ink display refresh characteristics.

   **Acceptance criteria:**

   - Page turns complete in < 500ms
   - Minimal full-refresh operations
   - Partial refresh used where possible
   - UI updates batched to reduce flicker
   - Animation duration configurable (default: 0 for e-ink)

----

5. Usability
------------

.. nfr:: Design system
   :id: NFR-5_1
   :status: open
   :priority: P0

   The user interface shall follow Material 3 design guidelines.

   **Acceptance criteria:**

   - Consistent use of Material 3 components
   - Dynamic color theming support
   - Consistent typography scale
   - Proper use of elevation and surfaces
   - Dark/light theme support

.. nfr:: Accessibility
   :id: NFR-5_2
   :status: open
   :priority: P0

   The application shall be accessible to users with disabilities (WCAG 2.1 AA compliance).

   **Acceptance criteria:**

   - Screen reader compatibility (TalkBack, VoiceOver)
   - Minimum color contrast ratio 4.5:1
   - All interactive elements keyboard accessible
   - Focus indicators visible
   - Text scalable up to 200%
   - No information conveyed by color alone
   - Touch targets minimum 44x44 points

.. nfr:: RTL and internationalization
   :id: NFR-5_3
   :status: open
   :priority: P1

   The system shall support right-to-left (RTL) languages and internationalization.

   **Acceptance criteria:**

   - UI mirrors correctly for RTL languages
   - Book content renders correctly for RTL text
   - Date/time formats localized
   - Number formats localized
   - Bidirectional text support

.. nfr:: Localization
   :id: NFR-5_4
   :status: open
   :priority: P1

   All user-facing text shall be localizable.

   **Acceptance criteria:**

   - English as primary language
   - Localization framework in place for additional languages
   - No hardcoded user-facing strings
   - Locale can be overridden in settings
   - Pluralization rules supported

.. nfr:: E-ink usability
   :id: NFR-5_5
   :status: open
   :priority: P1

   The system shall provide optimized usability for e-ink displays.

   **Acceptance criteria:**

   - High contrast theme option
   - Simplified UI with fewer visual elements
   - Large, clear typography
   - Reduced reliance on hover states
   - Clear button/touch feedback without animations

----

6. Security
-----------

.. nfr:: Password security
   :id: NFR-6_1
   :status: open
   :priority: P0

   User passwords shall be hashed using industry-standard algorithms.

   **Acceptance criteria:**

   - Passwords hashed with bcrypt or Argon2
   - Minimum password length: 8 characters
   - Password strength indicator during registration
   - No plaintext password storage or transmission
   - Secure password reset mechanism

.. nfr:: Transport security
   :id: NFR-6_2
   :status: open
   :priority: P0

   All data transmission shall use TLS 1.3 or higher encryption.

   **Acceptance criteria:**

   - HTTPS required for all API communication
   - Certificate pinning for mobile apps (optional)
   - No fallback to unencrypted connections
   - TLS 1.2 minimum (1.3 preferred)

.. nfr:: Two-factor authentication
   :id: NFR-6_3
   :status: open
   :priority: P2

   The system shall support two-factor authentication (TOTP).

   **Acceptance criteria:**

   - TOTP-based 2FA (Google Authenticator compatible)
   - Backup codes available
   - 2FA can be enabled/disabled by user
   - Graceful recovery if 2FA device lost

.. nfr:: Session management
   :id: NFR-6_4
   :status: open
   :priority: P0

   Session management shall include automatic timeout and secure token handling.

   **Acceptance criteria:**

   - JWT tokens with configurable expiration
   - Refresh token rotation
   - Sessions can be revoked remotely
   - Automatic logout after inactivity (configurable)
   - Secure token storage on device

.. nfr:: Privacy by default
   :id: NFR-6_5
   :status: open
   :priority: P0

   The application shall collect no analytics by default; telemetry is opt-in.

   **Acceptance criteria:**

   - No analytics without explicit consent
   - Clear privacy policy accessible in-app
   - Telemetry settings easily accessible
   - No third-party tracking SDKs by default
   - Data collection scope clearly explained

----

7. Reliability
--------------

.. nfr:: System uptime
   :id: NFR-7_1
   :status: open
   :priority: P1

   The system shall have 99.5% uptime for self-hosted deployments under normal conditions.

   **Acceptance criteria:**

   - Maximum planned downtime: 4 hours/month
   - Health check endpoints available
   - Graceful degradation during partial outages
   - Automatic recovery from transient failures

.. nfr:: Data integrity
   :id: NFR-7_2
   :status: open
   :priority: P0

   Data corruption shall be prevented through checksums and integrity verification.

   **Acceptance criteria:**

   - File checksums verified on upload/download
   - Database transactions are atomic
   - Corrupted files detected and reported
   - No silent data corruption

.. nfr:: Network resilience
   :id: NFR-7_3
   :status: open
   :priority: P0

   The system shall gracefully handle network interruptions without data loss.

   **Acceptance criteria:**

   - Operations are idempotent where possible
   - Uploads/downloads resumable
   - No data loss on network failure
   - Clear error messages for network issues
   - Automatic retry with exponential backoff

.. nfr:: Backup and restore
   :id: NFR-7_4
   :status: open
   :priority: P1

   Automatic backup and restore capabilities shall be available for user data.

   **Acceptance criteria:**

   - Export all user data in portable format
   - Import/restore from backup
   - Scheduled automatic backups (optional)
   - Backup integrity verification

----

8. Extensibility
----------------

.. nfr:: Plugin architecture
   :id: NFR-8_1
   :status: open
   :priority: P3

   The architecture shall support modular plugins without compromising core stability.

   **Acceptance criteria:**

   - Plugin API documented
   - Plugins run in sandboxed environment
   - Core functionality unaffected by plugin failures
   - Plugin enable/disable without restart
   - Version compatibility checking

----

9. Maintainability
------------------

.. nfr:: Code quality
   :id: NFR-9_1
   :status: open
   :priority: P1

   The codebase shall maintain high quality standards.

   **Acceptance criteria:**

   - Automated linting (dart analyze)
   - Code formatting enforced (dart format)
   - Minimum 70% test coverage for core functionality
   - No critical security vulnerabilities
   - Documentation for public APIs

.. nfr:: Logging and monitoring
   :id: NFR-9_2
   :status: open
   :priority: P1

   The system shall provide comprehensive logging and monitoring capabilities.

   **Acceptance criteria:**

   - Structured logging for all components
   - Log levels configurable (debug, info, warning, error)
   - No sensitive data in logs
   - Log rotation and retention policies
   - Error tracking integration (optional)
