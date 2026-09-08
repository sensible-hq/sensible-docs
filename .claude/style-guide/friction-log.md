# Style friction log

Running record of style and framing mistakes caught during doc sessions. Each entry has a root cause and a rule so the pattern becomes a durable constraint, not a one-time correction.

---

## 2026-09-08 — extra-data.md (manual edits)

### Opening sentence described the API instead of the user action

**What happened:** The opening read "Returns a value from an `extra_data` object you supply in an asynchronous extraction request. Use this method to bring request-time context into a config so validations, postprocessors, and computed fields can read it." Frances rewrote it to "Use this method to inject data you supply at request time into the extraction config, so you can dynamically validate, transform, and postprocess extracted document data."

**Rule:** Reference pages should open with what the user does and why, not with what the API returns. Lead with "Use this method to..." not "Returns a...". Mechanical API description belongs in the parameters table, not the opening.
