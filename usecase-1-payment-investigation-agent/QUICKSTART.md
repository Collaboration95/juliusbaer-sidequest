# Quick Start

## Prerequisites

- Python 3.10 or later
- An LLM API key (any provider — see `.env.example`)

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your LLM
cp .env.example .env
# Edit .env and add your API key and model name

# 4. If your LLM provider requires a Python SDK, install it
#    e.g. pip install openai   OR   pip install anthropic
```

## Understand the problem

Follow the reading order in `PARTICIPANT_INSTRUCTIONS.md` → "Before you
start".  The key documents are:

- `PROBLEM_STATEMENT.md` — what you are building
- `DATA_NOTES.md` — data clarifications (read this before coding)
- `AI_ARCHITECTURE_REQUIREMENTS.md` — required components
- `EVALUATION_CRITERIA.md` — how you are scored
- `SUBMISSION_GUIDE.md` — required output format

Inspect the data:
```text
data/clients.csv          — 50 synthetic clients
data/payments.csv         — 184 synthetic payments
data/policies/            — 9 policy documents (5 relevant, 4 decoys)
data/data_dictionary.csv  — field descriptions
questions/questions.json  — 10 evaluation questions
```

## Implement

```text
tools/client_tools.py     — client data access
tools/payment_tools.py    — payment lookup + deterministic analysis
tools/policy_tools.py     — policy retrieval (connects to RAG)
rag/pipeline.py           — document loading, chunking, indexing, retrieval
agent/agent.py            — LLM/tool-calling agent loop
```

## Run

```bash
python main.py --questions questions.json --output submission.json
```

Your program must run without interactive input and produce one result for each
question.

## Verify before submitting

- The output file contains exactly 10 JSON objects (one per question).
- Each object has all required fields: `question_id`, `payment_id`,
  `answer`, `citations`, `facts`, `tools_used`.
- No answer is hard-coded to a `question_id`.
- The program runs in a fresh environment with only `pip install -r
  requirements.txt` plus your chosen LLM SDK.
