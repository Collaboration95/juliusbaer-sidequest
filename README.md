# Julius Baer AI Hackathon — jb-sidequest

## Overview

Two use cases, both manually evaluated. Read each use case's own
`README.md` before starting — full spec, starter code, exact submission
format. Attempt as many as you like; one done well beats two done
halfway.

| # | Directory | Track | LLM required? | How it's scored |
|---|---|---|---|---|
| 1 | [`usecase-1-payment-investigation-agent/`](usecase-1-payment-investigation-agent/) | AI agent: tools + RAG + LLM orchestration | **Yes** — any LLM provider with tool-calling support | Manual evaluation against a private answer key (see `EVALUATION_CRITERIA.md`) |
| 2 | [`usecase-2-production-incident-investigator/`](usecase-2-production-incident-investigator/) | Retrieval + evidence correlation (RAG-shaped, no LLM) | No | Manual evaluation against a private answer key, possibly using an LLM as judge |

**Use case 1** asks you to build a payment-investigation AI assistant
that answers 10 natural-language questions by combining structured data,
policy documents (via RAG), deterministic tools, and an LLM agent. It
requires an LLM API key (any provider — see `.env.example`). The
organizer runs your code and evaluates the output against a private
answer key.

**Use case 2** asks you to build an incident-investigation function that
correlates evidence across a document corpus and produces a structured
report with a calibrated confidence score. No LLM, no API key — it's
purely retrieval + correlation. You run your own code against both
incidents' queries and submit the resulting `answers.json` alongside
your `solution.py`; the organizer judges it against a private answer
key, the same way use case 1 is judged.

---

## Project structure

```
jb-sidequest/
├── README.md                     you are here — participant-facing overview
├── LICENSE
├── requirements.txt                deps for use case 2's solution.py
├── .gitignore
│
├── docs/
│   └── HIRING_GUIDE.md             for organizers/admins, not participants
│
├── usecase-1-payment-investigation-agent/
│   ├── README.md                     the brief + quick start
│   ├── main.py                        entry point (do not modify)
│   ├── requirements.txt               use-case-specific deps (pandas, numpy)
│   ├── .env.example                   LLM configuration template
│   ├── sample_submission.json         example output format
│   ├── PROBLEM_STATEMENT.md           what you are building
│   ├── PARTICIPANT_INSTRUCTIONS.md    your three tasks and schedule
│   ├── DATA_NOTES.md                  important data clarifications
│   ├── AI_ARCHITECTURE_REQUIREMENTS.md  required components
│   ├── EVALUATION_CRITERIA.md         how submissions are scored
│   ├── SUBMISSION_GUIDE.md            required output format
│   ├── ARCHITECTURE_HINTS.md          architecture guidance (optional)
│   ├── WHY_METHODS_ONLY.md            why interfaces are empty
│   ├── QUICKSTART.md                  setup + run guide
│   ├── data/
│   │   ├── clients.csv                50 synthetic clients
│   │   ├── payments.csv               184 synthetic payments
│   │   ├── data_dictionary.csv        field descriptions
│   │   └── policies/                  9 policy docs (5 relevant, 4 decoys)
│   ├── questions/
│   │   └── questions.json             10 evaluation questions
│   ├── tools/                         data-access tools (implement these)
│   │   ├── client_tools.py
│   │   ├── payment_tools.py
│   │   └── policy_tools.py
│   ├── rag/                           RAG pipeline (implement this)
│   │   └── pipeline.py
│   └── agent/                         AI agent (implement this)
│       └── agent.py
│
└── usecase-2-production-incident-investigator/
    ├── README.md                     the brief, spec, and submission format
    ├── data/
    │   ├── incident_a_pool_exhaustion/   7 documents + query.txt (high-confidence scenario)
    │   ├── incident_b_ambiguous_delay/   7 documents + query.txt (low-confidence scenario)
    │   └── loader.py                       loads one incident's query + document corpus
    ├── starter/solution.py           copy this into your own submission folder
    └── submissions/                  your work goes here
        └── <your-name>/
            ├── solution.py
            ├── answers.json
            └── README.md
```

**Use case 1** provides method-only interfaces — function signatures and
contracts with no implementations. You implement the tools, RAG pipeline,
and AI agent, then run `python main.py` to produce `submission.json`.

**Use case 2** gives you `README.md` (the brief) and `starter/solution.py`
(the function you implement); `data/loader.py` is a small helper for
loading each incident's query + corpus, not something you need to
modify. You run your own `investigate()` against both incidents and
produce `answers.json` yourself — there's no test suite or CI in this
repo for either use case; both are evaluated the same way, by a human
(and possibly an LLM-as-judge review) reading your submitted output
against a private answer key.

---

## Getting started

### Use case 1 — Payment Investigation Agent

```bash
cd usecase-1-payment-investigation-agent
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your LLM API key
# Install your chosen LLM SDK, e.g.: pip install openai

python main.py --questions questions/questions.json --output submission.json
```

**Don't have an LLM API key handy?** [open-free-llm-api/awesome-freellm-apis](https://github.com/open-free-llm-api/awesome-freellm-apis)
is a community-maintained directory of free-tier LLM APIs across many
providers (rate limits, context windows, and setup snippets included) —
useful if you want to attempt use case 1 without signing up for a paid
plan first.

Follow the reading order in `PARTICIPANT_INSTRUCTIONS.md` → "Before you
start". Key documents: `PROBLEM_STATEMENT.md`, `DATA_NOTES.md`,
`AI_ARCHITECTURE_REQUIREMENTS.md`, `EVALUATION_CRITERIA.md`,
`SUBMISSION_GUIDE.md`.

### Use case 2 — Production Incident Investigator

```bash
pip install -r requirements.txt
cd usecase-2-production-incident-investigator
mkdir -p submissions/<your-name>
cp starter/solution.py submissions/<your-name>/solution.py

# implement investigate() in submissions/<your-name>/solution.py, then
# run it against both incidents yourself and save the output as
# submissions/<your-name>/answers.json, e.g.:
python -c "
from data.loader import load_incident
import json, sys
sys.path.insert(0, 'submissions/<your-name>')
import solution
answers = {}
for name in ['incident_a_pool_exhaustion', 'incident_b_ambiguous_delay']:
    query, corpus = load_incident(name)
    answers[name] = solution.investigate(query, corpus)
with open('submissions/<your-name>/answers.json', 'w') as f:
    json.dump(answers, f, indent=2)
"
```

---

## Submission requirements

### Use case 1

Run the official command and submit the resulting `submission.json` along
with your source code:

```bash
python main.py --questions questions/questions.json --output submission.json
```

Your output must contain exactly 10 JSON objects (one per question), each
with the required fields: `question_id`, `payment_id`, `answer`,
`citations`, `facts`, `tools_used`. See `SUBMISSION_GUIDE.md` for the
full schema and `sample_submission.json` for a worked example.

### Use case 2

Create `usecase-2-production-incident-investigator/submissions/<your-name>/`
with three files: `solution.py`, the `answers.json` it produced for both
incidents (see that use case's README, "What you submit"), and a
`README.md` covering, in your own words:

- **Design** — how your solution is structured and why
- **Your understanding of the problem** — what the actual difficulty
  was, in your assessment
- **Why you took the approach you did** — including anything you tried
  and abandoned, and tradeoffs made under the time limit
- **Your name, phone number, and email**

This `README.md` is graded alongside the rest and it's what a reviewer
reads first.

**Both use cases are evaluated manually, by a human reading your
submission against a private answer key** — there's no automated
scoring or CI in this repo for either one.

---

## Using AI assistants well

You're welcome to use AI tools here — that's realistic, not a shortcut.
It's genuinely useful for explaining a concept you're rusty on, reviewing
a solution once you've already spotted a specific concern, and handling
boilerplate. What it won't reliably do: a fluent, obvious-looking first
draft from an assistant tends to look plausible and fail somewhere that
actually matters — read each use case's README carefully and check your
own output against the actual source material (the incident corpus, for
use case 2) before trusting a first pass.

---

Good luck!
