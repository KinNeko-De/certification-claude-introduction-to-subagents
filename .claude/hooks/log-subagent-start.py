import json
import sys
from pathlib import Path

try:
    payload = json.load(sys.stdin)
    log_file = Path(__file__).parent / "debuglogs" / "SubagentStart.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / "hook-error.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
