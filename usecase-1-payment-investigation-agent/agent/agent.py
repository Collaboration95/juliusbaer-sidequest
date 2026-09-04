"""
AI AGENT — MAIN CANDIDATE WORK AREA

This file contains the tool registry, prompt and method contract, but NO
finished agent implementation.

The expected behavior is an LLM/tool-calling loop.

Recommended flow:

    Question
       ↓
    LLM / Agent
       ↓
    tool call
       ↓
    deterministic result
       ↓
    LLM
       ↓
    more tools if necessary
       ↓
    grounded final answer

LLM integration guidance
------------------------

You need an LLM with tool-calling (function-calling) support.  Install
your provider's SDK (e.g. ``pip install openai``) and load your API key
from ``.env``.

Minimal skeleton (adapt to your chosen provider):

    import os, json
    from openai import OpenAI

    client = OpenAI()  # reads OPENAI_API_KEY from env

    # 1. Define tool schemas for the LLM from the functions above.
    tool_schemas = [
        {
            "type": "function",
            "function": {
                "name": "get_payment",
                "description": "Retrieve a payment by ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {"type": "string"}
                    },
                    "required": ["payment_id"],
                },
            },
        },
        # ... repeat for each tool in TOOLS ...
    ]

    # 2. Call the LLM with the question and tool schemas.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
        messages=messages,
        tools=tool_schemas,
    )

    # 3. If the LLM requests a tool call, execute it and feed the
    #    result back.  Loop until the LLM produces a final answer.
    # 4. Parse the final answer into the required JSON schema.

You may also use an agent framework (LangChain, etc.) if you prefer.
The engineering behavior matters more than the framework name.
"""


from tools.client_tools import get_client_profile
from tools.payment_tools import (
    get_payment,
    get_client_payments,
    aggregate_beneficiary_24h,
)
from tools.policy_tools import search_policy


TOOLS = {
    "get_client_profile": get_client_profile,
    "get_payment": get_payment,
    "get_client_payments": get_client_payments,
    "aggregate_beneficiary_24h": aggregate_beneficiary_24h,
    "search_policy": search_policy,
}


SYSTEM_PROMPT = """
You are a bank payment-investigation assistant.

Rules:
1. Retrieve transaction facts before making factual claims.
2. Use deterministic tools for arithmetic and aggregation.
3. Retrieve applicable policy evidence through RAG.
4. Separate observed facts from assumptions.
5. A policy trigger does not automatically establish suspicious activity.
6. Explain missing evidence when necessary.
7. Cite relevant policy sources.
"""


def run_agent(
    question: str,
    payment_id: str,
) -> dict:
    """
    Implement the complete AI assistant.

    Required output:

    {
        "answer": "...",
        "citations": ["..."],
        "facts": {...},
        "tools_used": [...]
    }

    Recommended implementation steps:

    1. Give the LLM the question and available tool schemas.
    2. Let the model decide what it needs.
    3. Execute the requested tool.
    4. Return tool results to the LLM.
    5. Permit additional tool calls if evidence is incomplete.
    6. Ask for a grounded final response.
    7. Normalize the response to the required JSON schema.

    Do not hard-code Q01-Q10.
    """
    pass
