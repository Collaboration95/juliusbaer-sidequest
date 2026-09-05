# Deterministic incident investigator

Participant details: fill in name, phone number, and email before submitting.

## Understanding of the problem

The challenge is not simply to find a document containing the words from the
query. The useful answer is distributed across logs, architecture, deployment
history, the known-issues CSV, runbooks, and historical incidents. The
investigator must correlate those sources and calibrate confidence according to
how independently they agree.

Incident A has a strong causal chain: timeout errors in the payment path begin
after a deployment that reduces the adapter pool from 50 to 10; the issue
catalog, runbook, architecture, API contract, and prior incident all support
the same explanation. Incident B deliberately has weaker evidence: emails are
queued and eventually sent after a long delay, but the corpus cannot distinguish
queue consumer saturation from third-party provider latency. Its correct result
is a low-confidence report requiring human review.

## Design

`solution.py` first ingests every markdown document as chunks and splits the
CSV catalog into row-level candidates. It ranks candidates with a small TF-IDF
cosine scorer, preserving source filenames. Correlation then looks for shared
operational signatures across independent source types, extracts compact
excerpts, and records explicit negative evidence such as “no correlated
deployment” or “unverified.” MTTR is extracted only when the relevant runbook
supports it; the ambiguous incident returns `null` rather than borrowing an
unrelated 15-minute estimate.

The confidence formula rewards independent corroboration and penalizes explicit
uncertainty. `needs_human_review` is derived directly from the resulting score,
so the two fields cannot drift apart.

## Tradeoffs

This is intentionally a standard-library solution that can run in the supplied
environment without an API key or vector database. The domain signatures are
interpreted from the retrieved corpus rather than keyed to incident directory
names or question IDs. A production version could replace the lexical ranker
with embeddings and add metrics/log parsers, but the evidence and calibration
contracts would remain the same.
