"""Run the same transcript prompt through Claude Opus 5.5, GPT-6 Astra and Gemini 4 Argon
on AssemblyAI's LLM Gateway, and print each answer with its response time and token usage."""
import os
import sys
import time

from openai import OpenAI

MODELS = ["claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"]

# A runner-up per model, so a provider error doesn't stop the comparison.
FALLBACKS = {
    "claude-opus-5-5": "claude-sonnet-5-5",
    "gpt-6-astra": "gpt-6.1-sol",
    "gemini-4-argon": "gemini-3.8-flash",
}

PROMPT = (
    "Summarize this call in 5 bullet points, then list every action item "
    "with its owner.\n\nTranscript:\n{transcript}"
)

client = OpenAI(
    base_url="https://llm-gateway.assemblyai.com/v1",
    api_key=os.environ["ASSEMBLYAI_API_KEY"],
)


def run(model: str, transcript: str) -> dict:
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT.format(transcript=transcript)}],
        max_tokens=1500,
        # LLM Gateway field, not part of the OpenAI schema, so it goes in extra_body
        extra_body={"fallbacks": [{"model": FALLBACKS[model]}]},
    )
    return {
        "model": model,
        "seconds": round(time.perf_counter() - start, 2),
        "tokens": response.usage.total_tokens if response.usage else None,
        "text": response.choices[0].message.content,
    }


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        transcript = f.read()
    for model in MODELS:
        result = run(model, transcript)
        print(f"=== {result['model']}  {result['seconds']}s  {result['tokens']} tokens")
        print(result["text"], "\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample_transcript.txt")
