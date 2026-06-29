# JSON5 Inline Comment Reference

Canonical inline comments for SenseML code examples. Source: docs/Senseml reference/ (PR #587; match.md and intersection.md for regex/boolean match params and horizontalAnchor/wordFilters).

When writing or enriching a JSON5 code block, copy the comment for every parameter present in the block — not just the non-obvious ones. Comments go on the same line as the parameter, in `/* */` style.

Add this line as a block comment before the opening `{` of every example:

```
/* Sensible uses JSON5 to support in-line comments*/
```

---

## Fingerprint

```json5
"fingerprint": {       /* optional. Sensible skips this config if these tests fail, improving performance when you have multiple configs */
  "tests": [           /* array of match tests; by default all tests must pass for the config to run */
    {
      "type": "startsWith", /* match types: startsWith | endsWith | includes | equals | regex */
      "text": "anyco",      /* string to match */
      "isCaseSensitive": true /* default: false */
    }
  ]
}
```

---

## Field-level (applies to every field in every example)

```json5
"id": "field_name",        /* user-friendly ID for extracted target data */
"type": "currency",        /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
"match": "first",          /* use the first occurrence of the anchor */
"match": "last",           /* use the last occurrence of the anchor */
"match": "all",            /* create an intersection for each instance of the anchor */
```

---

## Anchor

```json5
"anchor": "some text",     /* an anchor is text that always occurs in the same position relative to your target data. Without an anchor, Sensible wouldn't know which page to search in for your target data. */

/* Full anchor object: */
"anchor": {                /* an anchor is text that always occurs in the same position relative to your target data. */
  "start": "heading text", /* optional. ignore everything before this line */
  "end": "footer text",    /* optional. stop searching at this line */
  "includeEnd": true,      /* default: false. if true, include the end line in the match search */
  "match":                 /* locates the anchor line. accepts a single Match object or an array of Match objects */
    [
      {
        "type": "includes",      /* equals | startsWith | endsWith | includes | regex | first | any | all | not */
        "text": "some string",
        "isCaseSensitive": false /* default: false */
      }
    ]
}
```

Match object comments:
```json5
"text": "some string",     /* string to match */
"type": "includes",        /* match anywhere in line. */
"type": "startsWith",      /* line must start with the match */
"type": "equals",          /* matching line must equal the string exactly */
"type": "regex",           /* match using a regular expression */
"pattern": "\\d+",         /* JavaScript-flavored regex. Double-escape special characters, e.g. \\s not \s. Doesn't support capturing groups */
"flags": "ig",             /* flags to apply to the regex, e.g. "i" for case-insensitive */
"isCaseSensitive": true    /* match is case-sensitive */
```

Compound match types:
```json5
"type": "all",             /* boolean and: all sub-match conditions must pass */
"type": "any",             /* boolean or: any sub-match condition must pass */
"type": "not",             /* boolean not: finds a line that doesn't meet the sub-match condition */
"matches": [               /* array of sub-match objects; use with type any or all. Supports nesting */
```

Array of match objects:
```json5
"match": [ /* array of Match objects. Sensible matches the last element
               if each element matches a successive line in the document */
```

---

## Row method

```json5
"method": {
  "id": "row",              /* target data to extract is distributed on same horizontal line as anchor */
  "position": "right",      /* default: right. target data is to left or right of anchor. enums: left | right. */
  "tiebreaker": "second",   /* extract the line in the second non-empty cell to the left of the anchor. default: returns all cells. */
  "tiebreaker": 1,          /* extract the line in the first non-empty cell to the right of the anchor. */
  "tolerance": 0.1          /* default: 0.08. number in inches. Configure for unusual font sizes. By default, each matching line in the "row" must have a top boundary that's within 0.08 inches below or above the anchor's top boundary (total range is 0.16" inches). */
}
```

---

## Region method

```json5
"method": {
  "id": "region",           /* extracts lines contained in a defined rectangular region */
  "start": "below",         /* initial coordinates for region's top-left corner relative to anchor's boundaries. enums: above | below | left | right */
  "offsetX": 0.00,          /* horizontally shifts the region's top-left corner specified in the Start parameter by specified number of inches. positive: right, negative: left */
  "offsetY": 0.00,          /* vertically shifts the region's top-left corner specified in the Start parameter by the specified number of inches. positive: down, negative: up */
  "width": 0.00,            /* width of the region in inches */
  "height": 0.00,           /* height of the region in inches */
  "isAbsoluteOffset": false  /* default: false. if true, offsets are relative to the top-left of the page, not to the Start parameter */
}
```

---

## Intersection method

```json5
"method": {
  "id": "intersection",
  "verticalAnchor": "col heading",  /* defines the vertical axis (the column). use horizontalAnchor instead to swap which anchor defines which axis */
  "horizontalAnchor": {     /* defines the horizontal axis (the row). use verticalAnchor instead to swap which anchor defines which axis */
    "match": { "type": "regex", "pattern": "\\d+" }
  },
  "offsetX": 0,             /* default: 0. offset the vertical line left (negative) or right (positive) in inches */
  "offsetY": 0,             /* default: 0. offset the horizontal line up (negative) or down (positive) in inches */
  "width": 0,               /* default: 0. zero creates a point intersection, non-zero creates a horizontal-line region, and in conjunction with Height param, creates a rectangular region. Sensible extracts any line overlapping the point, or any line contained in the region. */
  "height": 0,              /* default: 0. same as width, but for height of the intersection region. */
  "percentOverlapX": 0.9,   /* default: 0.9. fraction of width overlap required for a line to be inside the region defined by Width or Height parameters; 0 accepts any overlap */
  "percentOverlapY": 0.8,   /* default: 0.8. same as percentOverlapX, but for height */
  "wordFilters": ["header text"] /* filters out the specified strings from the method output */
}
```

---

## Box method

```json5
"method": {
  "id": "box",              /* extracts all lines inside a box */
  "position": "right",      /* starting point for searching outward in all directions until Sensible recognizes a box. point is relative to anchor boundaries. default: center of anchor line's bounding box. enums: right | left | below | above */
  "offsetX": 0,             /* default: 0. shifts box search starting point horizontally from Position parameter. positive: right, negative: left */
  "offsetY": 0,             /* default: 0. shifts box search starting point vertically from Position parameter. positive: down, negative: up */
  "percentOverlapX": 0.9,   /* default: 0.9. minimum fractional width overlap for a line to be contained in the box */
  "percentOverlapY": 0.8,   /* default: 0.8. minimum fractional height overlap for a line to be contained in the box */
  "offsetBoxes": {          /* default: none. recognize a box offset from the starting box by a number of contiguous boxes sharing borders */
    "direction": "right",   /* direction in which to search for the offset box. enums: above | below | right | left */
    "number": 1             /* number of boxes to offset by */
  },
  "darknessThreshold": 0.9, /* default: 0.9. brightness threshold below which a pixel is considered a box border. white is 1.0 */
  "includeAnchor": false    /* default: false. if true, includes anchor lines inside box borders in the output */
}
```

---

## Sections

```json5
{
  "id": "claims_sections",  /* ID for the extracted array of sections */
  "type": "sections",       /* extracts repeating sections; returns each section as an object */
  "display": true,          /* default: true. show section start/end brackets in Sensible app for troubleshooting */
  "requiredFields": ["claim_number"], /* optional. field IDs that must be non-null for Sensible to return a section */
  "range": {
    "direction": "horizontal", /* default: horizontal. enums: horizontal | vertical */
    "anchor": {             /* required. defines which lines start each section. optionally defines which lines stop each section. optionally scopes the section group */
      "start": {            /* optional. ignore document content before this line */
        "text": "September",
        "type": "startsWith"
      },
      "match": {            /* required. repeated text marking the start of each section */
        "type": "includes",
        "text": "claim number"
      },
      "end": {              /* optional. stop looking for sections after this line */
        "text": "November",
        "type": "startsWith"
      }
    },
    "stop": {               /* optional. text marking each section's bottom boundary; if omitted, each section ends where the next starts */
      "type": "includes",
      "text": "date of claim"
    },
    "requireStop": false,   /* default: false. if true, sections end at the stop match, even if an anchor match precedes the stop match. Configure this to avoid prematurely ending each section if multiple anchor matches occur in a section */
    "offsetY": 0,           /* default: 0. shift each section's top boundary in inches from anchor match. positive: down, negative: up */
    "stopOffsetY": 0,       /* default: 0. shift each section's bottom boundary in inches from stop line. positive: down, negative: up */
    "tolerance": 0.08       /* default: 0.08. gap between sections' boundaries in inches; adjust for unusual font sizes */
  },
  "fields": [               /* array of fields to extract from each section. can include computed fields */
  ],
  "sections": []            /* optional. nested sections for complex repeating elements inside each section */
}
```

---

## Checkbox method

```json5
"method": {
  "id": "checkbox",             /* returns true if the checkbox is selected, false if unselected */
  "position": "left",           /* direction to search for the checkbox from the anchor. enums: left | right */
  "offsetX": 0,                 /* default: 0. horizontal offset in inches from the anchor; use to point inside a large or borderless checkbox */
  "offsetY": 0,                 /* default: 0. vertical offset in inches from the anchor */
  "width": 0,                   /* for large or borderless checkboxes: width in inches of the selection mark region */
  "height": 0,                  /* for large or borderless checkboxes: height in inches of the selection mark region */
  "darknessThreshold": 0.9,     /* default: auto. brightness below which a pixel is considered selected; white is 1.0. configure for dark or scanned backgrounds */
  "ignoreFormData": false        /* default: false. set to true to bypass PDF form metadata and use pixel recognition instead */
}
```

---

## Pick Values method

```json5
"method": {
  "id": "pickValues",                    /* selects values from a group of fields; commonly used to return the label of the selected option from a checkbox or radio button group */
  "source_ids": ["field_a", "field_b"],  /* IDs of the fields to evaluate */
  "match": "all",                        /* default: all. enums: one | all. one: for mutually exclusive groups (e.g. radio buttons); returns null if none or more than one field matches. all: returns every field that matches the value */
  "value": true                          /* default: true. value to match; true selects checked checkboxes */
}
```

---

Vertical sections additional parameters:
```json5
"direction": "vertical",        /* extracts columnar sections scanning left-to-right */
"columnSelection": [[1, -2]],   /* default: all columns. specifies which columns are sections; unselected columns are appended to each section */
"minColumnGap": 0,              /* default: 0. minimum column gap in inches; increase if whitespace inside a column is mistaken for a column boundary */
"ignoredColumns": [0],          /* optional. remove these column indices from output and from the SenseML search scope */
"lineFilters": {                /* optional. ignore lines spanning multiple columns that would break column recognition */
  "type": "includes",
  "text": "subtotal"
}
```
