# Participant Instructions — 60 Minutes

## What are you building?

An AI investigation assistant, not a dashboard and not a simple rule engine.

## Before you start

Read these documents in this order:

1. `PROBLEM_STATEMENT.md` — objective, architecture, and challenges
2. `PARTICIPANT_INSTRUCTIONS.md` — this file (your three tasks and schedule)
3. `DATA_NOTES.md` — important data clarifications (currency, country codes, dates)
4. `AI_ARCHITECTURE_REQUIREMENTS.md` — required components
5. `EVALUATION_CRITERIA.md` — how you will be scored
6. `SUBMISSION_GUIDE.md` — required output format

`ARCHITECTURE_HINTS.md` and `WHY_METHODS_ONLY.md` are short optional
reads for additional context.

## What is provided?

### Data
- `data/clients.csv`
- `data/payments.csv`
- `data/data_dictionary.csv`
- See `DATA_NOTES.md` for important clarifications about the data

### Knowledge base
- `data/policies/*.md` (9 documents: 5 relevant, 4 decoys)

### Evaluation questions
- `questions/questions.json`

### Interfaces
- `tools/*.py`
- `rag/pipeline.py`
- `agent/agent.py`

The interfaces contain method signatures and detailed contracts, but **no
implementations**.

You may add helper functions, create new files, or adjust function
signatures as needed.  The provided signatures are a starting point, not
a constraint.  Do not modify `main.py` — it must remain the entry point.

## Your three coding tasks

### Task 1 — Implement tools

Implement the methods in:
- `tools/client_tools.py`
- `tools/payment_tools.py`
- `tools/policy_tools.py`

### Task 2 — Implement RAG

Implement the methods in:
- `rag/pipeline.py`

A simple lexical/TF-IDF RAG is completely acceptable for one hour.

### Task 3 — Implement the AI agent

Implement:
- `agent/agent.py`

The agent should:
1. receive the question;
2. decide which tools it needs;
3. call tools;
4. retrieve policy evidence;
5. optionally make additional tool calls;
6. synthesize the final answer;
7. return the required JSON structure.

## Suggested schedule

### 0–10 min
Understand the data and policy documents. Read `DATA_NOTES.md` for
important clarifications about currency, country codes, and dates.

### 10–20 min
Implement core data tools.

### 20–35 min
Implement basic RAG.

### 35–50 min
Implement LLM/tool-calling agent.

### 50–57 min
Test all 10 questions.

### 57–60 min
Verify submission command and output.

## What not to spend time on

Do not spend the entire challenge building:
- UI;
- multi-agent systems;
- authentication;
- deployment;
- production databases;
- elaborate vector infrastructure.

## Strong solution

```text
Question
   ↓
Agent
   ├── get_payment
   ├── get_client_profile
   ├── payment-history tool
   └── search_policy
          ↓
       Evidence
          ↓
    grounded answer
```

## Weak solution

```text
Question
   ↓
LLM
   ↓
guessed answer
```

or:

```python
if question_id == "Q01":
    return "..."
```

Hard-coded answers are not acceptable.
