"""compactor.py — Hierarchical association pruner.

Scores associations by confidence * recency * relevance.
Drops bottom 30%, merges duplicates, archives the rest.
Writes condensed index for respawning across context limits.

Usage:
  python3 compactor.py <associations.json> [--threshold 8000]
"""

import json, sys, math, pathlib
from datetime import datetime, timezone
from typing import Any


THRESHOLD_TOKENS = 8000
ARCHIVE_DIR = pathlib.Path.home() / ".config" / "opencode" / "memory"


def score(assoc: dict, now: float) -> float:
    conf = assoc.get("confidence", 0.5)
    # recency: weight decays for older stamps
    stamp = assoc.get("provenance", {}).get("stamp", "")
    try:
        age_hours = (now - datetime.fromisoformat(stamp).timestamp()) / 3600
        recency = math.exp(-age_hours / 24)  # half-life ~24h
    except Exception:
        recency = 0.5
    # relevance: more trigger/resolve links = more relevant
    relevance = 1.0 + 0.1 * (len(assoc.get("triggers", [])) + len(assoc.get("resolves", [])))
    return conf * recency * relevance


def merge(a: dict, b: dict) -> dict:
    """Merge two associations, keeping the higher-confidence source."""
    if a.get("confidence", 0) >= b.get("confidence", 0):
        kept, dropped = a, b
    else:
        kept, dropped = b, a
    kept["tags"] = list(set(kept.get("tags", []) + dropped.get("tags", [])))
    kept["triggers"] = list(set(kept.get("triggers", []) + dropped.get("triggers", [])))
    kept["resolves"] = list(set(kept.get("resolves", []) + dropped.get("resolves", [])))
    kept["_merged_from"] = kept.get("_merged_from", []) + [dropped.get("id")]
    return kept


def compact(associations: list[dict], threshold: int = THRESHOLD_TOKENS) -> dict:
    now = datetime.now(timezone.utc).timestamp()
    total_in = len(associations)

    # 1. Deduplicate by concept name (merge)
    by_concept: dict[str, dict] = {}
    for a in associations:
        c = a.get("concept", "")
        if c in by_concept:
            by_concept[c] = merge(by_concept[c], a)
        else:
            by_concept[c] = a

    merged = list(by_concept.values())

    # 2. Score and sort
    for a in merged:
        a["_score"] = score(a, now)
    merged.sort(key=lambda x: x["_score"], reverse=True)

    # 3. Drop bottom 30%
    keep_count = max(1, int(len(merged) * 0.7))
    kept = merged[:keep_count]
    archived = merged[keep_count:]

    # 4. Write condensed index
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    condensed = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_before_compact": total_in,
        "after_dedup": len(merged),
        "kept": keep_count,
        "archived": len(archived),
        "associations": [
            {k: v for k, v in a.items() if not k.startswith("_")}
            for a in kept
        ],
    }
    cond_path = ARCHIVE_DIR / "condensed-index.json"
    cond_path.write_text(json.dumps(condensed, indent=2))

    archive_path = ARCHIVE_DIR / "archived-associations.jsonl"
    with open(archive_path, "a") as f:
        for a in archived:
            clean = {k: v for k, v in a.items() if not k.startswith("_")}
            f.write(json.dumps(clean) + "\n")

    return {
        "total_in": total_in,
        "after_dedup": len(merged),
        "kept": keep_count,
        "archived": len(archived),
        "condensed_index": str(cond_path),
    }


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    path = pathlib.Path(args[0])
    threshold = int(args[args.index("--threshold") + 1]) if "--threshold" in args else THRESHOLD_TOKENS

    data = json.loads(path.read_text())
    assocs = data if isinstance(data, list) else data.get("associations", [data])
    result = compact(assocs, threshold)

    print(json.dumps(result, indent=2))
    print(f"\nCompacted: {result['kept']} kept, {result['archived']} archived")


if __name__ == "__main__":
    main()
