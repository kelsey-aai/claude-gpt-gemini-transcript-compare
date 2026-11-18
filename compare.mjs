// Same comparison in Node.js with the OpenAI SDK: npm install openai
import { readFile } from "node:fs/promises";
import OpenAI from "openai";

const MODELS = ["claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"];
const FALLBACKS = {
  "claude-opus-5-5": "claude-sonnet-5-5",
  "gpt-6-astra": "gpt-6.1-sol",
  "gemini-4-argon": "gemini-3.8-flash",
};

const client = new OpenAI({
  baseURL: "https://llm-gateway.assemblyai.com/v1",
  apiKey: process.env.ASSEMBLYAI_API_KEY,
});

const transcript = await readFile(process.argv[2] ?? "sample_transcript.txt", "utf8");
const prompt =
  "Summarize this call in 5 bullet points, then list every action item " +
  `with its owner.\n\nTranscript:\n${transcript}`;

for (const model of MODELS) {
  const start = performance.now();
  const response = await client.chat.completions.create({
    model,
    messages: [{ role: "user", content: prompt }],
    max_tokens: 1500,
    fallbacks: [{ model: FALLBACKS[model] }], // LLM Gateway field, passed through in the body
  });
  const seconds = ((performance.now() - start) / 1000).toFixed(2);
  console.log(`=== ${model}  ${seconds}s  ${response.usage?.total_tokens} tokens`);
  console.log(response.choices[0].message.content, "\n");
}
