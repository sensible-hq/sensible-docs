#!/usr/bin/env python3
"""Build the evidence records for the three ocrIfMissing claims tested on 2026-11-19, from the configs,
documents, and responses in this evidence folder.

  python3 build_records.py OUT_DIR --approved-by NAME --date YYYY-MM-DD

writes OUT_DIR/pr-825/<claim_id>.json and OUT_DIR/pr-825/files/. Point OUT_DIR at
scripts/doc-detective/testable-claims only after Frances approves the records in the review step.
"""

import argparse
import hashlib
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the evidence folder
DOCS_PR = 825
PAGE = "docs/Senseml reference/preprocessors/ocr-preprocessor.md"
SECTION = "Parameters"
RAN_ON = "2026-11-19"
ENGINE = {"note": "Production accepted the parameter as omit; sensible-hq/sensible#3533 renamed it ocrIfMissing with no change in logic, and hadn't deployed"}
DOC_URL = "https://app.sensible.so/extraction?e="

DOC_TYPES = {"array_in_order": "ocr_array_in_order", "array_reversed": "ocr_array_reversed"}


def run(name, role, purpose, document, expected):
    """One run: the config and response named `name`, checked against `expected` ({field: value})."""
    with open(os.path.join(HERE, "results", f"{name}.json"), encoding="utf-8") as f:
        response = json.load(f)
    parsed = response["parsed_document"]
    actual = {k: (v["value"] if isinstance(v, dict) else v) for k, v in parsed.items()}
    return {
        "run_id": name, "role": role, "purpose": purpose, "environment": "production", "account": "personal",
        "ran_on": RAN_ON, "engine": ENGINE, "doc_type": DOC_TYPES.get(name, name), "extraction_id": response["id"],
        "config": ("configs", f"{name}.json"), "document": ("documents", document), "response": ("results", f"{name}.json"),
        "fields": [{"field": k, "expected": v, "actual": actual[k]} for k, v in expected.items()],
    }


AGENCY = "Agency Reference: HIA-REF-4417"
RECORDS = [
    {
        "claim_id": "ocr_if_missing_match_array",
        "claim": "The OCR If Missing parameter accepts a Match array, and matches it as consecutive lines in order.",
        "claim_kind": "type or shape",
        "verdict": "holds",
        "runs": [
            run("array_in_order", "test", "The array's lines are consecutive on page 2 in this order, so it matches and nothing is OCR'd: total_premium, in a text image, stays null.",
                "cgl_quote_screenshot.pdf", {"total_premium": None}),
            run("array_reversed", "control", "The same lines in reverse order don't match as a sequence, so Sensible OCRs and total_premium extracts. Rules out the array being ignored.",
                "cgl_quote_screenshot.pdf", {"total_premium": 6109}),
        ],
    },
    {
        "claim_id": "ocr_if_missing_searches_embedded_text",
        "claim": "If Sensible doesn't find the matched text in the document's embedded text, it OCRs every page.",
        "claim_kind": "scope and order",
        "verdict": "contradicted",
        "page_change": {"summary": "The row now says \"in the document\": OCR If Missing searches the text as earlier preprocessors left it, OCR text included.",
                        "commit": "c8c5ede36", "pr": "sensible-hq/sensible-docs#825"},
        "runs": [
            run("claims_t1b_test", "test", "An earlier OCR preprocessor OCRs page 2, then OCR If Missing looks for \"Total Premium\", which is only in page 2's text image. If it searched embedded text it would OCR every page and agency_ref (page 1's image) would extract; it stays null.",
                "two_images.pdf", {"agency_ref": AGENCY, "total_premium": 6109}),
            run("claims_t1b_match_only", "control", "The earlier OCR preprocessor alone OCRs page 2 only: agency_ref null, total_premium extracted.",
                "two_images.pdf", {"agency_ref": None, "total_premium": 6109}),
            run("claims_t1_omit_only", "control", "OCR If Missing alone OCRs both pages, so agency_ref can extract when OCR runs on page 1.",
                "two_images.pdf", {"agency_ref": AGENCY, "total_premium": 6109}),
            run("claims_t1_none", "control", "No preprocessors: neither image is OCR'd.",
                "two_images.pdf", {"agency_ref": None, "total_premium": None}),
            run("claims_t1_test", "invalid", "First attempt: the earlier preprocessor matched \"Premium Summary\", which page 1's cover letter also contains, so it OCR'd page 1 itself.",
                "two_images.pdf", {"agency_ref": AGENCY, "total_premium": 6109}),
            run("claims_t1_match_only", "invalid", "First attempt's control, with the same flaw.",
                "two_images.pdf", {"agency_ref": AGENCY, "total_premium": None}),
        ],
    },
    {
        "claim_id": "ocr_if_missing_ocrs_every_page",
        "claim": "If Sensible doesn't find the matched text in the document, it OCRs every page.",
        "claim_kind": "scope and order",
        "verdict": "holds_with_bug",
        "bug": {"summary": "OCR If Missing also OCRs pages that an earlier Page Range preprocessor excluded, and their text comes back.", "status": "not_reported"},
        "runs": [
            run("claims_t1_omit_only", "test", "\"Total Premium\" is only in a text image, so OCR If Missing OCRs every page: both pages' image fields extract.",
                "two_images.pdf", {"agency_ref": AGENCY, "total_premium": 6109}),
            run("claims_t2_test", "test", "Page Range keeps page 1 only, then OCR If Missing runs. Page 2 should stay excluded, but it's OCR'd and total_premium extracts: the bug.",
                "cgl_quote_screenshot.pdf", {"total_premium": None}),
            run("claims_t2_range_only", "control", "Page Range alone excludes page 2 on the digital quote: total_premium null.",
                "cgl_quote_digital.pdf", {"total_premium": None}),
            run("claims_t2_digital_ok", "control", "No preprocessors on the digital quote: total_premium extracts, so the field works.",
                "cgl_quote_digital.pdf", {"total_premium": 6109}),
            run("claims_t2_ctrl", "control", "Page Range keeps pages 1 and 2, then OCR If Missing: total_premium extracts, as expected.",
                "cgl_quote_screenshot.pdf", {"total_premium": 6109}),
        ],
    },
]



def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out")
    parser.add_argument("--approved-by", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    folder = os.path.join(args.out, f"pr-{DOCS_PR}")
    os.makedirs(os.path.join(folder, "files"), exist_ok=True)
    for spec in RECORDS:
        record = {"schema_version": 1, "claim_id": spec["claim_id"], "docs_pr": DOCS_PR, "page": PAGE, "section": SECTION,
                  "claim": spec["claim"], "claim_kind": spec["claim_kind"], "verdict": spec["verdict"]}
        for key in ("bug", "page_change"):
            if key in spec:
                record[key] = spec[key]
        record["runs"] = []
        for r in spec["runs"]:
            r = dict(r)
            for role in ("config", "document", "response"):
                sub, name = r[role]
                # Responses and configs share names, so prefix the response's
                dest = f"response_{name}" if role == "response" else name
                shutil.copyfile(os.path.join(HERE, sub, name), os.path.join(folder, "files", dest))
                with open(os.path.join(folder, "files", dest), "rb") as f:
                    r[role] = {"path": f"files/{dest}", "sha256": hashlib.sha256(f.read()).hexdigest()}
            record["runs"].append(r)
        record["approval"] = {"by": args.approved_by, "date": args.date}
        with open(os.path.join(folder, f"{spec['claim_id']}.json"), "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)
            f.write("\n")
    print(f"Wrote {len(RECORDS)} records to {folder}")


if __name__ == "__main__":
    main()
