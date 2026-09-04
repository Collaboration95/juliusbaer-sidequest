"""
Payment and deterministic analysis tool interfaces.

These methods intentionally contain NO implementations.

Exact calculations should happen in these tools, not in the LLM.
"""


def get_payment(payment_id: str) -> dict:
    """
    Retrieve one payment by payment ID.

    The implementation should read from ``data/payments.csv``.

    Returns a structured payment record or a clear empty/error result when
    the payment does not exist.
    """
    pass


def get_client_payments(client_id: str) -> list[dict]:
    """
    Retrieve the supplied payment history for a client.

    Useful for transaction-pattern and structuring questions.
    """
    pass


def aggregate_beneficiary_24h(
    client_id: str,
    beneficiary_name: str,
) -> dict:
    """
    Aggregate payments to a beneficiary within a 24-hour window.

    This should be deterministic Python/business logic.

    Suggested result:

    {
        "count": 3,
        "total_amount": 140000,
        "payments": [...]
    }

    Consider:
    - date/time parsing;
    - true 24-hour windows;
    - missing values;
    - currency handling;
    - preserving payment IDs.
    """
    pass


def find_repeated_beneficiaries(client_id: str) -> list[dict]:
    """
    OPTIONAL: Identify beneficiaries appearing multiple times in the
    client's payment history.

    Useful for potential structuring analysis.
    """
    pass
