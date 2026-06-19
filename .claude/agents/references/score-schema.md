# Schema Description
{
  "emotion": {
    "score": "integer 1-10",
    "reason": "string, non-empty"
  },
  "clarity": {
    "score": "integer 1-10",
    "reason": "string, non-empty"
  },
  "benefits": {
    "score": "integer 1-10",
    "reason": "string, non-empty"
  },
  "overall": {
    "score": "integer 1-10",
    "passed": "boolean — true if overall score >= 7",
    "feedback": "string, non-empty — actionable feedback for the writer; null if passed"
  }
}

# Example Schema Output — Post Passed

<example>
{
  "emotion": {
    "score": 8,
    "reason": "Opens with a relatable scenario that makes the reader feel understood before presenting the main point."
  },
  "clarity": {
    "score": 7,
    "reason": "Short sentences and plain language throughout; one paragraph slips into jargon but does not derail the post."
  },
  "benefits": {
    "score": 8,
    "reason": "Concrete outcome stated in the second paragraph with a specific before/after comparison."
  },
  "overall": {
    "score": 8,
    "passed": true,
    "feedback": null
  }
}
</example>

# Example Schema Output — Post Did Not Pass

<example>
{
  "emotion": {
    "score": 4,
    "reason": "Jumps straight into the product claim without grounding the reader in a relatable situation first."
  },
  "clarity": {
    "score": 5,
    "reason": "Several sentences exceed 25 words and the second paragraph uses three industry acronyms without explanation."
  },
  "benefits": {
    "score": 6,
    "reason": "Benefits are mentioned but stay abstract — no concrete numbers or specific outcomes are provided."
  },
  "overall": {
    "score": 5,
    "passed": false,
    "feedback": "Start with a one- or two-sentence story or observation the reader can recognise from their own experience. Cut any sentence longer than 20 words in half. Replace the acronyms with plain descriptions. In the benefits section, add at least one concrete number or specific real-world outcome."
  }
}
</example>

# Markdown MUST be avoided in the output

DO NOT use a markdown code block around the curly brackets of the JSON object. DO NOT return markdown text. Return only the single raw JSON object.
<example>
```json
{ json }
```
</example>
