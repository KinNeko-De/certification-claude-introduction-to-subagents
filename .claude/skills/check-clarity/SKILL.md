---
name: check-clarity
description: Analyse a LinkedIn post for clarity. Checks sentence length, jargon, and conversational tone. Returns a clarity score 1–10 with specific issues. Can be called standalone or by the linkedin-post-scorer agent.
argument-hint: "[paste the full post text]"
disable-model-invocation: false
---

Analyse the post text provided as the argument for clarity according to LinkedIn's marketing criterion: *use straightforward language, short sentences, and avoid jargon so your content is easy to read and understand.*

## Step 1 — Evaluate three clarity signals

1. **Sentence length** — count sentences longer than 20 words. Each one is a clarity problem.
2. **Jargon and acronyms** — identify any industry-specific terms, acronyms, or buzzwords a general professional audience would not immediately understand.
3. **Conversational tone** — assess whether the language feels like a natural spoken sentence or reads like a press release / internal memo.

## Step 2 — Assign a score

Score the overall clarity on a scale of 1–10:
- 9–10: All sentences short, zero jargon, reads like a conversation
- 7–8: Mostly clear with minor issues
- 5–6: Noticeable problems that interrupt reading flow
- 3–4: Several long sentences and jargon make it hard to follow
- 1–2: Dense, jargon-heavy, reads like a document

## Step 3 — Report

Return a short plain-text report with:
- The clarity score (e.g. "Clarity score: 6/10")
- Up to 3 specific issues found, each on its own line starting with "- "
- If no issues found, write "No clarity issues found."

Do not add any other prose or headings. The report is consumed programmatically by the scorer — keep it concise.
