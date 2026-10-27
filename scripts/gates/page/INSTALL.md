# Implementing the page gate

The gate is defined by [SPEC.md](SPEC.md) and [tests.yaml](tests.yaml); the implementation is generated from them. To (re)build it, give an agent this prompt:

```markdown
Implement the page gate in Python 3 (stdlib plus PyYAML only).

1. Read scripts/gates/page/SPEC.md: it's the complete behavior specification.
2. Write scripts/gates/page/test/tests/test_spec.py: a pytest file that loads
   tests.yaml and runs every case as described in SPEC.md "Testing".
3. Implement scripts/gates/page/page_gate.py. It reads the alphabetical folders from
   scripts/gates/page/alphabetical-folders.yaml under --root; don't hardcode them.
4. Run the tests until every case passes. Don't edit SPEC.md or tests.yaml; if they
   seem wrong or disagree, stop and report the case and the sentence instead.
5. Run the gate on the real repo (`--root .`), with and without `--strict`, and
   report the counts per rule.
```

If the agent reports a gap or a contradiction, fix SPEC.md and tests.yaml (the design), then regenerate. Don't patch the implementation by hand.
