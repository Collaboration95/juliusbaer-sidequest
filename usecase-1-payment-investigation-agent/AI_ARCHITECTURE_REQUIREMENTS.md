# AI Architecture Requirements

## Required

### 1. RAG
Implement a policy retrieval pipeline.

At minimum:

```text
documents
   ↓
clean
   ↓
chunk
   ↓
index
   ↓
retrieve
   ↓
evidence + source
```

You may use lexical retrieval, TF-IDF, BM25, embeddings, hybrid retrieval,
reranking, or another local approach.

### 2. Tools
Implement structured tools for:
- payment lookup;
- client lookup;
- client payment history;
- deterministic beneficiary/time-window analysis.

### 3. Agent
Implement an LLM/agent loop that decides which tools it needs and then
synthesizes a grounded answer.

### 4. Deterministic calculations
Use Python/tool logic for:
- amounts;
- thresholds;
- counts;
- aggregation;
- time-window calculations.

Do not rely on the LLM for exact arithmetic.

### 5. Grounding
Important claims must be supported by supplied data or retrieved policy
evidence.

### 6. Uncertainty
If evidence is insufficient, explicitly say what is missing.

## Framework freedom

No particular LLM, agent framework, embedding model, vector database or
provider is required.

The engineering behavior matters more than the framework name.
