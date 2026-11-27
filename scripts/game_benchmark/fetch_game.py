"""Download one A2Z GameSpec-Bench game (design document, contract, sprite library) and check each file's sha256.

Usage: python3 fetch_game.py <split> <game> <dest>   e.g. big abyssal_chain /home/brian/projects/data/aes-gamebench/games
Source: https://huggingface.co/datasets/KRAFTON/A2Z-GameSpec-Bench (MIT). Plan: docs/planning/game-benchmark.md.
"""
import hashlib, json, sys, urllib.request
from pathlib import Path

REPO = "https://huggingface.co/datasets/KRAFTON/A2Z-GameSpec-Bench"


def get(path: str) -> bytes:
    with urllib.request.urlopen(f"{REPO}/resolve/main/{path}", timeout=60) as r:
        return r.read()


def main(split: str, game: str, dest: Path) -> int:
    manifest = {f["path"]: f["sha256"] for f in json.loads(get("metadata/manifest.json"))["files"]}
    wanted = [p for p in manifest if p == f"gdds/{split}/{game}.md"
              or p.startswith(f"contracts/{split}/{game}/") or p.startswith(f"library/{split}/{game}/")]
    if not any(p.startswith("gdds/") for p in wanted):
        print(f"no such game: {split}/{game}"); return 1
    bad = 0
    for p in wanted:
        data = get(p)
        ok = hashlib.sha256(data).hexdigest() == manifest[p]
        bad += not ok
        out = dest / game / p.split("/", 2)[0] / Path(p).name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
    print(f"RESULT game={game} files={len(wanted)} sha256_mismatches={bad} dest={dest / game}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], Path(sys.argv[3])))
