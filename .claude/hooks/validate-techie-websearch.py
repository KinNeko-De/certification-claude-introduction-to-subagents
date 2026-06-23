import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def scan_transcript(path: Path) -> tuple[bool, list[str]]:
    log_lines = [f"transcript: {path}"]
    if not path.exists():
        log_lines.append("transcript file not found")
        return False, log_lines
    assistant_count = 0
    try:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    entry = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "assistant":
                    continue
                assistant_count += 1
                content = entry.get("message", {}).get("content", [])
                tool_names = [b["name"] for b in content if b.get("type") == "tool_use" and "name" in b]
                if tool_names:
                    log_lines.append(f"  assistant msg #{assistant_count}: tool_use={tool_names}")
                    if "WebSearch" in tool_names:
                        log_lines.append("    → WebSearch FOUND")
                        return True, log_lines
                else:
                    log_lines.append(f"  assistant msg #{assistant_count}: no tool_use")
    except Exception as exc:
        log_lines.append(f"exception during scan: {exc}")
        return False, log_lines
    log_lines.append(f"scanned {assistant_count} assistant messages — WebSearch not found")
    return False, log_lines


def write_debug(payload, log_lines: list[str], result: str):
    debug_dir = Path(__file__).parent / "debuglogs"
    agent_id = payload.get("agent_id", "unknown")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    debug_file = debug_dir / f"validate-techie-websearch-{agent_id}-{timestamp}.txt"
    timestamp = datetime.now(timezone.utc).isoformat()
    with open(debug_file, "w", encoding="utf-8") as f:
        f.write(f"timestamp:        {timestamp}\n")
        f.write(f"agent_type:       {payload.get('agent_type', '')}\n")
        f.write(f"agent_id:         {agent_id}\n")
        f.write(f"stop_hook_active: {payload.get('stop_hook_active', False)}\n")
        f.write(f"\nresult: {result}\n")
        if log_lines:
            f.write("\n--- transcript scan ---\n")
            f.write("\n".join(log_lines) + "\n")


def log_failure(payload, reason: str):
    log_file = Path(__file__).parent / "debuglogs" / "techie-websearch-failures.jsonl"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_type": payload.get("agent_type", "unknown"),
        "agent_id": payload.get("agent_id", "unknown"),
        "attempt": "retry" if payload.get("stop_hook_active") else "first",
        "violations": [reason],
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


try:
    payload = json.loads(sys.stdin.buffer.read().decode("utf-8"))

    if not payload.get("agent_type"):
        sys.exit(0)

    transcript_path = payload.get("agent_transcript_path", "")
    if not transcript_path:
        log_failure(payload, "agent_transcript_path missing — WebSearch check skipped.")
        sys.exit(0)

    found, log_lines = scan_transcript(Path(transcript_path))

    if found:
        write_debug(payload, log_lines, "PASS — WebSearch was called")
        sys.exit(0)

    write_debug(payload, log_lines, "FAIL — WebSearch was not called")
    log_failure(payload, "WebSearch was not called.")

    if payload.get("stop_hook_active"):
        sys.exit(0)

    sys.stderr.reconfigure(encoding="utf-8")
    sys.stderr.write(
        "You did not use WebSearch.\n"
        "You must call WebSearch to verify current information before responding.\n"
        "Repeat your analysis and call WebSearch with a suitable search term.\n"
    )
    sys.exit(2)
except SystemExit:
    raise
except Exception as e:
    error_file = Path(__file__).parent / "debuglogs" / f"validate-techie-websearch-error-{uuid.uuid4()}.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(str(e))
