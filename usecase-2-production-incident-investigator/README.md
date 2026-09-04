# 🔎 Use Case 2 — Production Incident Investigator

**Track**: Retrieval + evidence correlation (RAG-shaped, no LLM required)
**Estimated time**: ~1 hour
**No banking/domain knowledge needed** beyond reading application logs. **No API keys, no GPU, no LLM calls** — see "A note on what 'RAG' means here" below.

---

## 📋 The brief

You're an on-call engineer's investigation assistant. You're given a
corpus of documents for one production incident — application logs, an
architecture overview, API specs, deployment history, previous incidents,
runbooks, and a known-issues catalog — plus a plain-English question
describing the symptom. Your job is to correlate evidence *across* those
documents and produce a structured incident report: probable root cause,
supporting evidence, impacted systems, mean time to recover, recommended
remediation, and a calibrated confidence score.

Not every document is markdown prose: `known_issues.csv` is a flat CSV
catalog with one row per known issue (`issue_id,title,signature,
affected_component,notes`) — several rows, most of them irrelevant to any
given incident, same as a real issue tracker export would look. Your
retrieval/correlation has to work over raw text regardless of which
file it came from, not assume everything is a markdown document.

There are **two incidents** in `data/`, and they're deliberately
different in kind:

- **`incident_a_pool_exhaustion/`** — "Payments are intermittently
  failing after yesterday's deployment...". The evidence is there, spread
  across five different documents, and a correct investigation finds all
  of it.
- **`incident_b_ambiguous_delay/`** — "Order confirmation emails are
  arriving late...". The evidence is genuinely thin: one unconfirmed
  warning, no matching known issue, no correlated deployment, no
  precedent. **The correct answer is low confidence, not a confident
  guess.**

### Exact spec

Implement:

```python
def investigate(query: str, corpus: dict) -> dict:
    """corpus: filename -> full document text (all the files in one
    incident's data/ folder)."""
```

Return a dict with exactly these keys:

- **`root_cause`** — non-empty string, even for the low-confidence incident
- **`supporting_evidence`** — `list[dict]`, each `{"source": <filename>, "excerpt": <str>}`
- **`impacted_systems`** — `list[str]`
- **`mttr_minutes`** — `int | None`
- **`remediation`** — string
- **`confidence_score`** — `float`, 0-100
- **`needs_human_review`** — `bool`, must equal `confidence_score < 50` exactly

No exact wording is required. Free-text fields are judged for substance
against a private answer key, not exact phrasing.

### What you submit

There's no live code execution during grading. Instead, **you run your
own `investigate()`** against both incidents' queries and commit the
output to your own folder under `submissions/<your-name>/`:

1. For each incident directory in `data/` (`incident_a_pool_exhaustion`,
   `incident_b_ambiguous_delay`), load its query and corpus — e.g. via
   `data/loader.py`'s `load_incident(name)` — and call your `investigate()`.
2. Write both reports to a single `answers.json` in
   `submissions/<your-name>/`, keyed by incident directory name:

   ```json
   {
     "incident_a_pool_exhaustion": { "root_cause": "...", "supporting_evidence": [...], "...": "..." },
     "incident_b_ambiguous_delay": { "root_cause": "...", "supporting_evidence": [...], "...": "..." }
   }
   ```

   Each value is exactly the dict your `investigate()` returned for that
   incident — same keys, same shape, as the spec above.

How you produce it is up to you (a short throwaway script, a REPL
session, whatever) — it isn't graded, only `solution.py` and the
resulting `answers.json` are.

---

## 🧠 A note on what "RAG" means here

A real production version of this tool would hand retrieved evidence to
an LLM to write the narrative. That needs an API key, and this use case
deliberately doesn't require one to *build* — you're building the two
halves that make the retrieval/correlation itself real:

1. **Retrieval** — rank the corpus against the query yourself (TF-IDF
   cosine similarity, plain bag-of-words overlap, whatever approach you
   choose — that's genuinely representative of how retrieval works, just
   without a vector database behind it). The starter leaves this as a
   stub; ingestion and ranking are part of what's graded, not given.
2. **Structured correlation and confidence calibration** — the actual
   graded difficulty. Do independent sources agree with each other, and
   does your confidence score honestly reflect that?

If you want to wire in a real LLM in your own `investigate()` to turn
your structured report into better prose, go ahead — it's your code,
run on your machine, to produce `answers.json`; nothing about how you
got there is graded, only the JSON you submit and the `solution.py` that
produced it. (Separately, the organizer's own review of your submitted
`answers.json` against the private answer key may itself use an LLM as
judge — that's not part of this repo and has nothing to do with whether
you use one.)

---

## 🧠 Why this is harder than it looks

- **Retrieval alone isn't the answer.** The top-ranked document for
  incident A's query might just be the architecture overview (it
  literally contains the word "payment" the most). The actual root cause
  only becomes clear when you notice that *logs*, *deployment history*,
  *known issues*, *the runbook*, and *a previous incident* are all
  independently telling you the same thing.
- **Not every log line is about this incident.** Both logs files carry a
  handful of entries from other, unrelated known issues (checkout
  latency, search indexing, email templating, and so on) alongside the
  ones that actually matter — real logs are not pre-filtered to just the
  incident you're investigating, and neither is this one.
- **Calibration, not confidence theater.** It's easy to always emit a
  plausible-sounding root cause with a high confidence number attached —
  that's what a fluent AI assistant will hand you if you don't push back.
  It's much harder to build something that correctly recognizes when the
  evidence is actually too thin, and says so.
- **The two incidents use the same document *types* on purpose.** If your
  approach only works for incident A because you hardcoded something
  specific to it (a filename, a magic string), it'll misbehave on
  incident B — your submitted `answers.json` is judged on both.

---

## 🎯 What you're building

In `submissions/<your-name>/` (create this folder yourself — see
[`submissions/README.md`](submissions/README.md)):

```
usecase-2-production-incident-investigator/
└── submissions/
    └── <your-name>/
        ├── solution.py
        ├── answers.json
        └── README.md
```

- **`solution.py`** — your `investigate()`. Copy `starter/solution.py` in
  as your starting point; it lays out a suggested function structure
  (ingest, retrieve, correlate, calibrate) but every step is a stub —
  retrieval included — for you to implement.
- **`answers.json`** — your `investigate()`'s output for both incidents,
  produced by running your own `solution.py` against each incident's
  `query.txt` + corpus (see "What you submit" above for the exact shape).
  This is what gets judged against the private answer key — not a live
  run of your code.
- **`README.md`** — see the root [README.md](../README.md)'s "Submission
  requirements" for what this needs to contain.

---

## ✅ How this is graded

**Everything here is judged manually** — there's no test suite or CI in
this repo. The organizer reads your submitted `answers.json` against a
private answer key for both incidents, looking for the same qualities a
trusted test suite would otherwise check:

- Well-formed and internally consistent output — `needs_human_review`
  exactly matches `confidence_score < 50`.
- Incident A: high confidence, `payment-gateway-adapter` correctly
  named, an MTTR close to 20 minutes, and evidence drawn from multiple
  independent source documents (not just the single most-relevant one).
- Incident B: correctly *low*, flagged confidence — manufacturing
  unwarranted confidence here should score worse, not better, than
  honestly saying "not sure."
- Free-text fields (`root_cause`, `remediation`) judged for substance,
  not exact phrasing.

Your `solution.py` itself (design, clarity, whether it'd hold up as real
code) and your `README.md`'s design write-up factor into the same manual
review. That review may itself use an LLM as a judge on the organizer's
side; how they run that comparison isn't part of this repo — only the
submission format (`answers.json`) is.

## 💡 Using Claude (or any AI assistant) here

Useful for: explaining TF-IDF/cosine similarity if retrieval is new to
you, reviewing whether your evidence-correlation logic actually checks
independent sources or just restates the top search hit, brainstorming
what "confidence" should mean here before you write the formula. Less
useful for: an assistant asked to "investigate this incident" with no
further steering will very readily produce a confident-sounding answer
for incident B too, regardless of how thin the evidence actually is —
check your own output against both incidents before you trust it.
