---
name: write-linkedin-post
description: Write a LinkedIn post about a given topic using the linkedin-post-writer subagent, then review it with the three reader personas via the linkedin-review skill.
argument-hint: "[topic]"
disable-model-invocation: false
allowed-tools: Read
---

The user wants a LinkedIn post written about a topic and then reviewed by the three simulated reader personas. This skill orchestrates the full pipeline: write → present → review.

Topic to write about: $ARGUMENTS

If no topic was provided, ask the user what the post should be about before proceeding.

Step 1 — Write the post
Use the `linkedin-post-writer` subagent to write the post about the topic above.
Tell the subagent to:
- Derive a filename slug from the topic (lowercase, spaces/special-chars → hyphens, ~50 chars max, `.md` extension).
- Write the finished post to `.claude/skills/write-linkedin-post/scratchpad/<slug>.md`.
- Return only a single raw JSON object: `{"language": "<ISO 639-1 2-char>", "file": "<path to the scratchpad file>"}`.

A deterministic `SubagentStop` hook validates the JSON against the schema and automatically forces one retry on invalid output. Do NOT re-invoke the subagent yourself.

Step 2 — Parse the result
Parse the JSON object the subagent returned and read its `language` and `file` fields.

If the returned response is still not a single valid JSON object after the automatic retry, tell the user the JSON contract failed and stop.

Step 3 — Read and present the post
Read the post text from the file path in the `file` field.
Show the post text to the user verbatim, in a form that is easy to copy-paste. Do not editorialize or summarize it.

Step 4 — Review the post
Invoke the `linkedin-review` skill via the Skill tool, passing the complete post text (verbatim, read from the file) as its arguments.
`linkedin-review` identifies the language itself, delegates to the three reader personas (techie, beamter, bedenkentraeger), and renders the reviews plus an overall verdict.
Present its output to the user as-is.
