# Payment Investigation Assistant

## Background

Banks process thousands of payments daily.  Compliance teams must
review payments that trigger policy thresholds, involve high-risk
destinations, or show patterns of potential structuring (splitting large
transfers into smaller ones to avoid detection).

Today this work is manual, time-consuming, and inconsistent.  Your task
is to build an AI assistant that helps investigators by combining
transaction data, client profiles, and policy documents to produce
grounded, traceable recommendations.

## Objective

Build a small AI-powered assistant for a bank's payment operations/compliance
team.

The assistant must answer 10 natural-language payment-investigation
questions by combining:

- structured client data;
- structured payment data;
- policy/procedure documents;
- RAG;
- deterministic tools;
- an LLM/agent orchestration layer.

The 10 questions cover distinct reasoning patterns:

- threshold review (is enhanced review required and why?);
- high-risk destination handling;
- structuring detection (requires payment-history aggregation);
- separating observed facts from assumptions;
- identifying which policy documents to retrieve;
- recommending what additional information to request;
- summarizing the investigation workflow.

## Target architecture

```text
                  Investigation Question
                           |
                           v
                    LLM / AI Agent          <-- LLM: planning, tool selection, synthesis
                           |
           +---------------+---------------+
           |               |               |
           v               v               v
     Client Tool      Payment Tools      Policy RAG
     (deterministic)  (deterministic)    (deterministic)
           |               |               |
           +---------------+---------------+
                           |
                           v
                        Evidence
                           |
                           v
                     LLM synthesis          <-- LLM: interpretation, recommendation
                           |
                           v
                 Grounded recommendation
                     + citations
```

**Deterministic tools** handle all arithmetic, threshold comparisons,
counting, aggregation, and date logic.  **The LLM** handles planning,
tool selection, interpretation, and final synthesis.  Do not rely on the
LLM for exact calculations.

## Example 1 — Threshold review

Question:

> What review requirement applies to P50001 and why?

A strong assistant should:
1. retrieve P50001;
2. identify the client and relevant region;
3. retrieve applicable policy evidence;
4. check destination risk;
5. compare the transaction against deterministic thresholds;
6. produce a grounded recommendation;
7. cite the evidence.

## Example 2 — Structuring detection

Question:

> Does the data show a possible transaction-splitting pattern for C2003?

A strong assistant should:
1. retrieve the client profile for C2003;
2. retrieve C2003's full payment history;
3. aggregate payments to the same beneficiary within a 24-hour window
   using deterministic tool logic;
4. compare the combined total against the structuring threshold;
5. retrieve the policy that defines structuring;
6. distinguish: observed facts (multiple payments, combined total) from
   assumptions (intent to evade);
7. recommend next steps and cite the evidence.

## Critical banking reasoning principle

A policy trigger is **not automatically proof of suspicious activity**.

The assistant should distinguish:

- observed transaction facts;
- policy triggers;
- assumptions;
- missing evidence;
- recommended next action.

Concrete illustration:

> **Observed fact:** P50002 is a USD 85,000 payment to AE (high-risk).
> **Policy trigger:** amount exceeds the Singapore RM-review threshold;
> destination is high-risk.
> **Assumption:** the client may be intentionally routing funds to a
> high-risk jurisdiction.
> **Missing evidence:** purpose of payment, source of funds, client's
> relationship history with the beneficiary.
> **Recommended action:** additional review; request payment purpose
> documentation before release.

## Policy corpus

The corpus intentionally contains:
- global policy;
- regional procedures (Singapore, Switzerland);
- high-risk jurisdiction list;
- investigation procedure;
- decoy administrative notes.

The assistant should retrieve relevant evidence instead of simply reading every
document or using the first search result.

## Key design challenges

These are intentional complexities that mirror real-world payment
investigation.  Read `DATA_NOTES.md` for full details.

1. **Multi-currency thresholds.** Policy thresholds are in USD and CHF.
   Payments use five currencies (USD, CHF, SGD, HKD, GBP).  No
   exchange-rate data is provided.
2. **Data quality.** The `beneficiary_country` and
   `beneficiary_country_code` fields do not always agree.  The code
   field is authoritative for risk assessment.
3. **Regional vs global policy layering.** Singapore and Switzerland
   have regional policies that add requirements on top of the global
   policy.  Other countries use the global policy only.
4. **Structuring detection.** Detecting transaction splitting requires
   aggregating a client's payment history by beneficiary and time
   window — not just looking at a single payment.
5. **Decoy documents.** The policy corpus contains four decoy documents
   with no relevant content.  RAG must filter them out.

## Constraints

- **No hard-coded answers.** Answers must be generated by the assistant,
  not keyed to question IDs.
- **Non-interactive.** The program must run end-to-end via
  `python main.py --questions questions.json --output submission.json`
  with no user input.
- **10 questions.** The program must produce exactly one JSON result per
  question.  See `SUBMISSION_GUIDE.md` for the required output schema.
- **Fresh environment.** The program must run with only
  `pip install -r requirements.txt` plus your chosen LLM SDK.

## 60-minute constraint

Do not build an enterprise platform.

A small, reliable implementation with clear separation between:
RAG → tools → agent → grounded answer
is preferred.
