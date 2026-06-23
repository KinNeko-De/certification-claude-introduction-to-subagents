import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

try:
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    session_id = payload.get("session_id", "unknown-session")
    agent_id = payload.get("agent_id", "unknown-agent")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_file = Path(__file__).parent / "debuglogs" / f"SubagentStart-{session_id}-{agent_id}-{timestamp}.json"
    with open(log_file, "w", encoding="utf-8", errors="replace") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"subagent-start-hook-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
