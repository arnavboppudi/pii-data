# PII data

Training/evaluation data for a financial-document PII detector and redaction checker.

## Setup

```bash
scripts/download_data.sh                      # raw datasets -> data/raw/ (~5.5 GB)
python3 -m venv .venv && .venv/bin/pip install presidio-evaluator pandas pyarrow
.venv/bin/python scripts/generate_presidio.py --n 5000 --seed 42   # -> data/generated/
```

Cloning: large files are in [Git LFS](https://git-lfs.com) — run `git lfs install` before `git clone`.

Loading the OpenPII shards:

```python
import pandas as pd, glob
df = pd.concat(pd.read_json(p, lines=True) for p in sorted(glob.glob("data/raw/openpii_1.5m/data/validation-*.jsonl.gz")))
# or: datasets.load_dataset("json", data_files="data/raw/openpii_1.5m/data/train-*.jsonl.gz")
```

## Layout

| Path | Source | License | Contents |
|---|---|---|---|
| `data/raw/gretel_finance/` | [gretelai/synthetic_pii_finance_multilingual](https://huggingface.co/datasets/gretelai/synthetic_pii_finance_multilingual) | Apache-2.0 | ~56k synthetic financial docs, 29 PII types, parquet per language + `combined_*`. Labels may contain errors — spot-check. |
| `data/raw/openpii_1.5m/` | [ai4privacy/pii-masking-openpii-1.5m](https://huggingface.co/datasets/ai4privacy/pii-masking-openpii-1.5m) | CC-BY-4.0 (attribution required) | Multilingual synthetic text with char spans + token labels. Stored as gzipped, line-aligned shards (`data/train-*-of-*.jsonl.gz`, `data/validation-*-of-*.jsonl.gz`) via Git LFS; concatenated they equal the upstream `train.jsonl` / `validation.jsonl`. |
| `data/raw/multipii/MultiPII.csv` | [Zenodo 16903816](https://zenodo.org/records/16903816) | CC-BY-4.0 | 197 items: source URL + `Type: Value` annotations. **Images are not included** — only links. |
| `data/generated/presidio_financial.jsonl` | `scripts/generate_presidio.py` ([Presidio Research](https://github.com/microsoft/presidio-research)) | yours | Fake checks, mortgage/bank statements, backups/exports, reports with exact char spans. Add templates in the script to fill gaps. |

## ⚠️ MultiPII contains real PII

Unlike the other sources, MultiPII annotates **real people's documents** scraped from public sites
(passports, résumés, social posts). It is redistributed here unchanged under its CC-BY-4.0 license, with attribution below.
Use it only as a small held-out eval set and don't train on it.

## Attribution

- Gretel.ai, *Synthetic PII Finance Multilingual* (Apache-2.0).
- Ai4Privacy, *OpenPII 1.5M* (CC-BY-4.0).
- MultiPII authors, *MultiPII: A Multimodal Benchmark for Personal Identifiers Detection in Real-World Documents*, Zenodo, doi:10.5281/zenodo.16903816 (CC-BY-4.0).
