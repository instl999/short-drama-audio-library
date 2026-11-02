"""Search the supplied audio library without loading audio or requiring dependencies."""
from pathlib import Path
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="Title, original path, or English tag")
    parser.add_argument("--kind", choices=["bgm", "sfx"])
    parser.add_argument("--mood", help="Exact English mood, e.g. suspense, sad, warm")
    parser.add_argument("--tag", help="Exact English function/style tag, e.g. riser, rain")
    parser.add_argument("--review", action="store_true", help="Only assets without a mood label")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true", help="Emit complete matching metadata")
    parser.add_argument("--verify", action="store_true", help="Verify local files and SHA-256 hashes")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    assets = json.loads((root / "catalog.json").read_text(encoding="utf-8"))["assets"]
    matches = [a for a in assets if
               (not args.kind or a["kind"] == args.kind) and
               (not args.mood or args.mood in a["moods"]) and
               (not args.tag or args.tag in a["tags"]) and
               (not args.review or a["needs_mood_review"]) and
               args.query.casefold() in json.dumps(a, ensure_ascii=False).casefold()]
    if args.verify:
        import hashlib
        failures = []
        for asset in matches:
            path = root / asset["path"]
            if not path.is_file():
                failures.append(f"missing: {asset['path']}")
                continue
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if digest != asset["sha256"]:
                failures.append(f"SHA-256 mismatch (run git lfs pull if this is a pointer): {asset['path']}")
        print(f"Verified {len(matches) - len(failures)}/{len(matches)} assets")
        for failure in failures:
            print(failure)
        raise SystemExit(1 if failures else 0)
    shown = matches[:max(0, args.limit)]
    if args.json:
        print(json.dumps(shown, ensure_ascii=False, indent=2))
    else:
        for asset in shown:
            print(f"{asset['id']} [{', '.join(asset['moods']) or 'unclassified'}] {asset['duration_seconds']:.1f}s")
            print(f"  {asset['path']}")
            print(f"  {asset['title']}")
        print(f"Showing {len(shown)} of {len(matches)} matches")


if __name__ == "__main__":
    main()
