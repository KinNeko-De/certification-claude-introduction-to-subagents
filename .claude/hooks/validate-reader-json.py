import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ALLOWED_REACTIONS = {"Daumen hoch", "Gefällt mir", "Unterstütze ich", "Witzig"}

SCHEMA_REMINDER = """{
  "first_impression": "string, non-empty",
  "credibility": "string, non-empty",
  "relevance": "integer 1-10",
  "reaction": "null or one of: \\"Daumen hoch\\", \\"Gefällt mir\\", \\"Unterstütze ich\\", \\"Witzig\\"",
  "comment": "null or string",
  "verdict": "string, non-empty"
}"""


def validate(text):
    violations = []
    try:
        data = json.loads(text.strip())
    except json.JSONDecodeError as e:
        violations.append(
            f"The response is not a pure JSON object ({e}). "
            "No markdown code block, no text before or after the JSON."
        )
        return violations
    if not isinstance(data, dict):
        violations.append("The response must be a single JSON object.")
        return violations
    for field in ("first_impression", "credibility", "verdict"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            violations.append(f"`{field}` must be a non-empty string.")
    relevance = data.get("relevance")
    if not isinstance(relevance, int) or isinstance(relevance, bool) or not 1 <= relevance <= 10:
        violations.append("`relevance` must be an integer between 1 and 10.")
    reaction = data.get("reaction")
    if reaction is not None and reaction not in ALLOWED_REACTIONS:
        violations.append(
            "`reaction` must be null or one of: "
            '"Daumen hoch", "Gefällt mir", "Unterstütze ich", "Witzig".'
        )
    comment = data.get("comment")
    if comment is not None and not isinstance(comment, str):
        violations.append("`comment` must be null or a string.")
    return violations


def log_failure(payload, violations, output):
    log_file = Path(__file__).parent / "debuglogs" / "validation-failures.jsonl"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_type": payload.get("agent_type", "unknown-agent-type"),
        "agent_id": payload.get("agent_id", "unknown-agent"),
        "attempt": "retry" if payload.get("stop_hook_active") else "first",
        "violations": violations,
        "output": output,
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


try:
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))

    # SubagentStop also fires for the main orchestrator, which has an empty agent_type.
    # The matcher in settings.json does not filter this case, so we skip validation here.
    if not payload.get("agent_type"):
        sys.exit(0)

    message = payload.get("last_assistant_message")
    if message is None:
        log_failure(payload, ["last_assistant_message missing from hook payload — validation skipped."], None)
        sys.exit(0)

    violations = validate(message)
    if not violations:
       sys.exit(0)

    log_failure(payload, violations, message)

    # Workaround so we do not need to track the state of retries. First time this is false, second time this is true
    if payload.get("stop_hook_active"):
        # Already retried once — give up and let the skill handle the raw response.
        sys.exit(0)

    sys.stderr.reconfigure(encoding="utf-8")
    sys.stderr.write(
        "Your response failed JSON validation:\n"
        + "".join(f"- {v}\n" for v in violations)
        + "\nRespond again with only a single raw JSON object"
        " — no markdown code block, no text before or after. Expected schema:\n"
        + SCHEMA_REMINDER + "\n"
    )
    sys.exit(2)
except SystemExit:
    raise
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"validate-reader-json-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
