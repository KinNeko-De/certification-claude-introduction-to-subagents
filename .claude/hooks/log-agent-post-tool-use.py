import json
import sys
import uuid
from pathlib import Path

try:
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    tool_use_id = payload.get("tool_use_id", uuid.uuid4())
    session_id = payload.get("session_id", "unknown-session")
    log_file = Path(__file__).parent / "debuglogs" / f"AgentPostToolUse-{session_id}-{tool_use_id}.json"
    with open(log_file, "w", encoding="utf-8", errors="replace") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"log-agent-post-tool-use-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
