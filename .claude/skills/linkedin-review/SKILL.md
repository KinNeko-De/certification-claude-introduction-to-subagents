---
name: linkedin-review
description: Review an already-written LinkedIn post using three simulated reader personas. Does NOT create a post. Passes the provided post text to linkedin-reader-techie, linkedin-reader-beamter, and linkedin-reader-bedenkentraeger, who each review it independently.
argument-hint: "[copy and paste the post]"
disable-model-invocation: true
---

The user has an already-written LinkedIn post and wants it reviewed by three simulated readers. Do NOT write or rewrite the post.

Post to review: $ARGUMENTS

If no post text was provided, ask the user to paste the complete LinkedIn post before proceeding.

Step 1 - Identifiy the language
Identify the language of the post. Pass this language to all subagents you create.

Step 2 — Delegate reviews
Use each of these independent subagents to review the post.
Pass the complete post text above (verbatim) to each.
Tell them to answer in the expected language you identify in Step 1
- linkedin-reader-techie
- linkedin-reader-beamter
- linkedin-reader-bedenkentraeger

Each agent returns a single JSON object with this schema:

```json
{
  "first_impression": "string — one sentence: does the reader keep reading or scroll on?",
  "credibility": "string — credibility from the persona's professional point of view",
  "relevance": "integer 1–10 (1 = forgotten after 10 seconds, 5 = read the whole text, 7 = think about it, 8 = react to it, 10 = share it)",
  "reaction": "null if relevance < 5, otherwise one of: \"Daumen hoch\", \"Gefällt mir\", \"Unterstütze ich\", \"Witzig\"",
  "comment": "null, or string — the persona's comment under the post",
  "verdict": "string — honest overall assessment"
}
```

Capture the full response each agent returns.

Step 3 — Validate
A deterministic SubagentStop hook validates each agent response against the schema and automatically forces one retry on invalid output. Do NOT re-invoke an agent yourself.

If a returned response is still not a single valid JSON object, show the user the raw response and continue with the remaining reviews.

Step 4 — Present results
Show the reviews of each subagent to the user, clearly separated and labeled in the identified language.

Render each review as a formatted section with the identified language, with the field values verbatim (render null as none is he identified language):
- first_impression
- credibility
- relevance
- reaction
- comment
- verdict

Do not show the raw JSON. Do not editorialize or summarize any field content.
