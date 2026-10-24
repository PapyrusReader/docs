User manual
===========

Papyrus manages physical and digital books, with a built-in EPUB/PDF reader.
Feature availability depends on the application version and platform.

Getting started
---------------

Use the `Papyrus client releases
<https://github.com/PapyrusReader/client/releases>`_ for available application
packages. The `client README
<https://github.com/PapyrusReader/client#readme>`_ describes installation and
platform details.

Choose **Continue offline** to use a guest library without an account. Your
books and library data are stored locally. Signing in opens a separate account
library. It does not transfer the guest library into that account.

Importing and organizing books
-------------------------------

Import book files through the library's import controls. EPUB and PDF can be
opened in the reader. Native metadata import also accepts several additional
formats, but importing a file does not mean its contents can be read in Papyrus.
The web file picker accepts EPUB and PDF.

Use shelves, tags, metadata editing, and library filters to organize books.
Physical books can be represented by metadata without a readable file.

Reading
-------

Open an EPUB or PDF from the library. Use the available reader controls for
navigation, appearance, and reading layout. Options vary with the file format.
Reading positions are saved by the application.

The reader currently supports reflowable EPUB and PDF. Fixed-layout EPUB and
DRM-protected content are not supported. Book-level notes, annotations, and
bookmarks should not be confused with selecting and highlighting text in the
reader, which remains unfinished.

Accessibility settings
----------------------

Open **Settings > Accessibility**. These preferences take effect immediately
and are stored on this device, shared across guest and signed-in profiles.

- **Interface text enlargement** adds 15%, 30%, 50%, or 100% to the system's
  existing text scaling. **System default** adds no enlargement. The system's
  nonlinear scaling curve is preserved. A live preview shows the result.
- **Increase contrast** follows the system when off and forces increased
  contrast when on, in either light or dark mode. E-ink uses its own contrast
  treatment, so this control is disabled while that appearance is selected.
- **Bold interface text** follows the system when off and adds bold interface
  text when on, including editable fields and navigation.
- **Interface font** offers **System default** and **OpenDyslexic** with a live
  preview. This is a personal reading preference, not a claim that a particular
  font improves reading for every person with dyslexia.
- **Reduce animations** limits interface motion. System reduced motion is
  always honored, and e-ink also reduces motion.

Additional interface text enlargement and bold text do not change embedded
reader text metrics. Reader controls retain system scaling and bold-text
settings, and book rendering retains the reader's own preferences. These
settings do not change books, saved positions, or reading preferences.

Accounts and offline access
---------------------------

An account connects a library to a Papyrus server for synchronization. Different
users and server profiles have separate libraries and cached media.

In **Settings > Account**, users can edit their display name and choose
a profile photo directly. **Save** applies both changes together. JPEG and PNG
photos up to 5 MB and 25 megapixels are supported. Photos are resized and image
metadata is removed before saving. In anonymous mode, the name and photo are
saved on this device without a network connection and survive app restarts.
They stay separate from signed-in profiles and are removed when the anonymous
account is deleted. Signed-in profile changes are saved to the account's server.
Email is shown for reference and cannot be edited here.

Books need to be available locally to read without a network connection.
Synchronization and online catalogs require connectivity. Full-library content
search is a product requirement and is not currently an available feature.

Local storage is not a substitute for an independent backup. Before uninstalling
the app or clearing browser storage, preserve any local-only files and data you
need to retain.

Account deletion and recovery
-----------------------------

Open **Settings > Account > Delete account**. Review the warning about the
30-day recovery period and choose **Delete account**. Your current signed-in session
authorizes the request without another password or Google sign-in. The receipt shows
the deletion date. Cancelling the dialog leaves the account unchanged.

Confirmation disables ordinary access and revokes all Papyrus sessions. Existing
short-lived PowerSync credentials expire within their configured lifetime and
cannot be renewed. Local libraries and cached files remain on your devices.
To recover, sign in normally before the deletion date. Papyrus will offer to keep
your account. Choose **Keep account** to restore access and open your library
immediately, without signing in again. Choosing **Not now**
leaves deletion scheduled. Sign-in alone never cancels deletion automatically.
When server email delivery is enabled, your verified email address receives a
deletion notice with the deadline, or a confirmation when you keep the account.

Deletion and recovery are also available without installing the app at the server's
``/v1/account-deletion`` URL (or its configured API prefix). After the deadline,
the server automatically deletes the account and its owned records, then removes
managed media and the account's local acquisition import directory. Files held by
external providers or download clients must be managed with those providers.
Storage failures are retried without restoring account access.

Automated database and media backups are not currently implemented. The planned
retention limit for future backups is 30 days after permanent deletion. Future
restore tooling must reapply deletions before serving restored data. Self-hosted
operators must publish any separate backup or exceptional-retention policy using
``ACCOUNT_DELETION_RETENTION_NOTICE``. This configuration changes the notice,
not backup behavior.


Troubleshooting
---------------

- If an imported file cannot be opened, check that it is a supported EPUB or PDF.
- If a book is unavailable offline, check whether its file has been downloaded.
- If the library appears different after signing in, check the active user and
  server profile. The guest library is separate.
- If synchronization is unavailable, check the server address and connection.
  Avoid clearing local data to troubleshoot unsynchronized changes.

Report reproducible application problems in the `client issue tracker
<https://github.com/PapyrusReader/client/issues>`_, including the application
version, platform, and steps to reproduce.
