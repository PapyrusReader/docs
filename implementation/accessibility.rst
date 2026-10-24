Accessibility foundation audit
==============================

Scope and standard
------------------

This increment targets `WCAG 2.2 Level AA <https://www.w3.org/TR/WCAG22/>`_,
with `WCAG2ICT <https://www.w3.org/TR/wcag2ict-22/>`_ guidance for native software.
WCAG2ICT interprets WCAG for non-web documents and software. It is not a separate
conformance certification. Requirement :need:`NFR-5_2` remains open.

The scope is client authentication, primary navigation, library search and
selection, book details/editing, file import, Settings, and the shared controls,
menus, dialogs, and sheets those journeys use. Passing the checks below is not
full-app conformance. Reader-engine remediation, EPUB/PDF content, read-aloud,
reading guides, and broader pages such as goals, statistics, and online catalogs
are outside this increment's audit.

Implementation contract
-----------------------

``PreferencesProvider`` stores device-wide interface enlargement, increased
contrast, and bold text alongside the existing font and motion settings.
Unsupported saved enlargement values fall back to System default. No server
schema, synchronization payload, or database migration changes are involved.

``AppAccessibilityScope`` retains the system text scaler and bold-text flag before
applying overrides. Enlargement multiplies each result of the original scaler,
rather than replacing its nonlinear curve with a linear estimate. System bold
text and reduced motion cannot be disabled by an app preference. Light and dark
high-contrast themes use Material's maximum contrast setting and build component
themes from that palette. E-ink retains its separate palette and motion policy.
OpenDyslexic is bundled with its license and applies to all theme variants.

``ReaderSystemTextScope`` restores system text metrics and bold text around the
embedded reader and reader panels. Reader preferences, book rendering settings,
and stored locators are unchanged. Tests of the adapter boundary do not evaluate
the accessibility of book content.

Audit matrix
------------

Results refer to local verification on 24 October 2026. **Automated** means the
specified regression scenario passes, not that every instance of the criterion
has been evaluated. **Pending** means acceptance evidence is still required.
Test paths below are relative to ``client/app/test``.

.. list-table:: Criteria, scenarios, and evidence
   :header-rows: 1
   :widths: 19 28 35 18

   * - Criteria
     - Scenario and remediation
     - Evidence
     - Result / limit
   * - 1.3.1, 4.1.2: information, relationships, names, roles, states
     - Settings toggles expose one labeled state and one action, including
       disabled state. Picker choices expose radio selection. Search and icon actions
       have names. Decorative covers do not duplicate book titles.
     - ``themes/app_accessibility_test.dart``,
       ``widgets/profile/accessibility_settings_section_test.dart``,
       ``widgets/accessibility_journeys_test.dart``.
     - Automated for sampled controls. Native announcements pending.
   * - 1.3.2, 2.4.3: reading and focus order
     - Nested page navigators must not remove the primary navigation from the
       accessibility tree. The shell provides a semantics boundary. Settings pickers use the root
       modal layer so background navigation is hidden until dismissal.
     - ``widgets/shell/navigation_counts_test.dart`` checks mobile and desktop
       navigation remains exposed. Chrome accessibility-tree inspection found
       the original defect and verified navigation after remediation. The
       regression also checks picker selection and restoration of focus.
     - Automated regression. Complete native reading-order review pending.
   * - 1.4.3, 1.4.11: contrast
     - Normal, dark, e-ink, and high-contrast palettes. Auth errors pair error
       background with on-error foreground. Divider labels use readable text
       color. Cover overlays retain their original translucent styling.
     - Flutter text-contrast guideline checks for shared settings toggles,
       book actions, and search in all five themes.
     - Automated sample. Image content and every color/state combination are
       not certified by these checks.
   * - 1.4.4, 1.4.10: text enlargement and reflow
     - Settings and auth at 320, 390, and 1280 logical pixels. System 200%
       combined with app +100% retains 400% effective enlargement. Keyboard
       inset does not hide auth submission. Navigation labels remain scalable.
     - ``widgets/accessibility_journeys_test.dart``,
       ``widgets/profile/accessibility_settings_section_test.dart``,
       ``widgets/accessibility_library_journeys_test.dart``.
     - Automated scenarios. Device font rendering and browser zoom still
       require platform acceptance.
   * - 2.1.1, 2.1.2, 2.4.7, 2.4.11: keyboard and focus
     - Whole-row toggle activation, keyboard activation, reduced-motion focus
       retention, explicit library action menus, keyboard-operable star ratings,
       and dialog dismissal.
     - ``themes/app_accessibility_test.dart``,
       ``widgets/app_motion_control_test.dart``,
       ``themes/eink_input_focus_test.dart``. Chrome keyboard inspection checks
       dialog Escape dismissal and focus restoration.
     - Automated shared controls and sampled browser behavior. Exhaustive
       focus visibility/containment across native dialogs pending.
   * - 2.5.1, 2.5.7: alternatives to gestures and dragging
     - Desktop card actions appear on hover or keyboard focus and retain
       programmatic labels. Compact cover overlays retain the original design.
       File import offers Browse files alongside desktop drop. Sheets retain
       explicit actions and dismiss behavior.
     - ``widgets/library/book_card_test.dart``,
       ``widgets/library/book_list_item_test.dart``,
       ``widgets/add_book/book_import_sheet_test.dart``.
     - Automated sampled actions. Touch card gesture alternatives and
       compact overlay target sizing remain gaps. No reader gesture audit.
   * - 2.5.8: target size
     - Standalone touch controls use at least 48 logical-pixel hit areas even
       when artwork is smaller. This product target is stricter than WCAG AA's
       24 CSS-pixel minimum, which has defined spacing and other exceptions.
     - Flutter Android (48) and iOS (44) tap-target guidelines on sampled
       settings, search, and book detail action controls. Compact cover
       overlays retain their original 30-pixel targets and are an exception
       to the product target, not covered by those guideline checks.
     - Automated sample. Flutter logical pixels and CSS pixels/points are
       platform-specific units, not a universal physical-size equivalence.
   * - 1.4.1, 3.3.1, 3.3.2, 4.1.3: errors and status
     - Invalid auth input has text errors and retains focus/input. Import
       failures have a live region. Selection has checked/selected state.
       Completion snackbars use Flutter's live-region semantics. Progress
       updates are not individually announced.
     - Auth validation tests, import state tests, existing completion/error
       paths, and settings semantics tests.
     - Automated behavior and code inspection. Actual announcement timing
       with VoiceOver/TalkBack pending.
   * - 3.3.8: accessible authentication
     - Login permits password paste and provides email/password autofill hints.
       Registration/recovery provide new-password hints. Visibility buttons
       are named Show password / Hide password.
     - ``widgets/accessibility_journeys_test.dart`` exercises paste and
       visibility and inspects autofill hints.
     - Automated. External password-manager integration pending.
   * - System preferences and reader isolation
     - Live system/app changes, nonlinear scaling, storage reload, malformed
       preferences, fonts, contrast, bold text, reduced motion, and reader
       boundary behavior.
     - ``providers/accessibility_preferences_test.dart``,
       ``themes/app_accessibility_test.dart``,
       ``widgets/profile/accessibility_settings_section_test.dart``, existing
       reader adapter and persistence tests.
     - Automated. No reader-package or stored-position schema change.

Platform acceptance
-------------------

Chrome on macOS was used to inspect the actual Flutter web accessibility tree,
verify exposed primary navigation and filter-button roles, activate Settings
controls, preview +100% text enlargement and OpenDyslexic, confirm preferences
survive reload, and verify that the font picker hides background navigation
and exposes radio choices. Escape dismissal and restoration of focus were checked
from a confirmation dialog. Accessibility-tree inspection is not equivalent to
listening to a screen reader.

The following remain pending and must not be reported as passed:

- VoiceOver on macOS/iOS: navigate representative auth, library, details/edit,
  import, and Settings journeys. Check order, single announcements, live-region
  timing, rotor access, and restoration after dialogs and sheets.
- TalkBack on Android: repeat those journeys with system large text, bold text,
  high contrast where available, and reduced motion. No Android target was
  available in the local device inventory for this increment.
- Native keyboard traversal and external password-manager acceptance on each
  supported platform. Confirm focus is visible and not obscured at every step.
- Broader app pages and EPUB/PDF content accessibility, including document
  structure, alternative text, reading order, and reader-engine interactions.

Local validation results
------------------------

- Full client suite: 1,927 passed, 19 skipped. The skipped tests are not counted
  as accessibility acceptance evidence.
- Client quality checks: formatting, analysis, and four web bootstrap tests.
- Chrome regressions verify saved guest avatars decode after browser-storage
  reload, Settings scrolling works over empty space, and short desktop sections
  remain aligned at the top. Account form checks cover 320, 390, and 1280 logical
  pixels at normal and 200% text size.
- Release web compilation: passed, including Flutter's Wasm dry-run check.
- Documentation: warning-as-error Sphinx build passed.
- Chrome inspection: primary navigation and Settings controls exposed, live
  enlargement observed, and a confirmation dialog dismissed with Escape with
  focus restored. VoiceOver and TalkBack are not included in these results.

Reproduction
------------

Run focused preference, theme, and journey tests, followed by the full client
suite and ``tools/papyrus check client``. Build the web client with the pinned
Flutter SDK and local dart defines. Build this documentation with ``make build``
from ``docs``. Validation used the workspace's existing local reader path override, which was
preserved. Remote CI was not run. Test success, compilation, browser inspection,
and assistive technology acceptance are separate forms of evidence.
