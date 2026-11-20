# Doc comparison rubric

Use this rubric to compare two versions of the same docs section, for example a new draft against the published page, or a skill's output against an earlier hand-written draft. Copy the template into the work's session folder (`.claude/sessions/<work>/rubric.md`), fill it in, and commit it to the docs PR.

Each criterion is a yes/no question drawn from the style guides, editorial preferences, and the source PR. Each cell holds a calibrated probability between 0 and 1 that the answer is yes.

---

## How to fill it in

1. **Name the versions.** Give each one a column heading and a link: the published page (`https://docs.sensible.so/docs/<slug>#<anchor>`) or the branch view (`https://github.com/<repo>/blob/<branch>/<path>#<anchor>`).
2. **Answer each question with a probability.** Write a number between 0 and 1 that the answer is yes, to two decimal places. Don't add up the probabilities or average them: the questions overlap, so a total double counts.
3. **Calibrate.**
   - 0.95 or higher means you checked it: you ran Vale, ran the config, or read the engine source. Don't go above 0.80 for a claim you haven't checked.
   - Around 0.50 means you can't tell. Say what would settle it.
   - Answer the question as asked. A version that's better overall can still score low on a question.
4. **Give the evidence.** In the Why column, quote the line or name the check that decides the answer. When one version's answer depends on an assumption nobody has checked, say so.
5. **Add questions that are specific to the source PR.** Add rows for this feature. For example, ask whether the doc shows the usage pattern the PR's reviewer notes call out. Cite the PR.
6. **Answer the overall question.** For each version, give the probability that it's the better version of the section. Then describe the best-of-both version in two or three sentences. Say which parts to take from each version, and which questions that version would raise.
7. **Note the rubric's limits.** These include questions that overlap, judgment calls that no written rule covers, and which questions need the reviewer to calibrate.

---

## Template

```markdown
# Rubric: <section> — <version A> vs. <version B>

- **<version A>:** <link>
- **<version B>:** <link>
- **Source PR:** sensible-hq/sensible#<number>

Each cell is a calibrated probability between 0 and 1 that the answer is yes.

| # | Question (source) | <version A> | <version B> | Why |
|---|---|---|---|---|
| 1 | Does every claim match the engine? (source PR, engine source) | | | |
| 2 | Does the first sentence start with a third-person verb? (`sensible-opening-sentence`) | | | |
| 3 | Does it lead with the reader's scenario before the mechanism? (`sensible-scenario-first`) | | | |
| 4 | Does the example data show why the feature is useful? (`sensible-realistic-example-data`) | | | |
| 5 | Does it warn about every pitfall a reader will hit? | | | |
| 6 | Is it no longer than it needs to be? (style guide: "Terse and precise") | | | |
| 7 | Does it match the sections around it in wording and shape? (`sensible-copy-sibling-wording`) | | | |
| 8 | Do the code comments explain why, and agree with the code? (`sentence-word-guidance.md`: inline comments) | | | |
| 9 | Is there one example per scenario? (`sensible-example-per-scenario`) | | | |
| 10 | Can a reader get the output shown? (`create-docs-example`: actual output) | | | |
| 11 | <a question from the source PR, for example: does it show the main way to use the feature plainly?> | | | |
| 12 | Does it pass the mechanical rules? (the Vale hook and code-block check in `.claude/hooks/vale_gate.py`) | | | |

**Is this the better version of the section?** <version A>: <p>. <version B>: <p>.

**Best of both:** <which parts to take from each version, and which questions that version would raise>

**Limits of this rubric:** <questions that overlap, judgment calls that no written rule covers, assumptions that a check would settle>
```

---

## Running the mechanical check

The Vale hook runs only on `Edit` and `Write`. To check a version as a whole, including the published page, call the hook's lint function on the section's lines:

```bash
python3 - <path/to/page.md> <first-line> <last-line> <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, ".claude/hooks")
import vale_gate as g
page, first, last = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for a in g.lint(Path.cwd(), page.read_text(), page.name, "suggestion"):
    if first <= a["line"] <= last:
        print(a)
PY
```

To check the published version, run `git show origin/v0:<path>` in the upstream `sensible-docs` clone and save the output to a scratch file. Then run the check on that file.
