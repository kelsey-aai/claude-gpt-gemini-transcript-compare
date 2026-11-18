#!/usr/bin/env bash
# One request with curl. Swap the model string to compare: claude-opus-5-5, gpt-6-astra, gemini-4-argon
curl -s https://llm-gateway.assemblyai.com/v1/chat/completions \
  -H "Authorization: $ASSEMBLYAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-5-5",
    "messages": [{"role": "user", "content": "Summarize this call in 5 bullet points:\n\nAgent: Thanks for calling. Customer: My invoice is wrong..."}],
    "max_tokens": 1500,
    "fallbacks": [{"model": "claude-sonnet-5-5"}]
  }'
