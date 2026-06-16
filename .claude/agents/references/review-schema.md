# Schema Description
{
  "language": "language using 2 characters ISO-639-1-Codes"
  "first_impression": "string, non-empty",
  "credibility_score": "null or integer 1-10 (only the techie persona fills this; others use null)",
  "credibility_comment": "string, non-empty",
  "relevance": "integer 1-10",
  "reaction": "null or one of the post reactions",
  "comment": "null or string",
  "verdict": "string, non-empty",
  "sources": "null or array of strings — each entry starts with [N] matching an inline reference used in the comment field, e.g. '[1] https://...'"
}

# Example Schema Output in English (no WebSearch used)
{
  "language": "en"
  "first_impression": "Yet another article about the supposed disruption caused by AI that completely ignores the actual risks and makes me want to scroll past it right away.",
  "credibility_score": null,
  "credibility_comment": "The author speaks from a naive perspective that completely ignores the critical security, privacy, and sovereignty issues surrounding AI-driven software development—this is not a well-informed technical discussion, but rather techno-optimism without substance.",
  "relevance": 3,
  "reaction": null,
  "comment": null,
  "verdict": "From a professional standpoint, this article is completely useless for my consultations with politicians. The author completely fails to recognize that this AI automation poses massive data protection risks—who controls what data the AI systems process? Which datasets are being misused for training?",
  "sources": null
}

# Example Schema Output in German (no WebSearch used)
{
  "language": "de"
  "first_impression": "Ein weiterer Beitrag über die vermeintliche Disruption durch KI, der die tatsächlichen Risiken völlig ausblendet und mich sofort zum Weiterscrollen bewegt.",
  "credibility_score": null,
  "credibility_comment": "Der Autor spricht aus einer naiven Perspektive, die die kritischen Sicherheits-, Datenschutz- und Souveränitätsaspekte der KI-gestützten Softwareentwicklung vollständig ignoriert – das ist keine fundierte fachliche Auseinandersetzung, sondern Techno-Optimismus ohne Substanz.",
  "relevance": 3,
  "reaction": null,
  "comment": null,
  "verdict": "Dieser Beitrag ist aus meiner beruflichen Sicht völlig unbrauchbar für meine Beratungsgespräche mit Politikern. Der Autor verkennt völlig, dass mit dieser KI-Automatisierung massive Datenschutzrisiken entstehen – wer kontrolliert, welche Daten die KI-Systeme verarbeiten? Welche Datensätze werden für das Training missbraucht?",
  "sources": null
}

# Example Schema Output with WebSearch citations
{
  "language": "en",
  "first_impression": "Interesting claim about Rust adoption — worth reading to see if the numbers hold up.",
  "credibility_score": 7,
  "credibility_comment": "The author's numbers broadly align with recent survey data, though the conclusion overstates the trend.",
  "relevance": 7,
  "reaction": "thumps_up",
  "comment": "Stack Overflow's 2024 survey puts Rust adoption at 12% among professional developers [1] — impressive, but still niche. Enterprise blockers are real though [2].",
  "verdict": "Solid post with a real signal behind it. The author could have gone deeper on the enterprise adoption blockers.",
  "sources": [
    "[1] https://survey.stackoverflow.co/2024/technology#admired-and-desired",
    "[2] https://www.infoq.com/news/2024/01/rust-enterprise-adoption/"
  ]
}

# Point you MUST avoid in the Schema Output

- Do not use markdown code block around the JSON object. Bad Example:
```json
{ json }
```

# What is a post reaction?

A post reaction is something that you CAN add to a post. You do not have to react on a post.

# Possible post reactions

| Reaction | When you should use it |
|----------|------------------------|
| null     | - you disagree to the author <br> - the quality of the post is low <br> - the author is wrong, comment the post instead |
| thumps_up | - you agree to the author, but the post does not sweep you off your feet |
| applause | - you strongly agree to the author, the post sweep you off your feet |
| support_it | - you strongly agree to the author and you want the same thing |
| funny | - the post is funny |