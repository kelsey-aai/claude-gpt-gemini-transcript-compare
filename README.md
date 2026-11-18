# Claude vs GPT vs Gemini on transcripts

Send the same transcript prompt to Claude Opus 5.5, GPT-6 Astra and Gemini 4 Argon through
AssemblyAI's LLM Gateway, and compare the answers, response times and token usage side by side.

Companion code for the AssemblyAI blog post "Claude Opus 5.5 vs GPT-6 Astra vs Gemini 4 Argon".

## Setup

1. Get an AssemblyAI API key: https://www.assemblyai.com/dashboard/signup
2. `cp .env.example .env` and export the key: `export ASSEMBLYAI_API_KEY=...`

## Python

```bash
pip install -r requirements.txt
python compare.py sample_transcript.txt
```

## Node.js

```bash
npm install
node compare.mjs sample_transcript.txt
```

## curl

```bash
./compare.sh
```

## Notes

- All three models use one base URL (`https://llm-gateway.assemblyai.com/v1`) and one API key.
  Only the `model` string changes.
- Each request sets a fallback model (`fallbacks`), so a provider error retries on the runner-up.
- `gpt-6-astra` is served from the US endpoint only. For EU data residency use
  `https://llm-gateway.eu.assemblyai.com/v1`, which serves Claude and Gemini models.
- Benchmark numbers for these models come from Voice Standard Bench
  (https://github.com/AssemblyAI/voice-standard-bench). Test on your own transcripts before you pick one.
