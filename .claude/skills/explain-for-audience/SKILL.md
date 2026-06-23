---
name: explain-for-audience
description: Takes the topic currently being discussed in the conversation and explains it for three different audiences in parallel using forked context. Each fork inherits the full conversation history — no need to re-state the topic.
argument-hint: "(no argument needed — uses the current conversation context)"
disable-model-invocation: false
---

Explain the topic from the current conversation to three different audiences. Use **forked context subagents** so each fork automatically inherits the full conversation history — you do not need to pass the topic text explicitly.

## Step 1 — Fork into three parallel subagents

Invoke the Agent tool **three times in parallel**, each with `subagent_type: "fork"`. Send these exact prompts to each fork:

**Fork 1 — Manager:**
> You have the full conversation context. Write a 3–5 sentence explanation of the main topic for a non-technical manager. Focus on business impact and practical consequences. No jargon. Return only the explanation text, no headings or commentary.

**Fork 2 — Developer:**
> You have the full conversation context. Write a precise, technical explanation of the main topic for an experienced developer. Include what matters in practice — edge cases, tradeoffs, implementation details. Return only the explanation text, no headings or commentary.

**Fork 3 — One-liner:**
> You have the full conversation context. Write a single sentence that captures the core idea of the main topic — clear enough for anyone to understand. Return only that one sentence, nothing else.

## Step 2 — Present the results

Show all three explanations to the user under these headings:

### Für den Manager
[Fork 1 result]

### Für den Entwickler
[Fork 2 result]

### Für alle (Ein Satz)
[Fork 3 result]

---

**Note on forked context:** Each fork ran with a copy of the full conversation history. That is why no topic text needed to be passed explicitly — the fork agents already knew what was being discussed. This contrasts with regular subagents, which start from a clean slate and must receive all relevant context as input.
