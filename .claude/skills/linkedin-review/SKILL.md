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
Identify the language of the post.

Step 2 — Delegate reviews
Use each of these independent agents to review the post.
Pass the complete post text above (verbatim) to each.
Tell them to answer in the language you identify in Step 1
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
For each agent response, verify:
- the response parses as a single JSON object (strip a Markdown code fence first if present)
- `first_impression`, `credibility`, and `verdict` are non-empty strings
- `relevance` is an integer between 1 and 10
- `reaction` is null or one of "Daumen hoch", "Gefällt mir", "Unterstütze ich", "Witzig"
- `comment` is null or a string

If a response fails validation, re-invoke that agent once with the same input. If it fails again, show the user the raw response together with the list of missing or invalid fields, and continue with the remaining reviews.

Step 4 — Present results
Show the three reviews to the user, clearly separated and labeled:
1. Review by Techie
2. Review by Beamter
3. Review by Bedenkenträger

Render each review as a formatted section with these German labels, with the field values verbatim (render null as "Keine"):
- Erster Eindruck (first_impression)
- Glaubwürdigkeit (credibility)
- Relevanz (relevance)
- Reaktion (reaction)
- Kommentar (comment)
- Fazit (verdict)

Do not show the raw JSON. Do not editorialize or summarize any field content.
