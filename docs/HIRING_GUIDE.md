# Organizer Guide (for organizers/admins, not participants)

`jb-sidequest` is a 2-use-case Julius Baer AI Hackathon. Use case 1 is an
AI agent challenge (payment investigation assistant requiring an LLM API
key); use case 2 is a retrieval + evidence-correlation problem
(RAG-shaped, deliberately no LLM required to build). Both are evaluated
manually, by a human reading the participant's submitted output against
a private answer key — there is no autoscoring, CI, or integrity-checking
machinery in this repo for either one. This doc covers the parts
participants don't need.

## Evaluation model

| Use case | What you collect | How to score |
|---|---|---|
| 1 — Payment Investigation Agent | Source code + `submission.json` | Run `python main.py --questions questions.json --output submission.json` yourself and evaluate the output against a private answer key (see `EVALUATION_CRITERIA.md`) |
| 2 — Production Incident Investigator | `solution.py`, `answers.json`, `README.md` | Read `answers.json` against a private answer key for both incidents; optionally spot-check by re-running their `solution.py` yourself |

## Use case 1 — evaluation

1. Collect each participant's source code and `submission.json`.
2. Run `python main.py --questions questions/questions.json --output submission.json`
   in a fresh environment with only `pip install -r requirements.txt`
   plus the participant's chosen LLM SDK.
3. Evaluate the output against your private answer key using the rubric
   in `EVALUATION_CRITERIA.md` (answer correctness 40%, grounding/citations
   20%, tool usage 15%, RAG quality 15%, code quality 10%).

Participants need an LLM API key (any provider — see `.env.example`).
Make sure they know to bring their own key.

## Use case 2 — evaluation

Each participant implements `investigate()` in their own copy of
`starter/solution.py`, runs it against both incidents themselves (via
`data/loader.py`'s `load_incident(name)`), and adds
`usecase-2-production-incident-investigator/submissions/<their-name>/`
with `solution.py` + `answers.json` (their `investigate()` output for
both incidents, keyed by incident directory name) + a `README.md`
covering their design, understanding of the problem, and approach.

To evaluate:

1. Read `answers.json` for both `incident_a_pool_exhaustion` and
   `incident_b_ambiguous_delay` against your private answer key. What to
   look for, per that use case's README:
   - Well-formed, internally consistent output (`needs_human_review`
     exactly matches `confidence_score < 50`).
   - Incident A: high confidence, `payment-gateway-adapter` correctly
     named, MTTR close to 20 minutes, evidence from multiple independent
     source documents (not just the single most-relevant one).
   - Incident B: correctly *low* confidence and flagged for review — the
     evidence there is genuinely thin, and a solution that manufactures
     unwarranted confidence should score worse, not better, than one
     that says "not sure."
   - Free-text fields (`root_cause`, `remediation`) judged for substance,
     not exact wording.
   This comparison can be done by a human, or by feeding both
   `answers.json` and your answer key to an LLM as judge — that judging
   logic is intentionally not part of this repo, so you can run it
   however fits your process (a separate script, a one-off prompt,
   whatever).
2. Optionally, spot-check for tampering or a mismatch between claimed and
   actual behavior: re-run their `solution.py` against both incidents
   yourself (same `load_incident()` + `investigate()` call) and diff the
   result against their submitted `answers.json`. There's no automated
   integrity check for this anymore — it's a manual spot-check, use your
   judgment on how often to do it.
3. Read their `README.md` for design reasoning, understanding of the
   problem, and approach/tradeoffs — same as any other written
   submission.

`PERFORMANCE_THRESHOLDS` and automated code-quality checks no longer
exist in this repo; if runtime performance or code style matter to your
process, review them the same way you'd review use case 1's code -
manually, reading the source.

## Collecting submissions

**Use case 2** has its own `submissions/<their-name>/` folder inside
`usecase-2-production-incident-investigator/` — each participant adds
their own folder there with `solution.py`, `answers.json`, and
`README.md` (see that use case's `submissions/README.md`). There's no
PR-based workflow or CI trigger tied to it anymore, just a shared
convention for where the files live — decide how participants actually
get you their folder (a shared fork, a zip, a PR into their own fork
that you pull from, email, whatever fits your process).

**Use case 1** has no equivalent folder — collect source code +
`submission.json` however fits your process, same as above.

Either way, track scores in your own spreadsheet or tracker; nothing
here generates a consolidated report for you anymore.
