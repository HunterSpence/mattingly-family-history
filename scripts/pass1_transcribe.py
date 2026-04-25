"""Pass 1 transcription — Deepgram Nova-3 on Grandma Shari interview.

Minimal keyterm seed (Shari, Spence, Ellis Island, Castle Garden).
Output: transcripts/pass1.json (raw response) + pass1.txt (readable).
"""
import json
import os
import sys
from pathlib import Path

from deepgram import DeepgramClient

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
AUDIO = WORKSPACE / "audio" / "source.m4a"
OUT_JSON = WORKSPACE / "transcripts" / "pass1.json"
OUT_TXT = WORKSPACE / "transcripts" / "pass1.txt"

SEED_KEYTERMS = [
    "Shari",
    "Spence",
    "Ellis Island",
    "Castle Garden",
]


def format_ts(seconds: float) -> str:
    s = int(seconds or 0)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h:d}:{m:02d}:{sec:02d}" if h else f"{m:d}:{sec:02d}"


def main():
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        print("ERROR: DEEPGRAM_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if not AUDIO.exists():
        print(f"ERROR: audio not found: {AUDIO}", file=sys.stderr)
        sys.exit(1)

    size_mb = AUDIO.stat().st_size / 1024 / 1024
    print(f"Loading {AUDIO.name} ({size_mb:.1f} MB)...")
    audio_bytes = AUDIO.read_bytes()

    client = DeepgramClient(api_key=api_key)

    print("Submitting to Deepgram Nova-3 (Pass 1)...")
    print(f"  model=nova-3 lang=en diarize=True smart_format=True")
    print(f"  keyterm seed: {SEED_KEYTERMS}")

    response = client.listen.v1.media.transcribe_file(
        request=audio_bytes,
        model="nova-3",
        language="en",
        keyterm=SEED_KEYTERMS,
        diarize=True,
        paragraphs=True,
        punctuate=True,
        smart_format=True,
        utterances=True,
        detect_entities=True,
        filler_words=False,
    )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(response, "model_dump_json"):
        OUT_JSON.write_text(response.model_dump_json(indent=2), encoding="utf-8")
    elif hasattr(response, "model_dump"):
        OUT_JSON.write_text(
            json.dumps(response.model_dump(), indent=2, default=str), encoding="utf-8"
        )
    else:
        OUT_JSON.write_text(json.dumps(response, indent=2, default=str), encoding="utf-8")
    print(f"Saved JSON: {OUT_JSON} ({OUT_JSON.stat().st_size:,} bytes)")

    transcript_lines = []
    try:
        results = response.results
        utterances = getattr(results, "utterances", None) or []
        if utterances:
            current_speaker = None
            buf = []
            for utt in utterances:
                spk = getattr(utt, "speaker", None)
                txt = getattr(utt, "transcript", "") or ""
                start = getattr(utt, "start", 0.0) or 0.0
                if spk != current_speaker:
                    if buf:
                        transcript_lines.append(" ".join(buf))
                        buf = []
                    current_speaker = spk
                    transcript_lines.append(f"\n[{format_ts(start)}] Speaker {spk}:")
                buf.append(txt)
            if buf:
                transcript_lines.append(" ".join(buf))
        else:
            channels = getattr(results, "channels", []) or []
            for ch in channels:
                alts = getattr(ch, "alternatives", []) or []
                for alt in alts:
                    paragraphs_obj = getattr(alt, "paragraphs", None)
                    if paragraphs_obj:
                        paras = getattr(paragraphs_obj, "paragraphs", []) or []
                        for p in paras:
                            spk = getattr(p, "speaker", None)
                            start = getattr(p, "start", 0.0) or 0.0
                            sentences = getattr(p, "sentences", []) or []
                            text = " ".join(
                                (getattr(s, "text", "") or "") for s in sentences
                            )
                            transcript_lines.append(
                                f"\n[{format_ts(start)}] Speaker {spk}: {text}"
                            )
                    else:
                        transcript_lines.append(getattr(alt, "transcript", "") or "")
    except Exception as e:
        print(f"WARN: extraction failed, dumping fallback: {e}")
        transcript_lines.append(str(response))

    OUT_TXT.write_text("\n".join(transcript_lines).strip(), encoding="utf-8")
    print(f"Saved text: {OUT_TXT} ({OUT_TXT.stat().st_size:,} bytes)")

    text = OUT_TXT.read_text(encoding="utf-8")
    print()
    print("=== PREVIEW (first 1500 chars) ===")
    print(text[:1500])
    print(f"\n=== Total transcript: {len(text):,} chars ===")


if __name__ == "__main__":
    main()
