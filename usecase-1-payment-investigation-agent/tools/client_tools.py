"""
Client data-access tool interfaces.

These methods intentionally contain NO implementations.

The candidate must implement the data lookup using the supplied
``data/clients.csv`` file.

The AI agent should interact with these methods rather than directly reading
the CSV. This creates a clean separation between:
    - AI orchestration;
    - deterministic data access;
    - final answer generation.
"""


def get_client_profile(client_id: str) -> dict:
    """
    Retrieve one client's profile.

    Parameters
    ----------
    client_id:
        Example: ``"C2001"``.

    Returns
    -------
    dict
        Client information including country, risk rating, client type and
        relationship duration.

    Implementation requirement
    --------------------------
    Return a structured result for known clients and handle unknown IDs
    gracefully.
    """
    pass


def get_clients_by_country(country: str) -> list[dict]:
    """
    OPTIONAL: Retrieve clients associated with a given country.

    Parameters
    ----------
    country:
        Country name.

    Returns
    -------
    list[dict]
        Matching client records.
    """
    pass
