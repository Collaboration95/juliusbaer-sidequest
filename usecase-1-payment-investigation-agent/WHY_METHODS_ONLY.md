# Why Are the Methods Empty?

This is intentional.

We want to evaluate whether you can implement the engineering layers behind an
AI assistant, rather than only wiring an LLM to pre-built tools.

For example, you receive:

```python
def get_payment(payment_id: str) -> dict:
    """Retrieve a payment."""
    pass
```

You implement the lookup.

Likewise, RAG exposes:

```python
def retrieve(index, query, top_k=5):
    """Retrieve relevant policy chunks."""
    pass
```

You implement retrieval.

This provides enough guidance to avoid wasting time on interface design while
still testing actual coding ability.
