# From documentation
# Forked subagents require Claude Code v2.1.117 or later. 
# From v2.1.161 the /fork command is enabled by default;
# on earlier versions it requires setting the CLAUDE_CODE_FORK_SUBAGENT environment variable to 1. 
# Letting Claude itself spawn forks is experimental and may change in future releases. 
# This capability may also be enabled in interactive sessions as part of a staged rollout.
# https://code.claude.com/docs/en/sub-agents#fork-the-current-conversation

# Note from me: In interactive mode Version 2.1.183 it only works with environment variable.

$env:CLAUDE_CODE_FORK_SUBAGENT = "1"

Write-Host "Set CLAUDE_CODE_FORK_SUBAGENT for this session."
