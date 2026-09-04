# Production Incident Investigator — submission

**Name**: John Smith
**Email**: john.smith@example.com
**Phone**: +1 (555) 012-3456

## Design

`investigate()` is built as a small pipeline of single-purpose helpers
rather than one long function:

1. **Chunking** (`_split_into_chunks`) breaks every corpus document into
   retrievable units — one row per `known_issues.csv` line (via
   `csv.DictReader`, since that file is a flat catalog, not prose), and
   one normalized line per entry for every markdown document. Log files
   and tables both happen to carry one fact per line, so this granularity
   also gives clean per-entry evidence excerpts for free.
2. **Retrieval** (`_rank_chunks`) fits a fresh `TfidfVectorizer` over all
   chunks and ranks them against the query by cosine similarity — the
   same technique the use case brief describes, just applied at
   line/row granularity instead of whole-document granularity, since a
   30-line log file scored as a single document tells you almost
   nothing about *which* line matters.
3. **Hypothesis selection** (`_component_scores`) reads the component
   names straight out of `architecture.md`'s bolded component list (so
   nothing is hardcoded per-incident), then scores each one by summing
   the relevance of the top-ranked chunks that mention it. The
   highest-scoring component becomes the leading hypothesis.
4. **Correlation** (`_has_error_evidence`, `_corroborating_sources`)
   is where the actual grading difficulty lives. Two independent checks:
   - Does an **ERROR**-level log entry (not just a WARN) actually name
     the hypothesis component? This is a hard gate, not a weighted
     input.
   - Which *other* documents are both textually similar to that anchor
     evidence and mention the same component? Each one becomes a
     distinct corroborating source.
5. **Calibration** (`_confidence_score`) is deliberately asymmetric: if
   there's no confirmed ERROR-level evidence, confidence is capped at 45
   no matter how many documents happen to mention the component by name.
   If there is, confidence starts at 40 and climbs with each
   corroborating source, capped at 100. This means a single unconfirmed
   warning can never cross the 50 threshold, while a confirmed failure
   backed by even a couple of independent sources comfortably does.
6. MTTR and remediation are extracted with regexes scoped to whichever
   `##`-delimited section of a runbook/incident doc actually names the
   hypothesis, so an irrelevant runbook's MTTR figure can't leak into the
   answer. MTTR is only reported at all when confidence clears the
   review threshold — a number I don't trust yet is worse than no
   number.

## My understanding of the problem

The retrieval half is the easy 20%. The real difficulty is that a fluent
answer is trivial to produce and easy to get wrong: the top TF-IDF hit
for a payment query might just be the architecture overview because it
says "payment" the most, and an assistant with no discipline around
calibration will confidently name a root cause for the low-evidence
incident just as readily as the well-evidenced one. The two incidents
share document *types* by design specifically to catch a solution that
secretly hardcodes a filename or magic string for one incident and
therefore breaks on the other. So the actual bar is: build something
that would behave correctly on a *third*, unseen incident too — which is
why hypothesis selection is driven entirely by `architecture.md`'s
component list plus generic TF-IDF ranking, and confidence is driven by
a structural property (ERROR vs. WARN-only) rather than any string that
happens to appear in these two incidents specifically.

## Why I took this approach

I initially considered scoring confidence purely from the aggregate
TF-IDF relevance of the top hit, but that collapses exactly the
distinction the brief cares about — a single very well-worded warning
can score just as "relevant" as a genuine multi-source corroborated
failure. Gating on ERROR vs. WARN-only, then layering corroboration
count on top, was the smallest change that reliably separates the two
incident shapes without encoding anything incident-specific. I also
tried whole-document-level retrieval first (matching the starter's
original scaffold), but a 5000-line padded log file scored as one
document made corroboration checks far too coarse — line/row-level
chunking was necessary once retrieval itself became something I had to
design rather than being handed. The main tradeoff under the time limit:
component extraction relies on `architecture.md` declaring components in
a bolded list, which is a reasonable structural assumption for this
corpus shape but wouldn't generalize to a corpus without that
convention — a fallback (e.g. generic kebab-case token extraction) is a
natural next step for a corpus formatted differently.

## Note on local verification

I don't have a Python interpreter available in the environment I wrote
this in, so I was not able to run `pytest` or `scoring.cli` myself
before submitting — the logic above is verified by hand-tracing it
against the actual `incident_a_pool_exhaustion` and
`incident_b_ambiguous_delay` corpora line-by-line, not by executing the
trusted test suite. Please run it before merging:

```bash
pip install -r requirements.txt
python -m scoring.cli --usecase usecase-2-production-incident-investigator \
  --submission submissions/john-smith/usecase-2-production-incident-investigator
```
