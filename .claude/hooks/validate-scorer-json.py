import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_REMINDER = """{
  "emotion": { "score": "<integer 1-10>", "reason": "<string>" },
  "clarity": { "score": "<integer 1-10>", "reason": "<string>" },
  "benefits": { "score": "<integer 1-10>", "reason": "<string>" },
  "overall": {
    "score": "<integer 1-10>",
    "passed": "<boolean>",
    "feedback": "<string or null>"
  }
}"""


def validate_dimension(data, key, violations):
    dim = data.get(key)
    if not isinstance(dim, dict):
        violations.append(f"`{key}` must be an object with `score` and `reason`.")
        return
    score = dim.get("score")
    if not isinstance(score, int) or not (1 <= score <= 10):
        violations.append(f"`{key}.score` must be an integer between 1 and 10.")
    reason = dim.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        violations.append(f"`{key}.reason` must be a non-empty string.")


def validate(text):
    violations = []
    try:
        data = json.loads(text.strip())
    except json.JSONDecodeError as e:
        violations.append(
            f"The response is not a pure JSON object ({e})."
            " DO NOT place a markdown codeblock before or after the JSON."
            " (This is wrong: ```json\n" + SCHEMA_REMINDER + "\n```)."
            " Expected schema:\n" + SCHEMA_REMINDER
        )
        return violations
    if not isinstance(data, dict):
        violations.append("The response must be a single JSON object.")
        return violations

    for dim in ("emotion", "clarity", "benefits"):
        validate_dimension(data, dim, violations)

    overall = data.get("overall")
    if not isinstance(overall, dict):
        violations.append("`overall` must be an object with `score`, `passed`, and `feedback`.")
    else:
        score = overall.get("score")
        if not isinstance(score, int) or not (1 <= score <= 10):
            violations.append("`overall.score` must be an integer between 1 and 10.")
        if not isinstance(overall.get("passed"), bool):
            violations.append("`overall.passed` must be a boolean (true or false).")
        feedback = overall.get("feedback")
        if feedback is not None and (not isinstance(feedback, str) or not feedback.strip()):
            violations.append("`overall.feedback` must be a non-empty string or null.")

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

    if payload.get("stop_hook_active"):
        sys.exit(0)

    sys.stderr.reconfigure(encoding="utf-8")
    sys.stderr.write(
        "Your response failed JSON validation:\n"
        + "".join(f"- {v}\n" for v in violations)
        + "\nRespond again with only a single raw JSON object."
        " DO NOT place a markdown codeblock before or after the JSON."
        " Expected schema:\n" + SCHEMA_REMINDER + "\n"
    )
    sys.exit(2)
except SystemExit:
    raise
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"validate-scorer-json-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
