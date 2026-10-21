# The Datasets, Explained Simply

**PII** means "personally identifiable information": anything that can point to a specific
person, like a name, Social Security number, bank account number, address, or phone number.

This repo holds example text that contains PII, with the PII already marked.
We use it to teach and test a tool that finds PII in financial documents and checks
whether it has been properly hidden (redacted).

Most of this data is **fake**. The names, numbers, and addresses were made up by
computers, so no real person is exposed. The one exception is MultiPII (see below).

---

## 1. Gretel Financial PII

📁 `data/raw/gretel_finance/`

- **What it is:** About 56,000 made-up financial documents, such as loan papers,
  bank forms, and statements.
- **What's marked:** 29 kinds of PII, like Social Security numbers, bank routing numbers,
  account PINs, employee IDs, and addresses.
- **Languages:** English, plus Dutch, French, German, Italian, Spanish, and Swedish.
- **Real or fake?** Fake.
- **Why it's useful:** It's the closest match to what we care about: financial paperwork.
- **Heads-up:** The creators say a few of the labels might be wrong, so spot-check before
  trusting it fully.
- **License:** Apache 2.0. Free to use.

## 2. Ai4Privacy OpenPII

📁 `data/raw/openpii_1.5m/`

- **What it is:** About 1.6 million short made-up texts in many languages (1.31 million for training, 326,000 for testing).
- **What's marked:** Everyday personal info like names, emails, phone numbers,
  addresses, and dates.
- **Real or fake?** Fake.
- **Why it's useful:** It's huge, so it gives the tool lots of practice with general
  personal info. It's less focused on financial documents.
- **Note:** The files are compressed and split into pieces (`.jsonl.gz`) because they
  are too big for GitHub otherwise.
- **License:** CC-BY-4.0. Free to use, but you must credit Ai4Privacy.

## 3. Presidio Generated Data

📁 `data/generated/presidio_financial.jsonl`

- **What it is:** 5,000 made-up snippets we created ourselves using Microsoft's
  Presidio tool. They look like checks, mortgage statements, bank statements,
  data backups, and reports.
- **What's marked:** Names, SSNs, bank and routing numbers, card numbers, IBANs,
  emails, phone numbers, addresses, passports, and more.
- **Real or fake?** Fake.
- **Why it's useful:** We control it. If the other datasets are missing a certain kind
  of document, we can add a template and make more examples.
- **How to make more:** Run `scripts/generate_presidio.py`.
- **License:** Ours.

## 4. MultiPII

📁 `data/raw/multipii/MultiPII.csv`

- **What it is:** A small list of 197 real documents and social media posts (passports,
  résumés, screenshots), with the PII in each one written out.
- **What's included:** Only a link to each original image and a list of the PII found in it.
  The images themselves are **not** included.
- **Real or fake?** ⚠️ **Real.** These are real people's details collected from public websites.
- **Why it's useful:** It shows how the tool does on messy, real-world documents.
- **How to use it:** Only for **testing** the tool, never for training it.
- **License:** CC-BY-4.0. Free to use, but you must credit the MultiPII authors.

---

## Quick Comparison

| Dataset | Size | Real or fake? | Best for |
|---|---|---|---|
| Gretel Financial PII | ~56,000 docs | Fake | Financial documents (main training data) |
| Ai4Privacy OpenPII | ~1.6 million texts | Fake | General personal info (lots of extra practice) |
| Presidio Generated | 5,000 snippets | Fake | Filling gaps with custom document types |
| MultiPII | 197 items | **Real** | Final testing only |
