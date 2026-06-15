import json
import sys
import uuid
from pathlib import Path

try:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input", {})
    if tool_input.get("subagent_type") or tool_input.get("prompt"):
        session_id = payload.get("session_id", "unknown-session")
        log_file = Path(__file__).parent / "debuglogs" / f"AgentToolUse-{session_id}-{uuid.uuid4()}.json"
        with open(log_file, "w", encoding="utf-8", errors="replace") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"log-agent-tool-use-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
