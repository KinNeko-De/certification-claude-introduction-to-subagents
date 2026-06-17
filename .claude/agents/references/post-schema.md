# Schema Description
{
  "language": "language using 2 characters ISO-639-1-Codes",
  "linkedin_post": "string, non-empty — the full LinkedIn post text, including line breaks, hashtags and emojis"
}

# Example Schema Output in English
<example>
{
  "language": "en",
  "linkedin_post": "Subagents in Claude Code: a brief operational overview.\n\nThis post documents the standard procedure for delegating tasks to subagents within Claude Code.\n\nKey points to note:\n- Subagents operate within a defined scope of responsibility.\n- Each subagent returns its output in the prescribed format.\n- Coordination is handled by the orchestrating process.\n\nFurther documentation is available upon request.\n\n#ClaudeCode #Subagents #ProcessDocumentation #Automation"
}
</example>

# Example Schema Output in German
<example>
{
  "language": "de",
  "linkedin_post": "Subagenten in Claude Code: eine kurze betriebliche Übersicht.\n\nDieser Beitrag dokumentiert das Standardverfahren zur Delegation von Aufgaben an Subagenten innerhalb von Claude Code.\n\nFolgende Punkte sind zu beachten:\n- Subagenten arbeiten innerhalb eines definierten Verantwortungsbereichs.\n- Jeder Subagent gibt sein Ergebnis im vorgeschriebenen Format zurück.\n- Die Koordination erfolgt durch den übergeordneten Prozess.\n\nWeitere Unterlagen werden auf Anfrage zur Verfügung gestellt.\n\n#ClaudeCode #Subagenten #Prozessdokumentation #Automatisierung"
}
</example>

# Markdown MUST be avoided in the output

DO NOT use a markdown code block around the curly brackets of the JSON object. DO NOT return markdown text. Return only the single raw JSON object.
<example>
```json
{ json }
```
</example>
