"""Sphinx configuration for the GNN prototype instance."""

from __future__ import annotations

import sys
from pathlib import Path

project = "FEMIC GNN Prototype"
author = "UBC-FRESH"
copyright = "2026, UBC-FRESH"

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

extensions: list[str] = ["sphinx.ext.napoleon"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_title = "FEMIC GNN Prototype"
