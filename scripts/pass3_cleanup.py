"""Pass 3 — Claude Haiku 4.5 cleanup of Pass 2 transcript.

Tasks:
- Replace Speaker 0 with Shari (Grandma) and Speaker 1 with Hunter
- Fix obvious transcription errors (e.g., "3435" -> "1934 or '35")
- Mark uncertain proper nouns with [?]
- Preserve all timestamps and grandma's verbatim phrasing
- Output transcripts/final.md with header

Cost: ~$0.05 (8k input + 8k output tokens to Haiku 4.5)
"""
import os
import sys
from pathlib import Path

from anthropic import Anthropic

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
INPUT = WORKSPACE / "transcripts" / "pass2.txt"
OUTPUT = WORKSPACE / "transcripts" / "final.md"

SYSTEM_PROMPT = """You are cleaning up a verbatim audio transcript of a family history interview.

The transcript is from Deepgram Nova-3 with diarization. Speaker 0 is the grandmother, named Shari, telling her family history. Speaker 1 is her grandson Hunter, the interviewer.

Your job:
1. Replace "Speaker 0:" with "**Shari:**" and "Speaker 1:" with "**Hunter:**"
2. Fix obvious transcription artifacts where the model misjoined or split numbers/dates. For example "1934. '35" became "3435" — restore to "1934 or '35". Don't change anything else.
3. Where a word looks like a likely proper-noun mistranscription that you cannot resolve confidently, mark it like this: `Beringa[?]` — leaving the original token followed by [?]. Use this sparingly — only for words clearly suspicious. Do NOT mark common words.
4. Preserve EVERY word grandma said. Do not summarize, paraphrase, or remove filler ("Mhmm", "you know", repeated words). This is a verbatim record.
5. Preserve every timestamp in [H:MM:SS] or [MM:SS] format exactly as given.
6. Output the result as Markdown. Each speaker turn starts on its own paragraph.

Add a header at the top:

# Grandma Shari — Family History Interview

**Date:** Recorded 2026-04-25 (timestamps from start of recording)
**Speakers:** Shari (grandmother, age 79) and Hunter (grandson, interviewer)
**Source:** Grandma Shari Family History.m4a (46:11)
**Transcript:** Deepgram Nova-3 two-pass + Claude Haiku 4.5 cleanup

---

Then output the cleaned transcript.

Do NOT add commentary, footnotes, or research. Just clean the transcript."""


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if not INPUT.exists():
        print(f"ERROR: input not found: {INPUT}", file=sys.stderr)
        sys.exit(1)

    transcript = INPUT.read_text(encoding="utf-8")
    print(f"Loaded {INPUT.name} ({len(transcript):,} chars)")

    client = Anthropic(api_key=api_key)

    print("Calling Claude Haiku 4.5 for cleanup...")
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Here is the raw Pass 2 transcript. Clean it up per the system instructions:\n\n---\n\n{transcript}",
            }
        ],
    )

    cleaned = response.content[0].text

    OUTPUT.write_text(cleaned, encoding="utf-8")
    print(f"Saved: {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
    print()
    print("=== Token usage ===")
    print(f"  input:  {response.usage.input_tokens:,}")
    print(f"  output: {response.usage.output_tokens:,}")

    # Compute cost (Haiku 4.5: $1/MTok input, $5/MTok output as of 2025/2026)
    cost = (response.usage.input_tokens / 1_000_000) * 1.0 + (
        response.usage.output_tokens / 1_000_000
    ) * 5.0
    print(f"  cost:   ${cost:.4f}")
    print()
    print("=== PREVIEW (first 1500 chars) ===")
    print(cleaned[:1500])


if __name__ == "__main__":
    main()
