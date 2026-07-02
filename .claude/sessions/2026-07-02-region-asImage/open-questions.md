# Open questions — region: asImage + percentOverlapX/Y

## asImage: problem and use cases

Need to dig deeper before deciding on example coverage or description specificity.

- What problem is `asImage` solving that existing methods don't? (The Signature method detects presence; `asImage` captures the visual — but what's the intended downstream use?)
- What are the primary use cases beyond signatures, stamps, and checkboxes?
- Is the output (a `data:image/png;base64,...` string) intended to be stored, forwarded to a vision model, displayed in a UI, or all of the above?
- Should the doc distinguish `asImage` from the Signature method, and if so, how?
