# Implementing the example-coverage gate

The gate is defined by [SPEC.md](SPEC.md) and [tests.yaml](tests.yaml); the implementation is generated from them. To (re)build it, give an agent this prompt:

```markdown
Implement the example-coverage gate in Python 3 (stdlib only; the tests may use PyYAML and pytest).

1. Read scripts/gates/examples/SPEC.md: it's the complete behavior specification. For the
   code-test markup it reads, see scripts/doc-detective/README.md ("Code tests") and
   scripts/doc-detective/codetests/markup.py, but don't import them or run code_tests.py.
2. Write scripts/gates/examples/test/tests/test_spec.py: a pytest file that loads
   tests.yaml and runs every case as described in SPEC.md "Testing".
3. Implement scripts/gates/examples/example_coverage.py.
4. Run the tests until every case passes. Don't edit SPEC.md or tests.yaml; if they
   seem wrong or disagree, stop and report the case and the sentence instead.
5. Run the gate on the real repo with an empty base (`--base <empty dir> --head .`) and
   report the counts per rule and the --print-tests list. Then run it on a few merged
   pull requests (base: the merge commit's parent, head: the merge commit, each extracted
   with `git archive`) and report what it flags.
```

If the agent reports a gap or a contradiction, fix SPEC.md and tests.yaml (the design), then regenerate. Don't patch the implementation by hand.
