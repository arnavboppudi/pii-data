#!/usr/bin/env bash
# Download the raw PII datasets into data/raw/. Re-runnable: files already at
# the expected size are skipped, partial files are resumed.
set -euo pipefail
cd "$(dirname "$0")/.."

hf_dataset() {  # hf_dataset <repo_id> <dest_dir>
  local repo=$1 dest=$2
  curl -sf "https://huggingface.co/api/datasets/$repo/tree/main?recursive=true" |
    python3 -c 'import sys,json; [print(f["size"], f["path"]) for f in json.load(sys.stdin) if f["type"]=="file"]' |
    while read -r size path; do
      local out="$dest/$path"
      if [[ -f "$out" && $(stat -f%z "$out" 2>/dev/null || stat -c%s "$out") == "$size" ]]; then
        continue
      fi
      # Large JSONL files are stored as gzipped shards (see shard_jsonl.py).
      if [[ "$out" == *.jsonl ]] && compgen -G "${out%.jsonl}-*-of-*.jsonl.gz" >/dev/null; then
        continue
      fi
      echo "fetching $repo/$path ($size bytes)"
      mkdir -p "$(dirname "$out")"
      curl -sSfL -C - --retry 5 --retry-all-errors -o "$out" "https://huggingface.co/datasets/$repo/resolve/main/$path"
    done
}

# 1. Gretel synthetic financial PII (Apache-2.0)
hf_dataset gretelai/synthetic_pii_finance_multilingual data/raw/gretel_finance

# 2. Ai4Privacy OpenPII 1.5M (CC-BY-4.0, attribution required) — ~5.3 GB
hf_dataset ai4privacy/pii-masking-openpii-1.5m data/raw/openpii_1.5m

for f in data/raw/openpii_1.5m/data/*.jsonl; do
  [[ -f "$f" ]] && python3 -I scripts/shard_jsonl.py "$f" --max-mb 1000 --delete
done

# 3. MultiPII benchmark (CC-BY-4.0) — annotations + source URLs only, no images
mkdir -p data/raw/multipii
[[ -s data/raw/multipii/MultiPII.csv ]] ||
  curl -fL -o data/raw/multipii/MultiPII.csv \
    "https://zenodo.org/api/records/16903816/files/MultiPII.csv/content"

echo "done"; du -sh data/raw/*
