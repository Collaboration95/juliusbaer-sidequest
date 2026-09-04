# Tools

The tools layer provides deterministic data access.  The AI agent should
call these methods rather than reading CSV files directly.

## Required tools

### `client_tools.py`

| Method                   | Description                                      |
|--------------------------|--------------------------------------------------|
| `get_client_profile(id)` | Return one client's profile from `clients.csv`.  |
| `get_clients_by_country` | _(optional)_ Return clients for a given country. |

### `payment_tools.py`

| Method                          | Description                                              |
|---------------------------------|----------------------------------------------------------|
| `get_payment(id)`               | Return one payment record from `payments.csv`.           |
| `get_client_payments(id)`       | Return all payments for a client (payment history).      |
| `aggregate_beneficiary_24h`     | Aggregate same-beneficiary payments within 24h window.   |
| `find_repeated_beneficiaries`   | _(optional)_ Find beneficiaries appearing multiple times.|

### `policy_tools.py`

| Method                   | Description                                           |
|--------------------------|-------------------------------------------------------|
| `search_policy(query)`   | Retrieve relevant policy evidence via RAG.            |
| `get_policy_document`    | _(optional)_ Retrieve a full policy document by name. |

## Implementation notes

- Read CSV files with `pandas` (already in `requirements.txt`).
- Return plain `dict` / `list[dict]` — no custom classes needed.
- Handle missing IDs gracefully (return empty dict or clear error).
- All arithmetic, counting, and date logic must be in these tools, not
  in the LLM.
- `search_policy` should delegate to `rag/pipeline.py`.
