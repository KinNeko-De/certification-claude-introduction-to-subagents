import json
import sys
import uuid
from pathlib import Path

try:
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    tool_input = payload.get("tool_input", {})
    if tool_input.get("subagent_type") or tool_input.get("prompt"):
        session_id = payload.get("session_id", "unknown-session")
        log_file = Path(__file__).parent / "debuglogs" / f"AgentPreToolUse-{session_id}-{uuid.uuid4()}.json"
        with open(log_file, "w", encoding="utf-8", errors="replace") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"log-agent-pre-tool-use-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
