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

Each agent will return a review written in plain text.
Capture the full review each agent returns.

Step 3 — Present results
Show the three reviews to the user, clearly separated and labeled:
1. Review by Techie (verbatim)
2. Review by Beamter (verbatim)
3. Review by Bedenkenträger (verbatim)

Do not editorialize or summarize any output.
