"""Phase 3 — Entity extraction from final transcript.

Uses Claude Sonnet 4.6 (better than Haiku for nuanced extraction with relationship reasoning).
Outputs research/entities.json with structured records for every person, place,
event, occupation, organization, and historical reference mentioned.

Cost: ~$0.15 (10k in + 6k out @ Sonnet rates).
"""
import json
import os
import sys
from pathlib import Path

from anthropic import Anthropic

WORKSPACE = Path(r"C:\Users\hspen\.openclaw\workspace\family-history")
INPUT = WORKSPACE / "transcripts" / "final.md"
OUTPUT = WORKSPACE / "research" / "entities.json"

SYSTEM_PROMPT = r"""You are a forensic genealogy entity extractor. You read a family-history interview transcript and extract every named entity into a structured JSON object that will drive parallel research subagents.

Output a single JSON object matching this exact schema (no markdown, no commentary, JUST the JSON):

{
  "interview_metadata": {
    "subject": "Shari",
    "interviewer": "Hunter (grandson)",
    "date_recorded": "2026-04-25",
    "duration": "46:11",
    "subject_current_age": 79,
    "subject_current_location": "Santa Monica, CA"
  },
  "people": [
    {
      "id": "p001",
      "full_name": "<best name>",
      "given_name": "...",
      "middle_name": "...",
      "surname": "...",
      "maiden_name": null,
      "alternate_spellings": [],
      "relation_to_shari": "<grandfather | great-grandmother | uncle | etc>",
      "birth_year": <int or null>,
      "death_year": <int or null>,
      "birth_place": "<or null>",
      "death_place": "<or null>",
      "occupation": "<or null>",
      "context": "<one-sentence summary of what Shari said about them>",
      "transcript_timestamps": ["0:00", "..."],
      "living_flag": <true if could plausibly be alive — Hunter, David, Charmaine, Stephanie etc>,
      "fuzzy": <true if name spelling is uncertain>,
      "research_priority": "<high | medium | low>",
      "research_targets": ["FamilySearch", "Ancestry", "FindAGrave", "Wikipedia", "Newspapers.com", ...]
    }
  ],
  "places": [
    {
      "id": "pl001",
      "name": "<as Shari said it>",
      "type": "<town | county | state | country | building | street | region>",
      "modern_name": "<if it's changed or unclear>",
      "country": "<US, England, etc>",
      "context": "<why Shari mentioned it>",
      "transcript_timestamps": ["..."],
      "fuzzy": <bool>,
      "research_targets": ["Wikidata", "GeoNames", "Wikipedia", ...]
    }
  ],
  "events": [
    {
      "id": "e001",
      "description": "<what happened>",
      "date_or_year": "<best date>",
      "place": "<where>",
      "people_involved": ["p001", "p002"],
      "context": "<Shari's framing>",
      "transcript_timestamps": ["..."]
    }
  ],
  "ships_and_voyages": [
    {
      "id": "s001",
      "ship_name_or_voyage": "...",
      "year": <int>,
      "from_port": "...",
      "to_port": "...",
      "passengers": ["p001"],
      "context": "...",
      "transcript_timestamps": ["..."]
    }
  ],
  "organizations": [
    {
      "id": "o001",
      "name": "<H-E-B, Stauffer Chemicals, Frost Bank, etc>",
      "type": "<company | university | bank | brand | church | etc>",
      "context": "...",
      "people_connected": ["p001"],
      "transcript_timestamps": ["..."]
    }
  ],
  "historical_references": [
    {
      "id": "hr001",
      "subject": "<Mark Twain, Sherman, Cromwell, Spindletop, etc>",
      "type": "<person | event | concept>",
      "shari_claim": "<what Shari said about it / the family connection>",
      "verifiable": <bool>,
      "transcript_timestamps": ["..."]
    }
  ],
  "open_questions": [
    "<list of uncertain transcription items, garbled passages, or claims needing verification>"
  ]
}

RULES:
- Extract EVERY named person, even if Shari only mentions them once (cousins, in-laws, friends).
- For unnamed referents (e.g. "my mother's brother who ran Frost Bank"), create an entity with full_name=null and given_name=null but include all other context.
- For people who could plausibly still be living (Hunter, David, Charmaine, Stephanie, Shari's living siblings), set living_flag=true. These will be redacted from any shareable output.
- For ambiguous transcription items where you marked [?] or where the spelling is uncertain (e.g., "Beringa tribe" — possibly mistranscribed Anglo-Saxon tribe name; "Ignatius" — first word, unclear if person/place; the garbled house number spelling), add to open_questions.
- For Shari herself, give her id "p000" and include all biographical context she revealed (royalty owner, council president, etc).
- Use unique IDs prefixed by entity type: p001, p002 (people), pl001 (places), e001 (events), s001 (ships), o001 (organizations), hr001 (historical refs).
- Cross-reference: in events, list the person IDs involved. In organizations, list connected people IDs.
- Be exhaustive but don't invent — if Shari didn't mention a date, leave it null. Don't guess.

Output ONLY the JSON object. No prose."""


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    transcript = INPUT.read_text(encoding="utf-8")
    print(f"Loaded {INPUT.name} ({len(transcript):,} chars)")

    client = Anthropic(api_key=api_key)

    print("Calling Claude Sonnet 4.6 for entity extraction (streaming)...")
    chunks = []
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=32000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Extract all entities from this family history interview transcript:\n\n{transcript}",
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            chunks.append(text)
        response = stream.get_final_message()

    raw = "".join(chunks).strip()

    if raw.startswith("```"):
        lines = raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.with_suffix(".raw.txt").write_text(raw, encoding="utf-8")
        print(f"WARN: invalid JSON, raw saved to {OUTPUT.with_suffix('.raw.txt')}")
        print(f"JSON error: {e}")
        sys.exit(2)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
    print()
    print("=== Token usage ===")
    print(f"  input:  {response.usage.input_tokens:,}")
    print(f"  output: {response.usage.output_tokens:,}")
    cost = (response.usage.input_tokens / 1_000_000) * 3.0 + (
        response.usage.output_tokens / 1_000_000
    ) * 15.0
    print(f"  cost:   ${cost:.4f}")
    print()
    print("=== Entity counts ===")
    for k in ["people", "places", "events", "ships_and_voyages", "organizations", "historical_references", "open_questions"]:
        v = data.get(k, [])
        print(f"  {k}: {len(v)}")

    print()
    print("=== People (first 5) ===")
    for p in data.get("people", [])[:5]:
        nm = p.get("full_name") or "(unnamed)"
        rel = p.get("relation_to_shari", "")
        b = p.get("birth_year")
        d = p.get("death_year")
        years = f" ({b}–{d})" if b or d else ""
        flag = " [LIVING]" if p.get("living_flag") else ""
        fuzzy = " [FUZZY]" if p.get("fuzzy") else ""
        print(f"  {p.get('id')}: {nm}{years} — {rel}{flag}{fuzzy}")


if __name__ == "__main__":
    main()
