# Interactive Mermaid Diagrams Design

**Date:** 2026-03-05
**Status:** Approved

## Problem

Mermaid diagrams rendered as static SVG are unusable for complex diagrams (ER, architecture, etc.) — no zoom, pan, or drag. There are 10 diagrams across 6 files currently affected.

## Approach

Replace the current `pymdownx.superfences` mermaid custom fence with the `mkdocs-mermaid2` plugin, which exposes Mermaid's JavaScript lifecycle hooks. Use those hooks to attach the `panzoom` library to each rendered SVG for inline interactivity.

No changes to any `.md` source files are required.

## Components

### `mkdocs.yml`
- Remove the `mermaid` custom fence from `pymdownx.superfences.custom_fences`
- Add `mermaid2` to `plugins`
- Add `panzoom` CDN URL to `extra_javascript`

### `javascripts/extra.js`
- After Mermaid renders each diagram, initialize `panzoom` on the SVG element
- Configure `contain: "outside"` to prevent diagram from being panned out of view
- Bind double-click to reset zoom/pan to original state

### `stylesheets/extra.css`
- `cursor: grab` on `.mermaid svg`
- `cursor: grabbing` on `.mermaid svg:active`
- Optional: reset-view button style

## Behavior

| Interaction | Result |
|---|---|
| Scroll | Zoom in / out |
| Click-drag | Pan |
| Double-click | Reset position and scale |

Applies uniformly to all diagram types (ER, flowchart, sequence, class, etc.).

## Out of Scope

- Opening diagrams in a separate page or window
- Changes to diagram source (`.md` files)
- Server-side diagram rendering
