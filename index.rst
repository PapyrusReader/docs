Papyrus
=======

Overview
--------

Papyrus is an open-source application for reading and managing both physical and digital books. It provides a versatile, user-friendly system that makes reading comfortable and fun across Android, iOS, Web, Desktop (Windows, macOS, Linux), and e-ink devices. Papyrus features an intuitive, familiar, modern UI with extensive customization options, unifying book organization, reading, note-taking, progress tracking, and personalized settings in a single application.

Goals
-----

1. **Cross-platform** - manage books seamlessly across all devices without relearning the UI.
2. **Integrated reader** - read uploaded books with extensive customization options.
3. **Flexible management** - organize books into shelves, categories, add tags, edit metadata and track physical books.
4. **Progress tracking** - track reading time, books read, and manage and complete goals.
5. **Storage flexibility** - choose between local (i.e., on device), self-hosted, or cloud storage provider for storing book files.
6. **Data ownership** - ability to export everything in open formats (e.g., JSON, CSV, ZIP).
7. **Extensible** - plugin system for metadata sources, storage, and reader features.
8. **Developer friendly** - public and documented API and SDKs, server self-hosting.

Target audience
---------------

- Regular readers who read digital and/or physical books and want a centralized library management solution.
- Habit builders who want to track reading statistics and build reading habits through goals and gamification.
- Multi-device users who want to read and access the same data on phones, tablets, e-readers, and PCs interchangeably.

Supported platforms
-------------------

- Android (8.0+).
- iOS (12.0+).
- Web (Chrome, Firefox, Safari, Edge).
- Windows (10+).
- macOS (10.15+).
- Linux.
 
Supported file formats
------------------------

1. EPUB.
2. PDF.
3. AZW3.
4. MOBI.
5. TXT.
6. FB2.
7. CBR/CBZ.
8. CBT/CB7.
9. ODT
10. DJVU.

Feature overview
----------------

Core features
~~~~~~~~~~~~~

**1. Book management**

- Import books from the file system or cloud services (Google Drive, OneDrive, Dropbox)
- Organize with shelves, user-defined collections (e.g., "Currently Reading", "Sci-Fi")
- Tag books with color-coded labels (0-10 tags per book)
- Edit metadata manually or fetch from online sources (`Open Library <https://openlibrary.org/developers/api>`_, `Google Books <https://developers.google.com/books>`_)
- Search and filter by title, author, tags, shelves, reading progress, text contents
- Physical book tracking, manually scanning and tracking physical books

**2. Integrated book reader**

Typography controls:

- Font family selection (built-in and custom fonts)
- Font size, weight, line, character and paragraph spacing
- Text alignment (left, right, center, justified)

Appearance:

- Background color themes (light, dark, sepia, custom)
- Text and link color customization
- Adjustable margins and padding
- Brightness controls
- Zoom with lock and auto-fit to screen

Navigation:

- Single-page and two-page layouts
- Paginated and continuous scroll modes
- Table of contents navigation
- Go-to-page/percentage jump with ability to get back to the previous location
- Progress bar with position (e.g., page, percentage toggle) indicator
- Touch zones, swipe gestures, volume key navigation

Reading profiles:

- Save named customized presets of all reader settings
- Switch between profiles in the reader
- Default profile per device
- Profile import/export to a file

**3. Annotations and notes**

- Annotate text with multiple colors (built-in and freely selectable from a color wheel)
- Add notes to annotations or create standalone book notes
- Create bookmarks for quick navigation
- Export annotations to a file (text, JSON, CSV, PDF, or Markdown)
- Search across all annotations and notes

**4. Reading progress and goals**

Automatic tracking:

- Reading time per book and total
- Pages/percentage read
- Books started, in progress, completed
- Reading velocity statistics

Goals:

- Time-based goals (e.g., "Read 30 minutes daily")
- Book count goals (e.g., "Read 12 books this year")
- Custom goals with manual progress updates
- Visual progress indicators and charts

Synchronization:

- Reading position synced across devices
- Progress and statistics synchronized

**5. Storage and sync**

Storage options:

- On-device (default, no account required)
- Self-hosted server
- Cloud storage (Google Drive, OneDrive, Dropbox)

Offline support:

- Full offline functionality without account on all platforms
- Automatic sync when online (with an account)

Advanced features
~~~~~~~~~~~~~~~~~

These features are planned for future releases, and may not be seriously considered for implementation:

- Format conversion between formats (create a book copy or replace existing)
- OPDS catalog browsing to download from online catalogs
- OCR processing to extract text from scanned document or book files
- Audiobook support to manage and play audiobooks with synchronized progress
- Text-to-speech to read books aloud
- Social features to share progress, reviews, and recommendations (Goodreads style)
- AI-powered features, such as summaries, recommendations, smart categorization, text-to-speech
- ISBN barcode scanning for adding physical books by scanning with a phone or laptop camera
- Plugin system which extend functionality with community plugins

Related documents
~~~~~~~~~

.. toctree::
   :maxdepth: 1
   :caption: Requirements

   requirements/index
   requirements/functional
   requirements/non-functional

.. toctree::
   :maxdepth: 1
   :caption: System design

   design/actors
   design/use-cases
   design/entities
   design/database-model
   design/server-architecture

.. toctree::
   :maxdepth: 1
   :caption: Implementation

   implementation/technologies
   implementation/user-interface

.. toctree::
   :maxdepth: 1
   :caption: API

   api/index

.. toctree::
   :maxdepth: 1
   :caption: Reference

   external/index
