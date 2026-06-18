---
name: improve-linkedin-post
description: Write a LinkedIn post and iteratively improve it using the linkedin-post-scorer agent. Loops up to 3 times until the post scores 7/10 or higher. Shows the score after each iteration.
argument-hint: "[topic]"
disable-model-invocation: false
allowed-tools: Read
---

Write a LinkedIn post on the given topic and refine it in a score-driven loop. Each iteration: write → score → check. Stop when the post passes (overall score ≥ 7) or after 3 iterations.

## Step 1 — Write

Invoke the `linkedin-post-writer` subagent with the topic. On the first iteration, pass just the topic. On subsequent iterations, pass the topic plus the scorer's feedback from the previous round:

> Topic: [topic]
> Feedback from previous score: [overall.feedback]

The writer returns a JSON object with `language` and `file`. A SubagentStop hook validates this — do NOT re-invoke the writer yourself if validation fails; the hook handles the retry.

Parse the JSON and read the `file` field. Use the Read tool to load the post text from that file.

Show the post text to the user (verbatim, easy to copy-paste) with a heading showing the iteration number, e.g. **Iteration 1 — Draft**.

## Step 2 — Score

Invoke the `linkedin-post-scorer` subagent. Pass the full post text as the input.

The scorer calls the `check-clarity` skill internally and returns a JSON score object. A SubagentStop hook validates this — do NOT re-invoke the scorer if validation fails.

Parse the JSON. Show the score to the user in a compact table:

| Criterion | Score | Reason |
|-----------|-------|--------|
| Emotion   | X/10  | ...    |
| Clarity   | X/10  | ...    |
| Benefits  | X/10  | ...    |
| **Overall** | **X/10** | passed / not passed |

## Step 3 — Check

If `overall.passed` is true OR this is iteration 3: go to Step 4.

Otherwise, show the scorer's feedback to the user and go back to Step 1 for the next iteration.

## Step 4 — Final result

Show a summary:

- If the post passed: state which iteration it passed on and show the final post (verbatim, easy to copy-paste).
- If the post did not pass after 3 iterations: state that the quality threshold was not reached, show the best-scoring post (highest `overall.score` across all iterations), and include the final scorer feedback so the user can continue manually.
