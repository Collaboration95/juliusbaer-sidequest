"""Production incident investigator: retrieves relevant evidence from an
incident's document corpus, correlates it across independent sources, and
produces a confidence-calibrated report. See ../../README.md for the
full brief.

Design in one paragraph: every document is split into small retrievable
units (CSV rows for known_issues.csv, individual lines for everything
else), TF-IDF/cosine similarity ranks those units against the query, and
the highest-scoring architecture component mentioned near the top of that
ranking becomes the leading hypothesis. Confidence is not derived from how
relevant the top hit felt - it is gated on whether an actual ERROR-level
log entry backs the hypothesis (a warning alone is capped well below the
human-review threshold, no matter how many documents happen to mention the
same component name) and then scaled by how many independent document
types corroborate it.
"""
from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_COMPONENT_RE = re.compile(r"\*\*([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\*\*")
_MTTR_RE = re.compile(r"MTTR\*{0,2}:?\s*(\d+)\s*minutes?", re.IGNORECASE)
_REMEDIATION_RE = re.compile(r"\*\*Remediation\*\*:\s*(.+?)(?:\n\s*\n|\Z)", re.DOTALL)
_NON_ALNUM_RE = re.compile(r"[^a-zA-Z0-9]")

_TOP_N_FOR_HYPOTHESIS = 25
_CORROBORATION_THRESHOLD = 0.12
_IMPACTED_SYSTEM_RATIO = 0.3


@dataclass
class Chunk:
    """One retrievable unit of evidence: a line, or a known_issues.csv row."""
    source: str
    text: str


def investigate(query: str, corpus: dict) -> dict:
    """Correlate evidence across `corpus` for `query` and return a
    structured incident report (see module docstring for the approach).
    """
    chunks = _split_into_chunks(corpus)
    ranked = _rank_chunks(query, chunks)
    components = _known_components(corpus)
    scores = _component_scores(ranked, components)
    hypothesis = max(scores, key=scores.get) if scores else None

    if hypothesis is None:
        return _no_evidence_report()

    anchor = _anchor_chunk(ranked, hypothesis)
    has_error_evidence = _has_error_evidence(chunks, hypothesis)
    corroborating = _corroborating_sources(corpus, anchor.text, hypothesis)
    cited_sources = corroborating | {anchor.source}

    confidence = _confidence_score(has_error_evidence, len(corroborating))
    needs_review = confidence < 50

    return {
        "root_cause": _summarize_root_cause(hypothesis, anchor, len(corroborating), has_error_evidence),
        "supporting_evidence": _collect_supporting_evidence(ranked, hypothesis, cited_sources),
        "impacted_systems": _impacted_systems(scores, hypothesis),
        "mttr_minutes": None if needs_review else _extract_mttr(corpus, hypothesis),
        "remediation": _extract_remediation(corpus, hypothesis) or _fallback_remediation(hypothesis),
        "confidence_score": confidence,
        "needs_human_review": needs_review,
    }


def _split_into_chunks(corpus: dict) -> list[Chunk]:
    """Break every document into retrievable units."""
    chunks: list[Chunk] = []
    for source, text in corpus.items():
        if source.endswith(".csv"):
            chunks.extend(_csv_row_chunks(source, text))
        else:
            chunks.extend(_line_chunks(source, text))
    return chunks


def _csv_row_chunks(source: str, text: str) -> list[Chunk]:
    reader = csv.DictReader(io.StringIO(text))
    return [Chunk(source, ", ".join(f"{k}: {v}" for k, v in row.items())) for row in reader]


def _line_chunks(source: str, text: str) -> list[Chunk]:
    chunks = []
    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("#-*").strip().strip("`|").strip()
        if len(_NON_ALNUM_RE.sub("", line)) < 3:
            continue
        chunks.append(Chunk(source, line))
    return chunks


def _rank_chunks(query: str, chunks: list[Chunk]) -> list[tuple[Chunk, float]]:
    """Rank every chunk against `query` with TF-IDF cosine similarity."""
    texts = [c.text for c in chunks]
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        chunk_vectors = vectorizer.fit_transform(texts)
        query_vector = vectorizer.transform([query])
        scores = cosine_similarity(query_vector, chunk_vectors)[0]
    except ValueError:
        scores = [0.0] * len(chunks)
    return sorted(zip(chunks, scores), key=lambda pair: -pair[1])


def _known_components(corpus: dict) -> list[str]:
    """Component identifiers declared in architecture.md's bolded list."""
    text = corpus.get("architecture.md", "")
    return list(dict.fromkeys(_COMPONENT_RE.findall(text)))


def _component_scores(ranked: list[tuple[Chunk, float]], components: list[str]) -> dict[str, float]:
    """Aggregate relevance score per component, from the top-ranked chunks."""
    scores: dict[str, float] = {}
    for chunk, score in ranked[:_TOP_N_FOR_HYPOTHESIS]:
        lowered = chunk.text.lower()
        for component in components:
            if component in lowered:
                scores[component] = scores.get(component, 0.0) + score
    return scores


def _anchor_chunk(ranked: list[tuple[Chunk, float]], hypothesis: str) -> Chunk:
    """The single highest-ranked chunk that actually mentions the hypothesis."""
    for chunk, _ in ranked:
        if hypothesis in chunk.text.lower():
            return chunk
    return ranked[0][0]


def _has_error_evidence(chunks: list[Chunk], hypothesis: str) -> bool:
    """True only if an ERROR-level entry (not just a WARN) names the hypothesis."""
    return any(hypothesis in c.text.lower() and "ERROR" in c.text for c in chunks)


def _corroborating_sources(corpus: dict, anchor_text: str, hypothesis: str) -> set[str]:
    """Other documents whose overall content both mentions the hypothesis and
    is textually similar to the anchor evidence - i.e. actually about the
    same thing, not just a passing mention of the component name."""
    sources = list(corpus)
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        doc_vectors = vectorizer.fit_transform(corpus[s] for s in sources)
        anchor_vector = vectorizer.transform([anchor_text])
        scores = cosine_similarity(anchor_vector, doc_vectors)[0]
    except ValueError:
        return set()
    return {
        source for source, score in zip(sources, scores)
        if score >= _CORROBORATION_THRESHOLD and hypothesis in corpus[source].lower()
    }


def _confidence_score(has_error_evidence: bool, n_corroborating: int) -> float:
    """Confirmed error evidence unlocks the high-confidence band; a warning
    alone is capped below the human-review threshold regardless of how many
    documents superficially mention the same component."""
    if has_error_evidence:
        return min(100.0, 40.0 + 12.0 * n_corroborating)
    return min(45.0, 10.0 + 8.0 * n_corroborating)


def _impacted_systems(scores: dict[str, float], hypothesis: str) -> list[str]:
    if not scores:
        return [hypothesis]
    best = scores[hypothesis]
    return sorted(c for c, s in scores.items() if s >= _IMPACTED_SYSTEM_RATIO * best)


def _collect_supporting_evidence(ranked: list[tuple[Chunk, float]], hypothesis: str, sources: set[str]) -> list[dict]:
    evidence, seen = [], set()
    for chunk, _ in ranked:
        if chunk.source not in sources or chunk.source in seen:
            continue
        if hypothesis not in chunk.text.lower():
            continue
        evidence.append({"source": chunk.source, "excerpt": chunk.text})
        seen.add(chunk.source)
    return evidence


def _extract_mttr(corpus: dict, hypothesis: str) -> int | None:
    """Typical MTTR from whichever runbook/incident section names the hypothesis."""
    for text in corpus.values():
        for block in text.split("##"):
            if hypothesis in block.lower():
                match = _MTTR_RE.search(block)
                if match:
                    return int(match.group(1))
    return None


def _extract_remediation(corpus: dict, hypothesis: str) -> str | None:
    for text in corpus.values():
        for block in text.split("##"):
            if hypothesis in block.lower():
                match = _REMEDIATION_RE.search(block)
                if match:
                    return " ".join(match.group(1).split())
    return None


def _fallback_remediation(hypothesis: str) -> str:
    return f"No documented remediation found for {hypothesis}; escalate for manual investigation."


def _summarize_root_cause(hypothesis: str, anchor: Chunk, n_corroborating: int, has_error_evidence: bool) -> str:
    confirmed = "a confirmed error" if has_error_evidence else "only an unconfirmed warning"
    strength = (
        f"corroborated by {n_corroborating} independent source(s)"
        if n_corroborating else "not corroborated by any other independent source"
    )
    return (
        f"Evidence points to {hypothesis} as the probable root cause. The strongest "
        f"signal is {confirmed} in {anchor.source}: \"{anchor.text}\" - {strength}."
    )


def _no_evidence_report() -> dict:
    return {
        "root_cause": "No component in the corpus could be confidently linked to this query.",
        "supporting_evidence": [],
        "impacted_systems": [],
        "mttr_minutes": None,
        "remediation": "Escalate for manual investigation; retrieval found no relevant evidence.",
        "confidence_score": 0.0,
        "needs_human_review": True,
    }
