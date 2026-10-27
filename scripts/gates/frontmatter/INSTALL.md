# Implementing the frontmatter gate

The gate is defined by [SPEC.md](SPEC.md) and [tests.yaml](tests.yaml); the implementation is generated from them. To (re)build it, give an agent this prompt:

```markdown
Implement the frontmatter gate in Python 3 (stdlib plus PyYAML only).

1. Read scripts/gates/frontmatter/SPEC.md: it's the complete behavior specification.
2. Write scripts/gates/frontmatter/test/tests/test_spec.py: a pytest file that loads
   tests.yaml and runs every case as described in SPEC.md "Testing".
3. Implement scripts/gates/frontmatter/frontmatter_gate.py.
4. Run the tests until every case passes. Don't edit SPEC.md or tests.yaml; if they
   seem wrong or disagree, stop and report the case and the sentence instead.
5. Run the gate on the real repo (`--root .`) and report the counts.
```

If the agent reports a gap or a contradiction, fix SPEC.md and tests.yaml (the design), then regenerate. Don't patch the implementation by hand.
