"""Loads one incident's query + document corpus from its data folder.
Used by tests, benchmark, and candidates alike - not something you need
to modify.
"""
from __future__ import annotations

from pathlib import Path

DATA_DIR = Path(__file__).parent


def load_incident(name: str) -> tuple[str, dict[str, str]]:
    """Returns (query, corpus) where corpus maps filename -> full document
    text, for every *.md and *.csv file in data/<name>/. Not every
    document type is the same format - known_issues, for one, is a CSV
    catalog, not prose - your retrieval needs to work over raw text
    either way, not assume every corpus value is markdown.
    """
    incident_dir = DATA_DIR / name
    query = (incident_dir / "query.txt").read_text(encoding="utf-8").strip()
    paths = sorted(incident_dir.glob("*.md")) + sorted(incident_dir.glob("*.csv"))
    corpus = {p.name: p.read_text(encoding="utf-8") for p in paths}
    return query, corpus
