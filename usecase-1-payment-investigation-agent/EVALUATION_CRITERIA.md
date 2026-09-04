# Evaluation Criteria

## How submissions are scored

The organizer runs:

```bash
python main.py --questions questions.json --output submission.json
```

and evaluates the resulting `submission.json` against a private answer key.

## Scoring dimensions

### 1. Answer correctness (40%)

Each of the 10 questions has an expected answer.  The evaluator checks
whether the participant's `answer` field contains the key facts and
recommendations:

- Correct threshold identification (amount, currency, region).
- Correct high-risk jurisdiction flag.
- Correct structuring determination (present / absent / inconclusive).
- Correct separation of facts vs assumptions.
- Correct recommended next action.

Partial credit is awarded per question for partially correct answers.

### 2. Grounding and citations (20%)

- Every important claim must be backed by retrieved evidence or
  structured data.
- The `citations` list must name the policy documents that support the
  answer.
- The `facts` object must contain the deterministic values (amount,
  currency, country code, etc.) that justify the conclusion.
- Answers that cite irrelevant or decoy documents receive lower scores.

### 3. Tool usage (15%)

- The `tools_used` list must reflect the tools actually invoked.
- A strong solution uses the right tools for the right question:
  - `get_payment` for payment facts;
  - `get_client_profile` for client/region context;
  - `get_client_payments` / `aggregate_beneficiary_24h` for structuring;
  - `search_policy` for policy evidence.
- Calling every tool for every question is not penalised but is not
  rewarded either.

### 4. RAG quality (15%)

- The retrieval pipeline must return relevant policy chunks, not decoy
  documents.
- Source filenames must be preserved so citations are traceable.
- Retrieval that returns the first document or every document
  regardless of query receives a low score.

### 5. Code quality and architecture (10%)

- Clean separation: tools → RAG → agent → answer.
- Deterministic logic in tools, not in the LLM.
- No hard-coded answers (`if question_id == "Q01": ...`).
- Code is readable and would run in a fresh environment.

## Disqualifiers

- Hard-coded answers keyed to `question_id`.
- Output that does not match the required JSON schema.
- Program that requires interactive input.
- Program that crashes on any of the 10 official questions.

## Weighting summary

| Dimension                | Weight |
|--------------------------|--------|
| Answer correctness       | 40%    |
| Grounding and citations  | 20%    |
| Tool usage               | 15%    |
| RAG quality              | 15%    |
| Code quality             | 10%    |
| **Total**                | 100%   |
