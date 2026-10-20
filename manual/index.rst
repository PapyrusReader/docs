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

Accounts and offline access
---------------------------

An account connects a library to a Papyrus server for synchronization. Different
users and server profiles have separate libraries and cached media.

Books need to be available locally to read without a network connection.
Synchronization and online catalogs require connectivity. Full-library content
search is a product requirement and is not currently an available feature.

Local storage is not a substitute for an independent backup. Before uninstalling
the app or clearing browser storage, preserve any local-only files and data you
need to retain.

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
