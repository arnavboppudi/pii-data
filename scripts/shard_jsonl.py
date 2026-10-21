"""Split a large JSONL file into line-aligned, gzipped shards for Git LFS.

Usage:
    python3 scripts/shard_jsonl.py data/raw/openpii_1.5m/data/train.jsonl --max-mb 1000 [--delete]

Writes <stem>-00000-of-0000N.jsonl.gz next to the input, splitting on line
boundaries once a shard reaches --max-mb of *uncompressed* text, then verifies
the shards hold exactly the input's lines. --delete removes the input afterwards.
"""

import argparse
import gzip
import hashlib
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("--max-mb", type=int, default=1000)
    ap.add_argument("--delete", action="store_true")
    args = ap.parse_args()

    src, limit = args.src, args.max_mb * 1_000_000
    stem = src.name.removesuffix(".jsonl")
    tmp_paths, src_hash, src_lines = [], hashlib.sha256(), 0

    out, written = None, 0
    with src.open("rb") as f:
        for line in f:
            if out is None or written >= limit:
                if out:
                    out.close()
                tmp = src.with_name(f"{stem}-{len(tmp_paths):05d}.tmp.jsonl.gz")
                tmp_paths.append(tmp)
                out, written = gzip.open(tmp, "wb", compresslevel=6), 0
            out.write(line)
            written += len(line)
            src_hash.update(line)
            src_lines += 1
    out.close()

    # Verify round-trip before renaming / deleting anything.
    chk_hash, chk_lines = hashlib.sha256(), 0
    for p in tmp_paths:
        with gzip.open(p, "rb") as g:
            for line in g:
                chk_hash.update(line)
                chk_lines += 1
    if (chk_hash.digest(), chk_lines) != (src_hash.digest(), src_lines):
        raise SystemExit(f"verification FAILED for {src}; shards left as *.tmp.jsonl.gz")

    n = len(tmp_paths)
    for i, p in enumerate(tmp_paths):
        final = src.with_name(f"{stem}-{i:05d}-of-{n:05d}.jsonl.gz")
        p.rename(final)
        print(f"{final}  {final.stat().st_size / 1e6:.0f} MB")
    print(f"verified {src_lines} lines, sha256 {src_hash.hexdigest()[:16]}…")
    if args.delete:
        src.unlink()
        print(f"deleted {src}")


if __name__ == "__main__":
    main()
