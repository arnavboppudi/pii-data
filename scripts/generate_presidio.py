"""Generate synthetic, span-labeled financial PII examples with Presidio Research.

Usage:
    .venv/bin/python scripts/generate_presidio.py --n 5000 --seed 42 \
        --out data/generated/presidio_financial.jsonl

Every value is fake (Faker). Each output line is one example:
    {"full_text", "masked", "spans": [{entity_type, entity_value, start_position, end_position}], "template_id", "doc_type"}
"""

import argparse
import json
from pathlib import Path

from presidio_evaluator.data_generator import PresidioSentenceFaker

# (doc_type, template). Placeholders are Faker provider names.
TEMPLATES = [
    # Checks
    ("check", "PAY TO THE ORDER OF {{name}} ${{pricetag}}\n{{company}}\n{{address}}\nMEMO: invoice {{bban}}\n:{{aba}}: {{bban}} 0{{random_number}}"),
    ("check", "Check #{{random_number}} dated {{date}} payable to {{name}}. Drawn on routing {{aba}}, account {{bban}}."),
    ("check", "Endorsed by {{name}} ({{phone_number}}). Deposit to acct {{iban}} only."),
    # Mortgage statements
    ("mortgage_statement", "MORTGAGE STATEMENT\nBorrower: {{name}}\nProperty Address: {{address}}\nLoan Number: {{bban}}\nStatement Date: {{date}}\nQuestions? Call {{phone_number}} or email {{email}}."),
    ("mortgage_statement", "Dear {{first_name}}, your escrow analysis for loan {{bban}} secured by {{street_address}}, {{city}} is enclosed. Borrower SSN on file: {{ssn}}."),
    ("mortgage_statement", "Co-borrower {{name}}, DOB {{date_of_birth}}, SSN {{ssn}}. Autopay from routing {{aba}} account {{bban}}."),
    # Bank statements / wires
    ("bank_statement", "Account Holder: {{name}}\n{{address}}\nAccount Number: {{bban}}\nIBAN: {{iban}}\nStatement Period ending {{date}}"),
    ("bank_statement", "Wire transfer of ${{pricetag}} from {{name}} (IBAN {{iban}}, SWIFT {{swift}}) to {{company}} on {{date}}."),
    ("bank_statement", "Card ending {{credit_card_number}} used at {{company}}. Contact {{name}} at {{phone_number}} if unauthorized."),
    # Backups / exports / logs
    ("backup_export", "customer_id,name,ssn,email,phone,dob\n{{random_number}},{{name}},{{ssn}},{{email}},{{phone_number}},{{date_of_birth}}"),
    ("backup_export", '{"user": "{{name}}", "email": "{{email}}", "card": "{{credit_card_number}}", "ip": "{{ipv4}}", "iban": "{{iban}}"}'),
    ("backup_export", "[{{date}}] login ok user={{user_name}} ip={{ipv4}} acct={{bban}} routing={{aba}}"),
    # Reports / correspondence
    ("report", "Quarterly review prepared for {{name}} ({{email}}). Client resides at {{address}} and was born {{date_of_birth}}."),
    ("report", "KYC verification: {{name}}, SSN {{ssn}}, passport {{passport_number}}, phone {{phone_number}}, employer {{company}}."),
    ("report", "Loan officer {{name}} approved application for {{name}} at {{city}}. Reference IBAN {{iban}}."),
]

ENTITY_MAP = {
    "aba": "ROUTING_NUMBER",
    "bban": "BANK_ACCOUNT",
    "swift": "SWIFT_CODE",
    "pricetag": "AMOUNT",
    "random_number": "ID_NUMBER",
    "passport_number": "PASSPORT",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="data/generated/presidio_financial.jsonl")
    args = ap.parse_args()

    faker = PresidioSentenceFaker(
        "en_US",
        lower_case_ratio=0.0,
        sentence_templates=[t for _, t in TEMPLATES],
        random_seed=args.seed,
    )
    # Extend the default mapping rather than replacing it.
    faker._entity_type_mapping.update(ENTITY_MAP)

    samples = faker.generate_new_fake_sentences(args.n)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    keep = ("entity_type", "entity_value", "start_position", "end_position")
    with out.open("w") as f:
        for s in samples:
            d = s.to_dict()
            d["spans"] = [{**{k: sp[k] for k in keep}, "entity_type": sp["entity_type"].upper()} for sp in d["spans"]]
            d["doc_type"] = TEMPLATES[d["template_id"]][0]
            d.pop("metadata", None)
            f.write(json.dumps(d) + "\n")
    print(f"wrote {len(samples)} examples to {out}")


if __name__ == "__main__":
    main()
