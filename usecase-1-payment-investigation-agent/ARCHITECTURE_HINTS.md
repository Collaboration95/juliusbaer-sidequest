# Architecture Hints

A good one-hour architecture is:

```text
                     Question
                        |
                        v
                    LLM Agent
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
       Payment        Client       Policy RAG
        Tools          Tool           |
          |             |             |
          +-------------+-------------+
                        |
                     Evidence
                        |
                        v
                  LLM synthesis
                        |
                        v
                Answer + citations
```

Use deterministic code for arithmetic and aggregation.
Use the LLM for interpretation, planning, tool selection and synthesis.
