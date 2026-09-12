#!/usr/bin/env python3
"""secret_scan.py — zero-dependency, high-confidence secret detector (pre-commit gate).

A first line of defense so an agent doesn't commit credentials by accident. It is
NOT a full replacement for a scanner like gitleaks — it only flags high-confidence
patterns to keep false positives low.

It scans the files git will commit (the index), so gitignored files — including a
properly-ignored .env — are never flagged and never block a commit. Outside a git
repo (e.g. when a template runs its own check in _templates/) it falls back to a
filesystem walk.

Usage: secret_scan.py <root>. Exit 0 if clean, 1 if a likely secret is found.
"""
import os, re, subprocess, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".hg", ".svn",
             "dist", "build", "target", "vendor", ".cache", ".next", ".nuxt"}
SKIP_FILES = {"secret_scan.py", "doc_lint.py", ".gitignore"}
PATTERNS = [
    (r"-----BEGIN (RSA|EC|DSA|OPENSSH|PGP|ENCRYPTED) PRIVATE KEY-----", "private key block"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS access key ID"),
    (r"(?i)aws_secret_access_key\s*[:=]\s*['\"][A-Z0-9]{40}['\"]", "AWS secret access key"),
    (r"\bghp_[A-Za-z0-9]{36}\b", "GitHub personal access token"),
    (r"\bgho_[A-Za-z0-9]{36}\b", "GitHub OAuth token"),
    (r"\bsk-[A-Za-z0-9]{20,}\b", "OpenAI-style API key"),
]
PLACEHOLDER = re.compile(r"(?i)(xxx|your[_-]|<|example|placeholder|changeme|todo|\.\.\.|dummy|fake|sample)")

hits = []

def git_index_files(root):
    """Return the files in git's index (what will be committed), or None if
    `root` is not inside a git work tree. NUL-safe."""
    try:
        out = subprocess.run(["git", "-C", root, "ls-files", "-z"],
                             capture_output=True, text=True, check=True,
                             timeout=30).stdout
    except (subprocess.SubprocessError, OSError):
        return None
    return [f for f in out.split("\0") if f]

def scan_file(path, rel):
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        return
    if b"\x00" in raw[:8000]:
        return  # binary
    text = raw.decode("utf-8", "ignore")
    for pat, label in PATTERNS:
        for m in re.finditer(pat, text):
            if PLACEHOLDER.search(m.group(0)):
                continue
            line = text[:m.start()].count("\n") + 1
            hits.append((rel, line, label))

# Prefer the git index (respects .gitignore); fall back to a tree walk.
index = git_index_files(ROOT)
if index is not None:
    for rel in index:
        if os.path.basename(rel) in SKIP_FILES or rel.endswith(".gitkeep"):
            continue
        scan_file(os.path.join(ROOT, rel), rel)
else:
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn in SKIP_FILES or fn.endswith(".gitkeep"):
                continue
            path = os.path.join(dp, fn)
            scan_file(path, os.path.relpath(path, ROOT))

if hits:
    for rel, line, label in hits:
        print(f"ERROR secret_scan: {rel}:{line} possible {label}")
    print(f"\n✗ secret_scan: {len(hits)} potential secret(s). Move to a gitignored .env and remove from the file.")
    sys.exit(1)
print("✓ secret_scan: no secrets detected")
sys.exit(0)
