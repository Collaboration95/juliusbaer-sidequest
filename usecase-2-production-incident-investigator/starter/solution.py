"""Copy this file into your own submissions/<your-name>/solution.py and
implement investigate(). See ../README.md for the full brief.

Required interface - do not change the signature:

    def investigate(query: str, corpus: dict) -> dict:
        # corpus: filename -> full document text, e.g.
        #   {"logs.md": "...", "architecture.md": "...", "api_specs.md": "...",
        #    "deployment_history.md": "...", "previous_incidents.md": "...",
        #    "runbooks.md": "...", "known_issues.csv": "..."}
        # Not every value is markdown prose - known_issues is a raw CSV
        # catalog (multiple rows, most of them irrelevant to any given
        # incident). Treat every corpus value as plain text either way.
        ...

Return a dict with exactly these keys:
    "root_cause"          str, non-empty
    "supporting_evidence" list[dict], each {"source": <filename>, "excerpt": <str>}
    "impacted_systems"    list[str]
    "mttr_minutes"        int | None
    "remediation"         str
    "confidence_score"    float, 0-100
    "needs_human_review"  bool - MUST equal (confidence_score < 50)

Nothing is scaffolded here - you're building the full pipeline, both
halves of "RAG":

1. Ingest + retrieve. Turn `corpus` into something you can rank against
   `query` (bag-of-words overlap, TF-IDF, or whatever you choose - pick
   your own vectorization/similarity approach), and produce a relevance
   ranking over the documents. Remember known_issues.csv is row-oriented,
   not prose - decide whether to treat it as one blob or split it into
   per-row candidates.
2. Correlate across documents. A confident conclusion here isn't "the
   top-ranked document says X" - it's "logs, deployment history, known
   issues, the runbook, and a previous incident all point at the same
   thing." Count how many *distinct source types* actually corroborate
   your leading hypothesis.
3. Calibrate confidence_score from that corroboration count, not from how
   relevant the top document felt. A single weak signal with no
   deployment correlation, no known-issue match, and no precedent should
   score low - and reporting a confident-sounding root cause anyway when
   the evidence doesn't support it is worse than correctly saying "I'm
   not sure."
4. Extract mttr_minutes and impacted component names from the retrieved
   text (a runbook's "Typical MTTR: N minutes" line, an architecture
   doc's component name) - simple pattern matching is fine, you don't
   need anything fancier.
"""
from __future__ import annotations


def _ingest_corpus(corpus: dict) -> dict:
    """TODO: normalize/prepare the raw corpus for retrieval.

    e.g. tokenize, lowercase, strip markdown/code-fence noise, split
    known_issues.csv into per-row candidates instead of one big blob -
    whatever representation your retrieval step below needs.
    """
    raise NotImplementedError


def _retrieve_relevant_documents(query: str, corpus: dict) -> list[tuple[str, float]]:
    """TODO: rank corpus entries against `query`.

    Returns [(source, relevance_score), ...] sorted most relevant first.
    `source` should be a corpus filename (or a finer-grained id, e.g.
    "known_issues.csv#KI-101", if you split the CSV into rows).
    """
    raise NotImplementedError


def _correlate_evidence(query: str, corpus: dict, ranked: list[tuple[str, float]]) -> dict:
    """TODO: go beyond the top-ranked hit - find independent sources that
    corroborate (or fail to corroborate) the same hypothesis, and collect
    the excerpts that back it.
    """
    raise NotImplementedError


def _calibrate_confidence(evidence: dict) -> float:
    """TODO: turn corroboration strength (how many distinct source types
    agree) into a 0-100 confidence score. Thin/uncorroborated evidence
    must land below 50.
    """
    raise NotImplementedError


def investigate(query: str, corpus: dict) -> dict:
    # TODO: wire the pieces above together (or restructure entirely -
    # these helpers are just a suggested shape, not a required one):
    #   1. ingest + retrieve relevant documents for `query`
    #   2. correlate evidence across independent sources
    #   3. extract root_cause / impacted_systems / mttr_minutes / remediation
    #   4. calibrate confidence_score and derive needs_human_review from it
    raise NotImplementedError
