import glob
import os

log_dir = ".claude/hooks/debuglogs"
pattern = os.path.join(log_dir, "*.json")
files = glob.glob(pattern)

if not files:
    print("No log files found.")
else:
    for f in files:
        os.remove(f)
    print(f"Deleted {len(files)} log file(s).")
