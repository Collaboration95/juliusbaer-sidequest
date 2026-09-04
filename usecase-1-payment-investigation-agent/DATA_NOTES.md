# Data Notes

Read this before working with the data files.  It clarifies several
intentional design choices that may otherwise cause confusion.

## Currency handling

Policy thresholds are expressed in different currencies:

| Policy source              | Threshold currency |
|----------------------------|--------------------|
| Global payment policy      | USD                |
| Singapore procedure        | USD                |
| Switzerland procedure      | CHF                |

Payments in `payments.csv` use five currencies: USD, CHF, SGD, HKD, GBP.

**For this 60-minute challenge, no exchange-rate data is provided.**

You have two acceptable options:

1. **Compare in native currency when a matching regional policy exists.**
   For example, a CHF payment from a Switzerland-region client is
   compared against the CHF thresholds in `regional_switzerland.md`.

2. **Treat "equivalent" as 1:1 for non-matching currencies** and state
   this assumption explicitly in your answer.

Do not spend time fetching live exchange rates.  The evaluation
questions are designed so that the correct answer does not depend on
precise currency conversion.

## beneficiary_country vs beneficiary_country_code

The `payments.csv` file contains two related columns:

| Field                      | Example     | Description                          |
|----------------------------|-------------|--------------------------------------|
| `beneficiary_country`      | UAE         | Human-readable country name          |
| `beneficiary_country_code` | AE          | Synthetic ISO-style code             |

**These two fields do not always agree.**  This is intentional — it
simulates real-world data quality issues.

**Use `beneficiary_country_code` for jurisdiction risk assessment.**
The `high_risk_jurisdictions.md` policy references codes (e.g., "AE"),
not country names.

Example: P50002 has `beneficiary_country = Hong Kong` but
`beneficiary_country_code = AE`.  The code `AE` is the authoritative
field for the high-risk check.

## Payment dates

`payment_date` is a calendar date in `YYYY-MM-DD` format.

**No time component is provided.**  When implementing the 24-hour
aggregation window (`aggregate_beneficiary_24h`), treat payments on the
same calendar date as being within the same 24-hour window.  State this
assumption if it affects your answer.

### 24h aggregation filtering

The `aggregate_beneficiary_24h` tool must filter by **both**
`client_id` **and** `beneficiary_name`.  The dataset contains payments
to the same beneficiary on the same date from different clients, and
payments from the same client on the same date to different
beneficiaries.  A correct implementation includes only payments matching
both the specified client and the specified beneficiary in the result.

## Policy corpus

The `data/policies/` directory contains:

| File                          | Relevance                           |
|-------------------------------|-------------------------------------|
| `global_payment_policy.md`    | Global thresholds and rules         |
| `regional_singapore.md`       | Singapore-specific thresholds       |
| `regional_switzerland.md`     | Switzerland-specific thresholds     |
| `high_risk_jurisdictions.md`  | High-risk destination list          |
| `investigation_procedure.md`  | Step-by-step investigation workflow |
| `decoy_operational_1-4.md`    | Decoys — contain no relevant policy |

A strong RAG implementation retrieves the relevant documents and
filters out the decoys.

## Client region mapping

A client's region is determined by the `country` field in
`clients.csv`.  The regional policy that applies is based on this
country:

| Client country   | Regional policy               |
|------------------|-------------------------------|
| Singapore        | `regional_singapore.md`       |
| Switzerland      | `regional_switzerland.md`     |
| Other countries  | `global_payment_policy.md` only |

The global policy always applies; regional policies add additional
requirements on top of it.
