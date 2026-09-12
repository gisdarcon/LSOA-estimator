#!/usr/bin/env python3
"""review.py — mechanical half of the human review loop for docs (papers / research).

The human reviews the rendered document, records feedback in REVIEW.md as
anchored comments; the agent reads REVIEW.md, addresses the open comments, and
marks them resolved. This script is the *mechanical* part of that loop:

  - validates the REVIEW.md schema (unique IDs, legal severity/status),
  - checks that every comment's anchor marker still resolves in a .qmd source,
  - reports the convergence count (open comments, blockers still open).

Design choice (intentional): in default mode this NEVER blocks — it always
exits 0, so the pre-commit gate shows the open count as information without
refusing a commit while a doc is still under review. Run with --check to get a
hard "is it review-clean?" signal (exit 1 if any comment is still open).

Anchor convention: each comment names an HTML comment dropped into the source
at the exact spot, e.g.  <!-- review:R012 -->  . Invisible when rendered,
stable across edits, and greppable. `review.py` searches all *.qmd files.

Usage: review.py [root] [--check]
"""
import glob, os, re, sys

args = [a for a in sys.argv[1:]]
CHECK = "--check" in args
args = [a for a in args if a != "--check"]
ROOT = args[0] if args else "."

REVIEW = os.path.join(ROOT, "REVIEW.md")
VALID_SEV = {"blocker", "major", "minor", "question"}
VALID_STATUS = {"open", "resolved", "rejected"}

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, OSError):
        return None

# --- load the review file ---
text = read(REVIEW)
if text is None:
    print("· review: no REVIEW.md — nothing to review")
    sys.exit(0)

# --- collect anchor markers from all .qmd sources ---
anchor_hay = []
for qmd in sorted(glob.glob(os.path.join(ROOT, "**", "*.qmd"), recursive=True)):
    t = read(qmd)
    if t:
        anchor_hay.append((os.path.relpath(qmd, ROOT), t))
hay = "\n".join(t for _, t in anchor_hay)

# --- parse comments: '## RNNN' blocks of '- key: value' ---
comments = []
cur = None
for line in text.splitlines():
    m = re.match(r"^##\s+(R[0-9]{3,})\s*$", line)
    if m:
        cur = {"id": m.group(1), "fields": {}}
        comments.append(cur)
        continue
    if re.match(r"^##\s", line) and cur:      # a non-comment heading ends the block
        cur = None
        continue
    if cur is None:
        continue
    kv = re.match(r"^\s*-\s*([a-z]+):\s*(.*)$", line)
    if kv:
        cur["fields"][kv.group(1)] = kv.group(2).strip()

# --- validate ---
problems = []
ids = [c["id"] for c in comments]
if len(ids) != len(set(ids)):
    problems.append(f"duplicate comment IDs: {sorted(set(i for i in ids if ids.count(i) > 1))}")

for c in comments:
    cid = c["id"]
    sev = c["fields"].get("severity", "")
    status = c["fields"].get("status", "")
    anchor = c["fields"].get("anchor", "")
    if sev and sev not in VALID_SEV:
        problems.append(f"{cid}: illegal severity '{sev}' (want one of {sorted(VALID_SEV)})")
    if status and status not in VALID_STATUS:
        problems.append(f"{cid}: illegal status '{status}' (want one of {sorted(VALID_STATUS)})")
    if anchor and anchor != "none" and anchor not in hay:
        # A resolved/rejected comment's anchor is expected to be gone (the agent
        # removes it when applying the fix), so only an OPEN comment's missing
        # anchor is worth flagging.
        if status in ("", "open"):
            problems.append(f"{cid}: anchor not found in any .qmd: {anchor}")

# --- report ---
open_c = [c for c in comments if c["fields"].get("status", "open") == "open"]
blockers = [c for c in open_c if c["fields"].get("severity") == "blocker"]

print(f"→ review: {len(comments)} comment(s), {len(open_c)} open, {len(blockers)} open blocker(s)")
for c in open_c:
    sev = c["fields"].get("severity", "?")
    note = c["fields"].get("note", "")
    mark = "⛔" if sev == "blocker" else "· "
    print(f"  {mark} {c['id']} [{sev}] {note}")
for p in problems:
    print(f"  WARN  review: {p}")

if problems:
    print(f"✗ review: {len(problems)} schema/anchor issue(s) (non-blocking)")
elif not comments:
    print("✓ review: REVIEW.md present, no comments yet")
else:
    print("✓ review: no open comments — doc is review-clean" if not open_c
          else f"✓ review: {len(open_c)} open comment(s) (non-blocking)")

# default mode: never block. --check: hard gate on open comments.
if CHECK and open_c:
    sys.exit(1)
sys.exit(0)
