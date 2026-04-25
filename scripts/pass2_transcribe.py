"""Pass 2 high-fidelity transcription with expanded keyterm list.

Keyterms harvested from Pass 1 review:
- Family surnames (Mattingly, Heichtmuller/Teichmuller, Pohl, Baity)
- Given names (Monette, Mamie, Mata, Charmaine, Leroy, Gigi)
- Texas places (San Antonio, Kerrville, Reeves County, Wolfcamp, Spindletop, Galveston)
- English places (Cambridge, Mattingley, Boonesborough, Mattingly's Hope)
- Historical figures (Mark Twain, Sherman, Daniel Boone, Lord Baltimore, Cromwell)
- Brands (H-E-B, Stauffer Chemicals, Frost Bank, Mattingly & Moore)
- Genealogical (Domesday, Norman, R1b, Euskara, Baringa, DAR)
- Anthropology (Denisovan, Neanderthal, Homo erectus, Australopithecus)
"""
import json
import os
import sys
from pathlib import Path

from deepgram import DeepgramClient

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
AUDIO = WORKSPACE / "audio" / "source.m4a"
OUT_JSON = WORKSPACE / "transcripts" / "pass2.json"
OUT_TXT = WORKSPACE / "transcripts" / "pass2.txt"

EXPANDED_KEYTERMS = [
    "Shari",
    "Spence",
    "Mattingly",
    "Mattingley",
    "Madigan",
    "Heichtmuller",
    "Teichmuller",
    "Hans Teichmuller",
    "Pohl",
    "Hugo Pohl",
    "Baity",
    "Beatty",
    "Pearl Baity",
    "Charmaine",
    "Monette",
    "Mamie",
    "Gigi",
    "Mata",
    "Leroy",
    "Claude",
    "Stephanie",
    "David",
    "Zay",
    "Ignatius",
    "San Antonio",
    "Castile",
    "Kerrville",
    "Reeves County",
    "Wolfcamp",
    "Wolfcamp Shale",
    "Spindletop",
    "Galveston",
    "Boonesborough",
    "Boonsboro",
    "Mattingly's Hope",
    "Cambridge",
    "Oxford",
    "Maryland",
    "North Carolina",
    "Houston",
    "Santa Monica",
    "Iberian Peninsula",
    "Pyrenees",
    "Basque",
    "Iberia",
    "Mark Twain",
    "Sherman",
    "Daniel Boone",
    "Lord Baltimore",
    "Cromwell",
    "Oliver Cromwell",
    "King James",
    "Herbert E. Butt",
    "Judson",
    "Kaiser",
    "Lucy",
    "H-E-B",
    "HEB",
    "Mattingly and Moore",
    "Stauffer Chemicals",
    "Frost Bank",
    "Texas A&M",
    "Student Union",
    "Domesday Book",
    "Domesday",
    "Norman invasion",
    "Revolutionary War",
    "DAR",
    "R1b",
    "Haplogroup",
    "Euskara",
    "Indo-European",
    "Baringa",
    "Beringa",
    "Beorma",
    "Mitochondrial Eve",
    "Denisovan",
    "Neanderthal",
    "Homo erectus",
    "Australopithecus",
    "World's Fair",
    "Meet Me in St. Louis",
    "Latter-day Saints",
    "Church of Jesus Christ of Latter-day Saints",
    "Genealogical Library",
    "St. Louis",
    "Kentucky",
    "Texas",
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

    print(f"Submitting to Deepgram Nova-3 (Pass 2) with {len(EXPANDED_KEYTERMS)} keyterms...")

    response = client.listen.v1.media.transcribe_file(
        request=audio_bytes,
        model="nova-3",
        language="en",
        keyterm=EXPANDED_KEYTERMS,
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
    except Exception as e:
        print(f"WARN: extraction failed: {e}")

    OUT_TXT.write_text("\n".join(transcript_lines).strip(), encoding="utf-8")
    print(f"Saved text: {OUT_TXT} ({OUT_TXT.stat().st_size:,} bytes)")

    text = OUT_TXT.read_text(encoding="utf-8")
    print(f"\n=== Pass 2 transcript: {len(text):,} chars ===")
    print("\n=== PREVIEW (first 1500 chars) ===")
    print(text[:1500])


if __name__ == "__main__":
    main()
