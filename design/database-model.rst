Database model
==============

Entity relationship diagram
---------------------------

.. mermaid::

   erDiagram
       USER {
           uuid user_id PK
           string display_name
           string_opt email UK
           string_opt password_hash
           string_opt external_login_id UK
           boolean is_anonymous
           boolean is_active
           boolean email_verified
           object_opt preferences
           datetime_opt last_login_at
       }

       BOOK {
           uuid book_id PK
           uuid user_id FK
           string title
           string_opt subtitle
           json authors
           string_opt publisher
           date_opt publication_date
           string_opt language
           string_opt isbn10
           string_opt isbn13
           text_opt description
           string_opt cover_image_url
           enum book_type
           string_opt digital_file_path
           string_opt file_format
           bigint_opt file_size
           string_opt file_hash
           string_opt physical_location
           string_opt lent_to
           datetime_opt lent_at
           enum reading_status
           integer_opt current_page
           decimal_opt current_position
           string_opt current_cfi
           boolean is_favorite
           integer_opt rating
           datetime_opt started_at
           datetime_opt completed_at
           datetime added_at
           datetime_opt last_read_at
           uuid_opt series_id FK
           decimal_opt series_number
           uuid_opt storage_backend_id FK
           object_opt custom_metadata
           boolean is_ocr_processed
           decimal_opt ocr_confidence
       }

       SHELF {
           uuid shelf_id PK
           uuid user_id FK
           uuid_opt parent_shelf_id FK
           string name
           text_opt description
           string_opt color
           string_opt icon
           boolean is_default
           boolean is_smart
           string_opt smart_query
           integer_opt sort_order
       }

       TAG {
           uuid tag_id PK
           uuid user_id FK
           string name
           string color
           text_opt description
           integer_opt usage_count
       }

       SERIES {
           uuid series_id PK
           uuid user_id FK
           string name
           text_opt description
           string_opt author
           integer_opt total_books
           boolean is_complete
       }

       ANNOTATION {
           uuid annotation_id PK
           uuid book_id FK
           uuid user_id FK
           text selected_text
           text_opt note
           string highlight_color
           string start_position
           string end_position
           string_opt chapter_title
           integer_opt chapter_index
           integer_opt page_number
       }

       NOTE {
           uuid note_id PK
           uuid book_id FK
           uuid user_id FK
           string title
           text content
           boolean is_pinned
       }

       BOOKMARK {
           uuid bookmark_id PK
           uuid book_id FK
           uuid user_id FK
           string position
           integer_opt page_number
           string_opt chapter_title
           string_opt note
           string_opt color
       }

       READING_SESSION {
           uuid session_id PK
           uuid user_id FK
           uuid book_id FK
           datetime start_time
           datetime_opt end_time
           decimal_opt start_position
           decimal_opt end_position
           integer_opt pages_read
           integer_opt duration_minutes
           string_opt device_type
           string_opt device_name
       }

       READING_GOAL {
           uuid goal_id PK
           uuid user_id FK
           string title
           text_opt description
           enum goal_type
           integer target_value
           integer current_value
           enum time_period
           date start_date
           date end_date
           boolean is_active
           boolean is_completed
           datetime_opt completed_at
       }

       READING_PROFILE {
           uuid profile_id PK
           uuid user_id FK
           string name
           boolean is_default
           string_opt font_family
           integer_opt font_size
           integer_opt font_weight
           decimal_opt line_height
           decimal_opt letter_spacing
           decimal_opt paragraph_spacing
           enum_opt text_alignment
           integer_opt horizontal_margin
           integer_opt vertical_margin
           string_opt background_color
           string_opt text_color
           string_opt link_color
           string_opt selection_color
           enum_opt theme_mode
           enum_opt reading_mode
           boolean_opt page_turn_animation
           integer_opt column_count
           boolean_opt hyphenation
       }

       METADATA_SERVER_CONFIG {
           uuid config_id PK
           uuid user_id FK, UK
           string server_url
           enum server_type
           string_opt auth_token
           string_opt refresh_token
           boolean is_connected
           boolean sync_enabled
           integer_opt sync_interval_seconds
           datetime_opt last_sync_at
           enum_opt sync_status
           string_opt sync_error_message
       }

       FILE_STORAGE_BACKEND {
           uuid backend_id PK
           uuid user_id FK
           enum backend_type
           string name
           boolean is_primary
           boolean is_active
           object connection_config
           object_opt credentials
           string_opt base_path
           bigint_opt storage_used_bytes
           bigint_opt storage_quota_bytes
           datetime_opt last_accessed_at
           enum_opt connection_status
           string_opt error_message
       }

       SAVED_FILTER {
           uuid filter_id PK
           uuid user_id FK
           string name
           text_opt description
           string query
           enum_opt filter_type
           string_opt icon
           string_opt color
           boolean is_pinned
           integer_opt usage_count
           datetime_opt last_used_at
       }

       BOOK_SHELF {
           uuid book_id PK, FK
           uuid shelf_id PK, FK
           integer_opt sort_order
       }

       BOOK_TAG {
           uuid book_id PK, FK
           uuid tag_id PK, FK
       }

       USER ||--o{ BOOK : owns
       USER ||--o{ SHELF : owns
       USER ||--o{ TAG : owns
       USER ||--o{ SERIES : owns
       USER ||--o{ ANNOTATION : creates
       USER ||--o{ NOTE : writes
       USER ||--o{ BOOKMARK : creates
       USER ||--o{ READING_SESSION : tracks
       USER ||--o{ READING_GOAL : sets
       USER ||--o{ READING_PROFILE : saves
       USER ||--o| METADATA_SERVER_CONFIG : configures
       USER ||--o{ FILE_STORAGE_BACKEND : configures
       USER ||--o{ SAVED_FILTER : saves

       BOOK }o--o| SERIES : belongs_to
       BOOK }o--o| FILE_STORAGE_BACKEND : stored_in
       BOOK ||--o{ ANNOTATION : has
       BOOK ||--o{ NOTE : has
       BOOK ||--o{ BOOKMARK : has
       BOOK ||--o{ READING_SESSION : has

       SHELF ||--o{ SHELF : parent_child

       BOOK ||--o{ BOOK_SHELF : in_shelves
       SHELF ||--o{ BOOK_SHELF : contains_books

       BOOK ||--o{ BOOK_TAG : has_tags
       TAG ||--o{ BOOK_TAG : assigned_to_books
