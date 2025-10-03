- Build a PromptManager (`prompt_manager.py`)
  - Stateful: Store prompt inside it.

- Add more LLMs:
  - Close-source: OpenAI
    - Reasoning
    - Tool decision
  - Open-source: Transformers HG
    - Embedding and similarity search
    - Classification/intent detection

- Add routers:
  - Top level router
  - Domain-specific router (inside top level router)