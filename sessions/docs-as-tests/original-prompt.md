# Original concept prompt

Session: docs-as-tests · ID: 54fbb70b-2c5e-4a3b-8d24-8a1f1b7e79f8 · 2026-09-23
Output: [CONCEPT.md](CONCEPT.md)

---

In a book called Docs as Test & AI, I read the following: "LangChain’s product moves with the LLM ecosystem, so last
  month’s code sample is next month’s bug report. Their fix was to pull each inline sample into a standalone file, add
  setup and teardown, run the samples in CI, and stitch the validated code back into the docs using Bluehawk markup and
  text snippets". ... I want to see if I can do something similar w/ my code examples in my \GitHub\sensible-docs\docs\Senseml reference; get auto-notified if any start breaking. They have a consistent example structre. For an test topic where we can start messing around w/ annotations etc, look at the docs-detective branch of
  this repo at the draft-getting-start-ai.md, there's a ## Row method example that I want to see if I can test in some sort
   of CI way inspired by that paragraph (as an inital POC). you have access to Sensible API docs thru the sensible-docs MCP server and to
  calling the API thru the python SDK at docs at https://docs.sensible.so/update/docs/python-sdk-quickstart.md ... I guess
  I'm somehow imagining extracting the example's code and output and example document URL dterministically somehow, then
  running in thru a GH action that leverages a python script that takes that stuff that was extracted from the
  document...maybe running the GH action once a week or something ... bluehawk might be the way to annotate and
  deterministically extract the code samples https://mongodb-university.github.io/Bluehawk/tutorials/ and
  https://mongodb-university.github.io/Bluehawk/continuous-integration/ ...first step is just to get a notification if the
  code sample fails or the output differs from what the docs claim or an example doc URL is broken, longer term might want
  to actually author a PR w/ a proposed fix ... let's start w/ a CONCEPT.md where you take my thoughts and flesh them out
  ...what’s ambiguous, ask me questions, what are dimensions I’m not considering, what API keys do you need (I have SENSIBLE_API_KEY in local env already and probably in GH too)

## Follow-up instructions

- "there is a PR already associated w/ this worktree; use that" → moved work onto `doc-detective-poc` (PR #725).
