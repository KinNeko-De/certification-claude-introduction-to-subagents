# Schema Description
{
  "language": "language using 2 characters ISO-639-1-Codes"
  "first_impression": "string, non-empty",
  "credibility": "string, non-empty",
  "relevance": "integer 1-10",
  "reaction": "null or one of: \\"Daumen hoch\\", \\"Gefällt mir\\", \\"Unterstütze ich\\", \\"Witzig\\"",
  "comment": "null or string",
  "verdict": "string, non-empty"
}

# Example Output in English
{
  "language": "en"
  "first_impression": "Yet another article about the supposed disruption caused by AI that completely ignores the actual risks and makes me want to scroll past it right away.",
  "credibility": "The author speaks from a naive perspective that completely ignores the critical security, privacy, and sovereignty issues surrounding AI-driven software development—this is not a well-informed technical discussion, but rather techno-optimism without substance.",
  "relevance": 3,
  "reaction": null,
  "comment": null,
  "verdict": "From a professional standpoint, this article is completely useless for my consultations with politicians. The author completely fails to recognize that this AI automation poses massive data protection risks—who controls what data the AI systems process? Which datasets are being misused for training?"
}


# Example Output in German
{
  "language": "en"
  "first_impression": "Ein weiterer Beitrag über die vermeintliche Disruption durch KI, der die tatsächlichen Risiken völlig ausblendet und mich sofort zum Weiterscrollen bewegt.",
  "credibility": "Der Autor spricht aus einer naiven Perspektive, die die kritischen Sicherheits-, Datenschutz- und Souveränitätsaspekte der KI-gestützten Softwareentwicklung vollständig ignoriert – das ist keine fundierte fachliche Auseinandersetzung, sondern Techno-Optimismus ohne Substanz.",
  "relevance": 3,
  "reaction": null,
  "comment": null,
  "verdict": "Dieser Beitrag ist aus meiner beruflichen Sicht völlig unbrauchbar für meine Beratungsgespräche mit Politikern. Der Autor verkennt völlig, dass mit dieser KI-Automatisierung massive Datenschutzrisiken entstehen – wer kontrolliert, welche Daten die KI-Systeme verarbeiten? Welche Datensätze werden für das Training missbraucht?"
}

# Point you MUST avoid
- Do not use markdown code block around the JSON object. Negativ Example:
```json
{ JSON object }
```
