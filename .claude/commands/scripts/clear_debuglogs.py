import glob
import os

log_dir = ".claude/hooks/debuglogs"
extensions = ["*.json", "*.jsonl"]

files = [f for ext in extensions for f in glob.glob(os.path.join(log_dir, ext))]

if not files:
    print("No log files found.")
else:
    for f in files:
        os.remove(f)
    print(f"Deleted {len(files)} log file(s).")
