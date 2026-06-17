---
name: write-linkedin-post
description: Write a LinkedIn post about a given topic using the linkedin-post-writer subagent, then review it with the three reader personas via the linkedin-review skill.
argument-hint: "[topic]"
disable-model-invocation: false
---

The user wants a LinkedIn post written about a topic and then reviewed by the three simulated reader personas. This skill orchestrates the full pipeline: write → present → review.

Topic to write about: $ARGUMENTS

If no topic was provided, ask the user what the post should be about before proceeding.

Step 1 — Write the post
Use the `linkedin-post-writer` subagent to write the post about the topic above.
Tell the subagent to:
- Write the finished post to the scratchpad file `.claude/skills/write-linkedin-post/scratchpad.md`.
- Return only a single raw JSON object matching its output schema: `{"language": "<ISO 639-1 2-char>", "linkedin_post": "<full post text>"}`.

A deterministic `SubagentStop` hook validates the JSON against the schema and automatically forces one retry on invalid output. Do NOT re-invoke the subagent yourself.

Step 2 — Parse the result
Parse the JSON object the subagent returned and read its `language` and `linkedin_post` fields.

If the returned response is still not a single valid JSON object after the automatic retry, fall back to reading the post text from `.claude/skills/write-linkedin-post/scratchpad.md` and tell the user the JSON contract failed (the post can still be reviewed).

Step 3 — Present the post
Show the `linkedin_post` text to the user verbatim, in a form that is easy to copy-paste. Do not editorialize or summarize it.

Step 4 — Review the post
Invoke the `linkedin-review` skill via the Skill tool, passing the complete `linkedin_post` text (verbatim) as its arguments.
`linkedin-review` identifies the language itself, delegates to the three reader personas (techie, beamter, bedenkentraeger), and renders the reviews plus an overall verdict.
Present its output to the user as-is.
