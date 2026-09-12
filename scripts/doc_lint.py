#!/usr/bin/env python3
"""doc_lint.py — structural checks over the project's agent docs (pre-commit gate).

Fails on errors; warnings are reported but do not fail. Checks:
  1. real wiki pages have the required frontmatter fields
  2. ADR filenames match NNNN-title.md and numbers are unique
  3. wiki index lists each real page (warning)
  4. [[wikilinks]] resolve to a page file (warning)
  5. tags used appear in the SCHEMA.md taxonomy (warning)

Excludes *-TEMPLATE* files and index/log/SCHEMA. Usage: doc_lint.py <root>
Exit 0 on success, 1 on error.
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
WIKI = os.path.join(ROOT, "wiki")
ADRS = os.path.join(ROOT, "docs", "adrs")
errors, warnings = [], []
REQUIRED = ["title", "created", "updated", "type", "tags", "sources"]
NONPAGE = {"index.md", "log.md", "schema.md", "readme.md"}

def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, OSError):
        return None

def is_template(fn):
    n = fn.lower()
    return "template" in n or n in NONPAGE

# --- collect real wiki pages ---
pages = {}
if os.path.isdir(WIKI):
    for dp, _, fns in os.walk(WIKI):
        for fn in fns:
            if fn.endswith(".md") and not is_template(fn):
                rel = os.path.relpath(os.path.join(dp, fn), WIKI)
                pages[rel] = os.path.join(dp, fn)

index_text = read(os.path.join(WIKI, "index.md")) or ""
schema_text = read(os.path.join(WIKI, "SCHEMA.md")) or ""
tax_tags = set()
if "## Tag Taxonomy" in schema_text:
    block = schema_text.split("## Tag Taxonomy", 1)[1].split("## ", 1)[0]
    tax_tags = set(re.findall(r"[a-z][a-z0-9-]+", block))

slugs = {os.path.splitext(os.path.basename(r))[0].lower() for r in pages}

for rel, path in sorted(pages.items()):
    text = read(path) or ""
    fm = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r"\s*([a-z_]+):\s*(.*)", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
    for field in REQUIRED:
        if field not in fm:
            errors.append(f"wiki/{rel}: missing frontmatter field '{field}'")
    if os.path.basename(rel) not in index_text:
        warnings.append(f"wiki/{rel}: not listed in wiki/index.md")
    for m in re.findall(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]", text):
        if m.strip().lower() not in slugs:
            warnings.append(f"wiki/{rel}: wikilink [[{m.strip()}]] may not resolve")
    m = re.search(r"tags:\s*\[([^\]]*)\]", text)
    if m and tax_tags:
        for t in (x.strip() for x in m.group(1).split(",")):
            if t and t not in tax_tags:
                warnings.append(f"wiki/{rel}: tag '{t}' not in SCHEMA.md taxonomy")

# --- ADR numbering ---
nums = []
if os.path.isdir(ADRS):
    for fn in sorted(os.listdir(ADRS)):
        m = re.match(r"^(\d{4})-.+\.md$", fn)
        if m:
            nums.append(int(m.group(1)))
        elif fn.endswith(".md") and not is_template(fn):
            warnings.append(f"docs/adrs/{fn}: filename does not match NNNN-title.md")
    if len(nums) != len(set(nums)):
        errors.append(f"docs/adrs: duplicate ADR numbers: {sorted(nums)}")

for w in warnings:
    print("WARN  ", w)
for e in errors:
    print("ERROR ", e)
if errors:
    print(f"\n✗ doc_lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1)
print(f"✓ doc_lint: OK ({len(pages)} wiki page(s), {len(nums)} ADR(s), {len(warnings)} warning(s))")
sys.exit(0)
