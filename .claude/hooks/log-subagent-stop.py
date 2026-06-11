import json
import sys
import uuid
from pathlib import Path

try:
    payload = json.load(sys.stdin)

    session_id = payload.get("session_id", "unknown-session")
    agent_id = payload.get("agent_id", "unknown-agent")
    log_file = Path(__file__).parent / "debuglogs" / f"SubagentStop-{session_id}-{agent_id}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"subagent-stop-hook-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
