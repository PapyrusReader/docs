"""Sphinx configuration for Papyrus documentation."""

project = "Papyrus"
copyright = "2025, Papyrus"
author = "Papyrus"

extensions = [
    "sphinx_needs",
    "sphinxcontrib.mermaid",
    "sphinx.ext.graphviz",
]

# -- Theme -------------------------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "Papyrus"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#5654A8",
        "color-brand-content": "#5654A8",
    },
    "dark_css_variables": {
        "color-brand-primary": "#C3C0FF",
        "color-brand-content": "#C3C0FF",
    },
}

# -- Sphinx-Needs ------------------------------------------------------------

needs_types = [
    dict(
        directive="fr",
        title="Functional Requirement",
        prefix="FR-",
        color="#7C6FD4",
        style="node",
    ),
    dict(
        directive="nfr",
        title="Non-Functional Requirement",
        prefix="NFR-",
        color="#D49A6F",
        style="node",
    ),
    dict(
        directive="uc",
        title="Use Case",
        prefix="UC-",
        color="#6FA8D4",
        style="artifact",
    ),
]

needs_flow_engine = "graphviz"

needs_graphviz_styles = {
    "furo": {
        "graph": {
            "bgcolor": "transparent",
            "pad": "0.3",
            "nodesep": "0.4",
            "ranksep": "0.6",
        },
        "node": {
            "fontname": "system-ui, -apple-system, sans-serif",
            "fontsize": "11",
            "fontcolor": "#333333",
            "style": "filled,rounded",
            "penwidth": "1.2",
            "color": "#cccccc",
        },
        "edge": {
            "color": "#999999",
            "arrowsize": "0.7",
            "penwidth": "1.0",
            "fontname": "system-ui, -apple-system, sans-serif",
            "fontsize": "9",
            "fontcolor": "#777777",
        },
    },
}

needs_fields = {
    "priority": {
        "type": "core",
        "description": "Requirement priority level",
        "schema": {"type": "string"},
    },
    "actors": {
        "type": "core",
        "description": "Use case actors",
        "schema": {"type": "string"},
    },
    "status": {
        "type": "core",
        "description": "Implementation status",
        "schema": {
            "enum": ["open", "in_progress", "implemented", "verified", "deferred"],
        },
    },
}

needs_id_required = True
needs_id_regex = r"^(FR|NFR|UC)-[0-9]+_[0-9]+(_[0-9]+)?$"

needs_default_style = ""
needs_role_need_template = "{title} ({id})"

# -- Graphviz ----------------------------------------------------------------

graphviz_output_format = "svg"

# -- Mermaid -----------------------------------------------------------------

mermaid_output_format = "raw"

# -- General -----------------------------------------------------------------

exclude_patterns = [
    "_build",
    "src",
    ".venv",
    "venv",
    "site",
    "Thumbs.db",
    ".DS_Store",
    "CLAUDE.md",
    "README.md",
]

templates_path = ["_templates"]
