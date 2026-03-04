# Interactive Mermaid Diagrams Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the static Mermaid SVG rendering with interactive pan/zoom diagrams using the `mkdocs-mermaid2` plugin and `panzoom` library.

**Architecture:** Swap `pymdownx.superfences` mermaid fence for `mkdocs-mermaid2` plugin, which exposes Mermaid's JS initialization lifecycle. A small initialization script attaches `panzoom` to each rendered SVG after Mermaid finishes drawing it. Double-click resets the view.

**Tech Stack:** MkDocs Material, mkdocs-mermaid2, panzoom (CDN)

---

### Task 1: Install mkdocs-mermaid2

**Files:**
- Modify: `mkdocs.yml`

**Step 1: Install the plugin**

```bash
pip install mkdocs-mermaid2-plugin
```

Expected output: `Successfully installed mkdocs-mermaid2-plugin-x.x.x`

**Step 2: Verify the existing site builds cleanly before touching anything**

```bash
mkdocs build --strict 2>&1 | tail -20
```

Expected: `INFO - Documentation built successfully.` (note any warnings for reference)

**Step 3: Commit baseline**

```bash
git add -A
git commit -m "chore: install mkdocs-mermaid2-plugin"
```

---

### Task 2: Swap Mermaid rendering from superfences to mermaid2 plugin

**Files:**
- Modify: `mkdocs.yml`

Current state of the relevant section in `mkdocs.yml`:

```yaml
plugins:
  - search:
      separator: '[\s\-\.]+'

markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

**Step 1: Add `mermaid2` to plugins and remove the mermaid custom fence**

Replace the plugins block and superfences config so it looks like this:

```yaml
plugins:
  - search:
      separator: '[\s\-\.]+'
  - mermaid2

markdown_extensions:
  - pymdownx.superfences
```

Note: Keep `pymdownx.superfences` — it's still needed for other fenced code blocks. Just remove the `custom_fences` list entirely (mermaid2 plugin handles mermaid fences itself).

**Step 2: Build and verify diagrams still render**

```bash
mkdocs serve
```

Open http://127.0.0.1:8000/database-model/ in a browser. The ER diagram should be visible. Check a few other pages with diagrams: `server-architecture/`, `entities/`, `actors/`.

If diagrams are blank, check the browser console for JS errors.

**Step 3: Commit**

```bash
git add mkdocs.yml
git commit -m "feat: switch mermaid rendering to mkdocs-mermaid2 plugin"
```

---

### Task 3: Add panzoom library via CDN

**Files:**
- Modify: `mkdocs.yml`

**Step 1: Add panzoom CDN to extra_javascript**

In `mkdocs.yml`, find the `extra_javascript` block:

```yaml
extra_javascript:
  - javascripts/extra.js
```

Add the panzoom CDN **before** `extra.js` (order matters — it must be loaded first):

```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/panzoom@9.4.3/dist/panzoom.min.js
  - javascripts/extra.js
```

**Step 2: Verify panzoom loads**

```bash
mkdocs serve
```

Open browser console on any page. Type `panzoom` — it should return the function, not `undefined`.

**Step 3: Commit**

```bash
git add mkdocs.yml
git commit -m "feat: add panzoom library via CDN"
```

---

### Task 4: Initialize panzoom on rendered Mermaid diagrams

**Files:**
- Modify: `src/javascripts/extra.js`

Current file contents (`src/javascripts/extra.js`):

```js
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('a[href^="http"]').forEach(function (link) {
    if (!link.hostname.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });
});
```

**Step 1: Add panzoom initialization after the existing code**

Append the following block to the end of `src/javascripts/extra.js`:

```js
// Initialize pan/zoom on Mermaid diagrams after they render.
// mkdocs-mermaid2 exposes mermaid.initialize() and triggers rendering,
// so we use a MutationObserver to detect when each .mermaid container
// receives its SVG child, then attach panzoom.
document.addEventListener('DOMContentLoaded', function () {
  var containers = document.querySelectorAll('.mermaid');
  if (!containers.length) return;

  containers.forEach(function (container) {
    var observer = new MutationObserver(function (mutations, obs) {
      var svg = container.querySelector('svg');
      if (!svg) return;

      obs.disconnect();

      // Remove fixed width/height so the SVG fills its container.
      svg.removeAttribute('width');
      svg.removeAttribute('height');
      svg.style.width = '100%';
      svg.style.height = 'auto';

      var instance = panzoom(svg, {
        contain: 'outside',
        maxZoom: 10,
        minZoom: 0.3,
      });

      // Double-click resets zoom and pan.
      svg.addEventListener('dblclick', function () {
        instance.reset();
      });
    });

    observer.observe(container, { childList: true, subtree: true });
  });
});
```

**Step 2: Verify interactivity in the browser**

```bash
mkdocs serve
```

Open http://127.0.0.1:8000/database-model/. The ER diagram should:
- Pan when you click and drag
- Zoom when you scroll
- Reset when you double-click

Also test on http://127.0.0.1:8000/server-architecture/ (multiple diagrams on one page).

**Step 3: Commit**

```bash
git add src/javascripts/extra.js
git commit -m "feat: attach panzoom to mermaid diagrams after render"
```

---

### Task 5: Add CSS affordance for interactive diagrams

**Files:**
- Modify: `src/stylesheets/extra.css`

**Step 1: Add cursor and interaction styles**

The existing `.mermaid` rule in `src/stylesheets/extra.css` is:

```css
.mermaid {
  text-align: center;
  margin: 1.5rem 0;
}
```

Replace it with:

```css
.mermaid {
  text-align: center;
  margin: 1.5rem 0;
  overflow: hidden;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 4px;
}

.mermaid svg {
  cursor: grab;
  display: block;
  margin: 0 auto;
}

.mermaid svg:active {
  cursor: grabbing;
}
```

**Step 2: Verify styles**

```bash
mkdocs serve
```

Open http://127.0.0.1:8000/database-model/. The diagram should have a subtle border and the cursor should change to a hand when hovering.

**Step 3: Commit**

```bash
git add src/stylesheets/extra.css
git commit -m "feat: add grab cursor and border to interactive mermaid diagrams"
```

---

### Task 6: Final verification

**Step 1: Full build with strict mode**

```bash
mkdocs build --strict 2>&1
```

Expected: `INFO - Documentation built successfully.` with no errors.

**Step 2: Manually check each page with diagrams**

Pages to check:
- `database-model/` — ER diagram (most complex, primary target)
- `server-architecture/` — multiple diagrams
- `entities/` — entity diagram
- `actors/` — actor diagram
- `market-analysis/` — diagram
- `technologies/` — diagram

For each: confirm pan, zoom, and double-click reset work.

**Step 3: Commit**

```bash
git add -A
git commit -m "chore: verify interactive mermaid diagrams complete"
```
