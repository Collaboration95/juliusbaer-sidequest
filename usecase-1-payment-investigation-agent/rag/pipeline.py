"""
RAG PIPELINE — METHOD-ONLY STARTER

No retrieval implementation is supplied intentionally.

You are expected to implement the pipeline within the one-hour challenge.

Minimum conceptual pipeline:

    policy files
        ↓
    load documents
        ↓
    clean text
        ↓
    chunk
        ↓
    build index
        ↓
    retrieve
        ↓
    optional rerank
        ↓
    evidence + source

A simple TF-IDF/keyword solution is acceptable.

An embedding/hybrid solution is welcome, but do not sacrifice reliability for
complexity.
"""


def load_policy_documents(policy_directory: str) -> list[dict]:
    """
    Load policy documents from the supplied directory.

    Each returned document should preserve:
        - source filename;
        - text;
        - optional metadata.
    """
    pass


def clean_document(text: str) -> str:
    """
    Normalize policy text before chunking.

    Preserve policy wording and headings that may be important for retrieval
    and citations.
    """
    pass


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[dict]:
    """
    Split policy documents into retrieval chunks.

    Each chunk should preserve its source.

    Suggested structure:

    {
        "chunk_id": "...",
        "source": "global_payment_policy.md",
        "text": "...",
        "metadata": {}
    }

    Avoid splitting a single policy rule across unrelated chunks.
    """
    pass


def build_index(chunks: list[dict]):
    """
    Build a reusable retrieval index.

    Possible approaches:
        - keyword/TF-IDF;
        - BM25;
        - embeddings;
        - local vector database;
        - hybrid retrieval.

    The return value is implementation-defined.
    """
    pass


def retrieve(
    index,
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Retrieve the most relevant policy chunks.

    Results must preserve the source document name.
    """
    pass


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """
    OPTIONAL: rerank retrieved candidates.

    A simple implementation may return the candidates unchanged.
    """
    pass


def retrieve_policy_evidence(
    index,
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Convenience method for the policy tool.

    Suggested implementation:

        candidates = retrieve(index, query, top_k=10)
        return rerank(query, candidates, top_k=top_k)
    """
    pass
