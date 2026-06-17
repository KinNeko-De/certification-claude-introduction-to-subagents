import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_REMINDER = """{\
  "language": "2-character ISO-639-1 code, e.g. \\"en\\" or \\"de\\"",
  "linkedin_post": "string, non-empty — the full post text incl. hashtags/emojis"
}"""


def validate(text):
    violations = []
    try:
        data = json.loads(text.strip())
    except json.JSONDecodeError as e:
        violations.append(
            f"The response is not a pure JSON object ({e}). "
            " DO NOT place a markdown codeblock before or after the JSON. (This is wrong: ```json\n" + SCHEMA_REMINDER + "\n```)."
            "Expected schema:\n" + SCHEMA_REMINDER + "\n"
        )
        return violations
    if not isinstance(data, dict):
        violations.append("The response must be a single JSON object.")
        return violations
    language = data.get("language")
    if not isinstance(language, str) or len(language.strip()) != 2:
        violations.append("`language` must be a 2-character ISO-639-1 code (e.g. \"en\", \"de\").")
    linkedin_post = data.get("linkedin_post")
    if not isinstance(linkedin_post, str) or not linkedin_post.strip():
        violations.append("`linkedin_post` must be a non-empty string.")
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
    # Skip validation in that case.
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
        " DO NOT place a markdown codeblock before or after the JSON. (Beispiel: ```json\n" + SCHEMA_REMINDER + "\n```)."
        "Expected schema:\n" + SCHEMA_REMINDER + "\n"
    )
    sys.exit(2)
except SystemExit:
    raise
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"validate-writer-json-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
