import json
import sys
import uuid
from pathlib import Path

try:
    payload = json.load(sys.stdin)

    # I had one time the fact that "last_assistant_message" only contained "Post this to linkedin". But could not reproduce that
    transcript_path = payload.get("agent_transcript_path")
    if transcript_path and Path(transcript_path).exists():
        full_response = None
        with open(transcript_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("type") == "assistant":
                    for block in entry.get("message", {}).get("content", []):
                        if block.get("type") == "text":
                            full_response = block["text"]
        payload["full_assistant_response"] = full_response

    session_id = payload.get("session_id", "unknown-session")
    agent_id = payload.get("agent_id", "unknown-agent")
    log_file = Path(__file__).parent / "debuglogs" / f"SubagentStop-{session_id}-{agent_id}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"subagent-stop-hook-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
