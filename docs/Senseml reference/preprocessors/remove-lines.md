---
title: Remove lines
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Remove lines matching a pattern from all pages in a document'
  robots: index
next:
  description: ''
---
Removes lines that match the specified text from all pages in the document. For example, use this preprocessor to remove watermarks. This preprocessor is a layout-independent alternative to the Remove Header and Remove Footer preprocessors.

# Parameters

| key                  | value                                               | description                                                  |
| -------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**)  | `removeLines`                                       |                                                              |
| match (**required**) | [Match](doc:match) object or array of Match objects | Sensible removes lines that match the specified text from all pages in the document |

# Examples

The following example shows using two `removeLines` preprocessors to clean up an academic transcript before extraction:

- The first preprocessor removes page number lines (`page 1 of 3`, `page 2 of 3`, etc.) using a regex pattern. Without this, page number lines would appear inline in the extracted text.
- The second preprocessor removes a rotated diagonal watermark ("This is Not an Official Transcript") using the [angleFilter](doc:match#global-parameters) option. The `angleFilter` targets only lines rotated between 30 and 60 degrees, so horizontal body text is unaffected.

**Config**

```json
{
  "preprocessors": [
    {
      /* remove "page x of y" lines */
      "type": "removeLines",
      "match": {
        "type": "regex",
        "pattern": "^page \\d+ of \\d+$"
      }
    },
    {
      /* remove rotated watermark text (30–60 degrees) */
      "type": "removeLines",
      "match": {
        "type": "regex",
        "pattern": ".",
        "angleFilter": {
          "minAngle": 30,
          "maxAngle": 60
        }
      }
    }
  ],
  "fields": [
    {
      /* to verify lines were removed, print out document text */
      "id": "all_text",
      "method": {
        "id": "documentRange",
        "includeAnchor": true
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}
```

**Example document**

The following image shows the first page of the example document. Note the `page 1 of 3` line at the bottom, which is removed by the first preprocessor.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/remove_lines.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/remove_lines.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "all_text": {
    "type": "string",
    "value": "Academic History Fictional Example Transcript Create Date: 06/19/2025 10:47:25 General Information García, Ana López Student: A12345678 PID: Student Level: UN Fictional College College: Major: Computer Science Intended Degree: Bachelor of Arts Cumulative Summary Grade Option UC-Crdts Attm Crdts Pssd UC-GPA Crdts UC-Grade Points UC-GPA Letter 73.00 71.00 69.00 201.20 2.915 P/NP 12.00 16.00 0.00 0.00 0.000 TOTAL 85.00 87.00 69.00 201.20 2.915 Total UCSD Upper Division Units Passed: 8.00 All credits are in quarter units. Cumulative summaries on this record may reflect adjustments for repeated courses and/or other adjustments made in accordance with UCSD academic policies. UCSD Undergraduate Courses by Term Term: Fall Qtr 2025 Subject Course Course Title Units Grade Points Repeat CCE 3 Elements/CommEngageColResearch 4.00 0.00 INTL 102 Econ, Politics & Intn'l Change 4.00 0.00 MGT 103 Product Marketing & Management 4.00 0.00 MGT 131A Intermediate Accounting A 4.00 0.00 Term Credits Passed: 0.00 Term GPA: 0.000 Term Grade Points: 0.00 Academic Status: Term GPA Credits: 0.00 Term: Spring Qtr 2025 Subject Course Course Title Units Grade Points Repeat ECON 4 Financial Accounting 4.00 0.00 INTL 100 Analysis/Argument/Real-World 4.00 F 0.00 LTLA 3 Intermediate Latin II 4.00 A 16.00 MGT 5 Managerial Accounting 4.00 D 4.00 Survey of World Literature MUS 19R 4.00 A+ 16.00 Term Credits Passed: 12.00 Term GPA: 2.250 Term Grade Points: 36.00 Academic Status: Term GPA Credits: 16.00 Term: Winter Qtr 2025 Subject Course Course Title Units Grade Points Repeat CCE 2 Cultivat/CommInformedPractices 4.00 A 16.00 LTLA 2 Intermediate Latin I 4.00 A 16.00 SIO 25 Climate Change and Society 4.00 P 0.00 Term Credits Passed: 12.00 Term GPA: 4.000 Term Grade Points: 32.00 Academic Status: Good Standing Term GPA Credits: 8.00 Term: Fall Qtr 2024 Subject Course Course Title Units Grade Points Repeat LTLA 1 Beginning Latin 4.00 A 16.00 Topics in Modern History LTWL 116 4.00 A 16.00 MUS 8 American Music: Jazz Cultures 4.00 A 16.00 TDGE 1 Introduction to Theatre 4.00 P 0.00 Term Credits Passed: 16.00 Term GPA: 4.000 Term Grade Points: 48.00 Academic Status: Good Standing Term GPA Credits: 12.00 Term Honors: Provost Honors Term: Spring Qtr 2024 Subject Course Course Title Units Grade Points Repeat BILD 3 Organismic&Evolutionary Biol 4.00 NP 0.00 CCE 1 CriticalApproach/CommPractice 4.00 B 12.00 ECON 4 Financial Accounting 4.00 W 0.00 LTEN 28 Intr/Asian-American Literature 4.00 A- 14.80 Term Credits Passed: 8.00 Term GPA: 3.350 Term Grade Points: 26.80 Academic Status: Good Standing Term GPA Credits: 8.00 Term: Winter Qtr 2024 Subject Course Course Title Units Grade Points Repeat Introduction to Sociology ANTH 21 4.00 B- 10.80 ETHN 2R R-Intro:CirculationsofDifferen 4.00 A- 14.80 HIUS 149 United States in the 1960's 4.00 A- 14.80 Term Credits Passed: 12.00 Term GPA: 3.366 Term Grade Points: 40.40 Academic Status: Good Standing Term GPA Credits: 12.00 Term: Fall Qtr 2023 Subject Course Course Title Units Grade Points Repeat Environmental Economics ANTH 10 4.00 D 4.00 BILD 10 Fundamental Concepts/Modrn Bio 4.00 D 4.00 LTKO 1A Beginning Korean:First Yr. I 5.00 C 10.00 Term Credits Passed: 13.00 Term GPA: 1.384 Term Grade Points: 18.00 Academic Status: Subject to Academic Disqual Term GPA Credits: 13.00 Transfer Credit Entity Name Dates Credit Advanced Placement Credit 05/22 - 05/23 8.00 Contra Costa College 01/22 - 05/22 6.00 CAUTION: Transfer Course Disclaimer Substitution of Transfer Courses for UCSD requirements may be subject to additional checks or approvals. Colleges and Departments require additional approvals. Please see your College or Department for clarification. Please note: Transfer courses will display approximately 8 weeks after they are received on campus. Transfer Courses Subject Course Course Title Units Grade Term Level UCSD Transferred From Approx AP EC3 Engl Lit Comp 8.00 P SP23 LD Advanced Placement Credit CISC 135 Intro To Computers 6.00 A SP22 LD Contra Costa College Academic Events Event Date UC ENTRLVL WRITNG REQT SATISFD 09/22/2023 AMER HIST& INST REQT SATISFIED 12/08/2023"
  }
}
```
