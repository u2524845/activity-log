#!/usr/bin/env python3
"""
Auto-commit script to keep GitHub activity green.
Runs every hour, makes a small change, commits and pushes.

Setup:
  1. Make sure this repo has a remote origin set.
  2. Run once manually to verify it works: python3 auto_commit.py
  3. Schedule with cron (see bottom of this file).
"""

import subprocess
import datetime
import os
import sys

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
ACTIVITY_FILE = os.path.join(REPO_PATH, "activity_log.txt")


def run(cmd: list[str]) -> tuple[int, str]:
    result = subprocess.run(cmd, cwd=REPO_PATH, capture_output=True, text=True)
    return result.returncode, result.stdout.strip() or result.stderr.strip()


def auto_commit():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append a timestamp line to the activity log
    with open(ACTIVITY_FILE, "a") as f:
        f.write(f"{now}\n")

    # Stage
    code, out = run(["git", "add", ACTIVITY_FILE])
    if code != 0:
        print(f"[ERROR] git add failed: {out}")
        sys.exit(1)

    # Commit
    code, out = run(["git", "commit", "-m", f"chore: activity update {now}"])
    if code != 0:
        print(f"[ERROR] git commit failed: {out}")
        sys.exit(1)

    # Push
    code, out = run(["git", "push"])
    if code != 0:
        print(f"[ERROR] git push failed: {out}")
        sys.exit(1)

    print(f"[OK] Committed and pushed at {now}")


if __name__ == "__main__":
    auto_commit()


# -------------------------------------------------------------------
# CRON SETUP (run every hour):
#
#   Open crontab editor:
#     crontab -e
#
#   Add this line (replace the path with your actual Python + script path):
#     0 * * * * /usr/bin/python3 /Users/akashkumarvanzara/Projects/6march2026/auto_commit.py >> /tmp/auto_commit.log 2>&1
#
#   Save and exit. Verify with:
#     crontab -l
# -------------------------------------------------------------------
