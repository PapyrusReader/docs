Watched device folders
======================

This client feature implements the device-folder portion of FR-2_6. It requires
no new server endpoint, replicated field or server migration.

Library workflow
----------------

**Library → Folders** uses the Library toolbar and page margins with responsive
table rows with Folder, Status, Books, Destination shelf and Last checked columns
and a contextual action. Books shows the number of associated books currently in
the library, without a repeated unit suffix.
The editable connection name sits above the source location. Native desktop
pickers supply the absolute path. Browser pickers expose only the selected
directory name. Rows and detail headers omit the subtitle when no actual path
is available. Narrow layouts reflow each row while keeping
its status, book count and action together. Upload counts remain separate. Mobile uses the Library floating action button. Empty libraries show
one connect action in the empty state.

Opening a folder uses a content-sized bottom sheet on desktop and mobile. Its
header groups the folder name, location and overflow menu. Status appears above
View books and Scan now. Compact properties show destination shelf, subfolders
and last successful check. Edit folder is in the header overflow menu. View books applies the
**Advanced filters → Source folders** facet. It uses the existing filter count
and Reset action, with no separate chip or additional row above the Library
filters. Multiple source folders combine with the other filter categories.

**Name** defaults to the selected folder name during setup and can be changed
in **Edit folder**, alongside recursion and destination shelf. The custom name
is profile-local and survives restarting or reconnecting. It does not rename
the source directory or change duplicate detection.
Changes require **Save changes**, apply to future discoveries and survive restart.
Edit opens above the folder details sheet. Cancel and Save return to those
details, with saved changes reflected immediately. Scan now runs without
dismissing the details sheet. Cancel leaves the saved preferences unchanged. Pause and Resume take effect
immediately from the sheet overflow menu. Deleted shelves show a recovery state
without blocking library imports. Secondary actions cover retry and file review.
Stop watching lives in the overflow menu and explains that imported books remain in the confirmation dialog.

**Add book → Connect folder** invokes the system picker immediately. The standard
bottom sheet stays over Library on desktop and mobile and combines preview with
configuration. The source location is a labeled read-only field, followed by
Name, destination shelf and recursion. Books found and Total size appear as
separate preview values, with file problems expandable only when present.
A short note appears only when manual selection is required. Canceling
releases the selected access reference and creates no connection. Empty folders
can be connected. A browser without persistent access displays **Import folder**
and explains that later additions require selecting it again.

Forms reuse the compact shared header, scrollable body, outlined Cancel and filled
primary action, theme tokens and motion policy. Enlarged text wraps actions, and
e-ink progress remains static. Progress indicators reserve their space in the
table, details and setup preview. Scanning is indeterminate. Importing shows
processed/total counts, the remaining count and a determinate bar, without
moving adjacent rows or controls. Completed attempts include duplicates and
failures, so progress is separate from the number of books added to the library. Folder operations do not show snackbars. Status and import counts remain in
the folder list and details. Action errors appear in the owning page or sheet.

Imported copies remain available when source files move or disappear. Watching
is add-only. Changed content offers Keep existing or Import as separate book.
Deleting a book records its fingerprint as excluded, including renamed copies.
Review files provides explicit reimport. Removing a shelf does not stop imports.

Client boundaries
-----------------

``DirectoryAccess`` owns selection, restored permission, incremental enumeration,
stat/read operations, optional events and grant release. Native adapters use
filesystem paths on Windows/Linux, persisted SAF tree permissions on Android,
and bookmarked, coordinated access on Apple platforms. Browsers use directory
handles stored in IndexedDB when supported, otherwise a one-time file selection.
Automatic scans verify permission without displaying permission prompts.

``FolderRepository`` stores local-only connections, observed files, jobs,
folder-book associations, exclusions, retired access grants and a renewable lease in a separate profile-scoped PowerSync SQLite
database. This database never connects to PowerSync. Account-cache resets do not
discard it. Paths and grants never enter book metadata or upload payloads.
Folder-book associations survive importing a changed source as a separate book.
Grant replacements commit before releasing the old permission, and failed release
work remains journaled for a later scan or restart.

``WatchedFolders`` owns lifecycle scheduling, reconciliation and UI state. Scans
run on activation/resume, manual requests and a 60-second timer. Filesystem
events are debounced for two seconds. Mobile and browser work requires an active
application. Desktop watching continues while the application is running.
Closed-app background services are outside this feature.

The coordinator processes one file at a time per profile. The lease prevents
competing local windows from processing jobs concurrently. Reconciliation reloads
persisted folder settings so another window cannot revive a stopped connection.
Hidden files, temporary downloads and symlinks are skipped. Enumeration does not
load book contents. A metadata-only discovery pass collects changed/new candidates
and recovery jobs before importing, fixing the batch total. Unchanged files
are reconciled without inflating progress, and a recovery job and its source
file count as one work item. Counters are transient and rebuilt after restart.
Stable size/modification information is checked before and
after reading, with SHA-256 used for exact-content identity. Native metadata and
hash processing use an isolate, and web processing uses the import worker and
asynchronous browser cryptography.
Providers may omit size or modification information. Unknown sizes are excluded
from preview totals, which are labeled Unknown or At least. Files without usable
timestamps use repeated observation and content hashing. Future timestamps do
not indefinitely postpone imports.

``LibraryFolderImportTarget`` captures ``BookImportSession``, repository ownership
and the media scope. Imports use preallocated UUIDs. The journal retains pending,
prepared and failed jobs across file copying, metadata persistence, shelf
assignment and media-queue submission. Recovery checks stored bytes and existing
books, preserving existing reading progress and retrying missing queue work.
These stores are not treated as one atomic transaction. Profile changes invalidate
work before another destination becomes active.
Journaled imports keep committed books and covers if upload-queue persistence
fails. Retrying repairs the queue without removing or replacing those books.
Explicit deletion cancels pending folder work for that book, and reimport uses a
new identity so a server deletion tombstone cannot discard the requested import.

Supported browser imports are EPUB/PDF. Native imports use the existing EPUB,
PDF, MOBI, AZW3, TXT, CBR and CBZ support. Reading in Papyrus currently supports
EPUB and PDF, which is distinct from metadata import support.

Offline web packaging
---------------------

After building the web client, run::

   python tools/prepare_web_offline.py app/build/web

The release packager runs this automatically during ``stamp-web``. It creates a
versioned manifest and stamps ``papyrus_service_worker.js``. The worker precaches
public application assets, reader runtimes and import dependencies. It never
caches authenticated API responses or user media. A partial download does not
replace the previous complete cache. Application updates activate after existing
tabs close.

Offline reopening requires a completed initial online installation. Browser
storage eviction and revoked permissions require recovery, and browser storage
is not permanent. Cloud-provider files must be downloaded before they can be
imported offline.

Validation and platform acceptance
----------------------------------

Automated coordinator tests cover read-only preview, initial imports, additions,
recursion, shelves, unchanged-file skipping, exact duplicates and renames,
changed-file choices, deletion exclusions, stable retry identities, staged-file
recovery, profile changes, permissions, pause, stop, shared leases and a
10,000-entry cancellable preview. Widget tests cover direct picker invocation,
confirmation and cancellation at mobile and desktop sizes, explicit preference
saves, profile changes, folder filtering, stable headers and enlarged e-ink text. Web tests cover
offline cache isolation and interrupted installation. These checks do not replace
operating-system or physical-device acceptance.

Before release, verify separately:

* Windows/Linux: native folder picker, new files, removable drive reconnect,
  subfolders, unreadable entries and Linux reconciliation without recursive events.
* macOS: sandbox bookmark restoration after restart, revoked access, coordinated
  cloud-provider reads and filesystem notifications.
* Android: SAF tree grants after restart, restricted roots, revoked grants and
  provider files unavailable offline.
* iOS/iPadOS: folder picker, bookmark restoration and foreground catch-up with
  local and cloud-provider files.
* Browsers: persisted handles, explicit permission reconnection, fallback folder
  selection, offline reopening, storage eviction and two competing tabs.
* Libraries: guest restart and clear, account import while offline, later metadata
  and media upload, account-cache reset and profile changes during processing.
* Reading: open an imported EPUB/PDF offline, restart without duplicates, discover
  a later addition and confirm that the source files are unchanged.

Run the existing two-client PowerSync integration harness against configured
test services for synchronization. Report actual device checks separately from
compilation, automated tests and integration-harness results.

Review verification, 2026-11-01
-------------------------------

The focused folder, import-commit, media-queue and repository tests pass, including
provider metadata omissions, future timestamps, failed grant replacement and
cleanup, deletion/profile races, expired leases and source-folder associations
after restart. Client formatting and analysis, Node web tests, Chrome transport
tests and offline-packaging tests pass.

PR preparation also validates a clean client checkout with the committed reader
pin and no local dependency override: all 152 focused folder, import, queue,
repository and library-provider tests pass, and analysis reports no issues.

* Web: release compilation passes. An isolated headless Chrome profile persisted
  real directory handles in IndexedDB, reloaded the packaged Flutter application
  with networking disabled, restored and enumerated the handle, and imported an
  EPUB through the production worker. Source and imported SHA-256 hashes matched.
  The picker was substituted with an OPFS directory handle, so this does not
  establish OS picker or revoked-permission acceptance.
* Android: debug APK compilation passes. Grant-channel tests cover cursor cleanup
  and unknown sizes. SAF providers, restricted roots and device restart still
  require physical-device acceptance.
* macOS: the ordinary debug build and live integration test pass. The Xcode
  project and CocoaPods dependency targets now use the existing 12.0 minimum.
  Both configurations include outgoing network entitlements. Bookmark and drive
  acceptance remain unrun.
* iOS/iPadOS: the ordinary debug simulator build passes with the installed Xcode
  27.1. CocoaPods dependencies now honor the existing iOS 15.0 minimum. Debug
  simulators select the host architecture, including Intel hosts, to avoid
  `Flutter issue 188461 <https://github.com/flutter/flutter/issues/188461>`_.
  Device and release architecture settings are unchanged, and the unsigned iOS
  release build passes. Folder picker, bookmarks and cloud-provider behavior
  require device acceptance.
* Linux: all 76 focused folder tests pass in an isolated Ubuntu 24.04 x64
  container using the pinned Flutter 3.41.2. This includes real filesystem
  enumeration, recursion, filtering, source reads, symlink rejection and
  unavailable roots. The release build passes. The clean build exposed a missing
  LLVM linker dependency, now installed by the shared Linux setup script. A
  ten-second headless launch stayed running, with container graphics/portal and
  unavailable-keyring warnings. This does not establish keyring or picker
  acceptance. Desktop picker and removable-drive acceptance remain unrun.
* Windows: the filesystem tests now use Windows path conventions and keep
  non-symlink coverage enabled. Native execution remains pending on a Windows
  runner. The installed Parallels service was unavailable, so no Windows build
  or physical-device acceptance is claimed.

The complete live two-client harness now passes: offline account folder import,
restart without duplication, queued upload after reconnecting, media visibility
on the second client, deletion and account isolation. The local test service was
upgraded from ``a8b9c0d1e234`` to the existing ``b9c0d1e2f345`` migration, restoring
the ``bookmarks.reader_locator`` column expected by the current server model.
No new migration or server code was needed.

Linux and Windows packaging workflows run the focused folder tests before
building. Linux now triggers for client code and test changes, as Windows already
did. Recursion, hidden/temporary file filtering, source reads and traversal tests
run on both systems. Only symlink-creation tests are skipped on Windows hosts
without configured symlink privileges. Workflow validation passes locally.

Generated design-review pages, captures, logs and copied fixtures were removed
from the workspace. Optional widget captures now write under the ignored
``client/app/build/folder-review`` directory. Temporary CocoaPods workspace
integration and its untracked macOS lockfile were removed. The tracked iOS lockfile
reflects the updated Podfile. The pre-existing local reader override is preserved.
