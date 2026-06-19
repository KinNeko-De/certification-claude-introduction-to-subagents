# Schema Description
{
  "language": "language using 2 characters ISO-639-1-Codes",
  "file": "string, non-empty — path to the scratchpad file the post was written to"
}

# Example Schema Output in English
<example>
{
  "language": "en",
  "file": ".claude/skills/write-linkedin-post/scratchpad/introduction-to-subagents.md"
}
</example>

# Example Schema Output in German
<example>
{
  "language": "de",
  "file": ".claude/skills/write-linkedin-post/scratchpad/einfuehrung-in-subagenten.md"
}
</example>

# Markdown MUST be avoided in the output

DO NOT use a markdown code block around the curly brackets of the JSON object. DO NOT return markdown text. Return only the single raw JSON object. Start with a { and end with a }
<example>
{ json }
</example>
