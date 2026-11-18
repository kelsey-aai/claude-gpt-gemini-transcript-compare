"""Offline check: patch the OpenAI client and confirm compare.run builds the right request."""
import os
import sys
import types
from unittest import mock

os.environ.setdefault("ASSEMBLYAI_API_KEY", "test")
sys.path.insert(0, os.path.dirname(__file__))
import compare  # noqa: E402

calls = []


def fake_create(**kwargs):
    calls.append(kwargs)
    msg = types.SimpleNamespace(content=f"summary from {kwargs['model']}")
    return types.SimpleNamespace(
        choices=[types.SimpleNamespace(message=msg)],
        usage=types.SimpleNamespace(total_tokens=42),
    )


with mock.patch.object(compare.client.chat.completions, "create", side_effect=fake_create):
    for m in compare.MODELS:
        r = compare.run(m, "Speaker A: hello")
        assert r["text"] == f"summary from {m}" and r["tokens"] == 42

assert str(compare.client.base_url).rstrip("/") == "https://llm-gateway.assemblyai.com/v1"
assert [c["model"] for c in calls] == compare.MODELS
assert all(c["extra_body"]["fallbacks"][0]["model"] == compare.FALLBACKS[c["model"]] for c in calls)
assert "hello" in calls[0]["messages"][0]["content"]
print("offline test passed:", len(calls), "requests")
