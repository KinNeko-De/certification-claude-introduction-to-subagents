# Disclaimer

> This repository is my personal working copy based on course material for  the Anthropic course [Introduction to subagents
](https://anthropic.skilljar.com/introduction-to-subagents) on Skilljar. It is not an official Anthropic source or endorsed resource for your training.

# Language
The agents and persona are written in german. It should write german LinkedIn Post and I want to keep one language.

> This does not mean that you should prompt in german in other situations

# References

[Frontmatter](https://code.claude.com/docs/en/sub-agents)
[Hooks for subagents](https://code.claude.com/docs/en/sub-agents#define-hooks-for-subagents)

# Tasks

[x] review skill with 3 subagents
[x] structured output
[x] create skill
[x] tools for agent
[x] hooks for debugging and forcing structured output
[x] references on reactions
[x] scratchfile
[x] skills für agents
[x] Iterative refinement loop — agent produces, a judge agent scores it, repeat until the score passes. 
[x] initial prompt (commit-message-writer, only visible when you start it correctly)
[x] subagent with forked context (needs [environment variable](https://code.claude.com/docs/en/env-vars#set-environment-variables) CLAUDE_CODE_FORK_SUBAGENT)

# Open Points

- I guess the name of the json field can be more descriptive.  "credibility_comment" and "comment" are confusing
- The final output values are only available on linkedin-reader-techie
- The techie fail to output correct json the first time since i introduced WebSearch
- i tried subagent wants feedback (linkedin-post-writer). i think this is the wrong approach. Currently it should ask for feedback, but not if called from a skill. It is never called directly. Better to write a skill that ask for feedback (like the plan mode?) and then call the subagent with a deterministic input
- the linkedin-post-scorer only use one skill for clarity and no skill for emotion and benefits.