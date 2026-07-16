# PDF Download Links in Blog Posts

Links instructing readers to download a sample PDF, identified by judgment.
"type: direct PDF" = link ends in `.pdf`. "type: directory" = GitHub folder link used as a download anchor.

For directory links, a candidate PDF is proposed based on context clues from the post.

---

## extracting-data-from-rate-confirmations
- **anchor:** "Download example PDF"
- **type:** direct PDF
- **url:** `https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/rate_confirmation_ch_robinson.pdf`
- **note:** from sensible-docs repo, not sensible-configuration-library

---

## how-to-extract-data-from-bank-statements-with-sensible
- **anchor:** "download an example PDF for a Chase statement"
- **type:** directory
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Bank%20Statements`
- **candidate PDF:** a Chase bank statement — figcaption in the post reads "Chase bank statement"; another post links to `bank_statements/bank_of_america` as a sibling directory, suggesting `bank_statements/chase/` exists with a Chase PDF

---

## how-to-extract-data-from-closing-disclosures
- **anchor:** "download an example PDF"
- **type:** directory
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Real%20Estate`
- **candidate PDF:** a mortgage closing disclosure — figcaption reads "Mortgage closing disclosure"; config path cited in same post is `real_estate/closing_disclosure`, so the PDF likely lives under `templates/Real%20Estate/Closing%20Disclosure/` or similar

---

## how-to-extract-data-from-explanation-of-benefits-documents
- **anchor:** "download an example PDF"
- **type:** directory
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Healthcare`
- **candidate PDF:** a Medicaid EOB — figcaption reads "Medicaid explanation of benefits"; the post's screenshot image filename contains `redacted_medicaid_sample_shortened.pdf`, strongly suggesting the sample PDF is a redacted Medicaid EOB; config path cited is `eobs`, so PDF likely lives under `templates/Healthcare/EOBs/` or similar

---

## low-code-pdf-to-database-with-zapier-and-sensible

### 2021 1040 (directory link)
- **anchor:** "2021 1040 example document"
- **type:** directory
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Tax%20Forms`
- **candidate PDF:** `https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf` — the same post contains this as a direct PDF link for the same 1040 content (see next entry); the directory link is likely an older/inconsistent anchor pointing to the same file

### 2021 1040 (direct PDF link)
- **anchor:** "1040 example document" (used inline to verify extraction result)
- **type:** direct PDF
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf`

### 2018 1040
- **anchor:** "2018 1040 example document"
- **type:** directory
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2018`
- **candidate PDF:** `https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2018/1040_2018_sample.pdf` — inferred from the 2021 direct link pattern (`tax_forms/1040/{year}/1040_{year}_sample.pdf`)

### 2019 1040
- **anchor:** "2019 1040 example document"
- **type:** directory
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2019`
- **candidate PDF:** `https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2019/1040_2019_sample.pdf` — same pattern

### 2020 1040
- **anchor:** "2020 1040 example document"
- **type:** directory
- **url:** `https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2020`
- **candidate PDF:** `https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2020/1040_2020_sample.pdf` — same pattern
