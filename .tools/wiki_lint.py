#!/usr/bin/env python3
"""
wiki_lint.py — Full wiki health linter

Usage:
    python3 wiki_lint.py
    python3 wiki_lint.py --fix
"""
import argparse
import os
import re
import yaml
from datetime import datetime
from collections import defaultdict

WIKI_ROOT = "/root/qaradawi-library"
ENTITIES_DIR = os.path.join(WIKI_ROOT, "entities")
CONCEPTS_DIR = os.path.join(WIKI_ROOT, "concepts")
COMPARISONS_DIR = os.path.join(WIKI_ROOT, "comparisons")
QUERIES_DIR = os.path.join(WIKI_ROOT, "queries")
INDEX_PATH = os.path.join(WIKI_ROOT, "index.md")
SCHEMA_PATH = os.path.join(WIKI_ROOT, "SCHEMA.md")
LOG_PATH = os.path.join(WIKI_ROOT, "log.md")


def read_page(path):
    if not os.path.exists(path):
        return None, None
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1])
    except Exception as e:
        print(f"  YAML ERROR in {path}: {e}")
        return {}, content
    return fm, parts[2].strip()


def get_all_wiki_pages():
    pages = []
    for directory in [ENTITIES_DIR, CONCEPTS_DIR, COMPARISONS_DIR, QUERIES_DIR]:
        if not os.path.exists(directory):
            continue
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(".md"):
                    pages.append(os.path.join(root, f))
    return pages


def extract_wikilinks(text):
    pattern = r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]"
    return re.findall(pattern, text)


def load_schema_taxonomy():
    """Extract valid tags from SCHEMA.md."""
    if not os.path.exists(SCHEMA_PATH):
        return set()
    with open(SCHEMA_PATH, "r") as f:
        content = f.read()
    # Find all tags listed in the taxonomy section
    tags = set()
    # Simple heuristic: lines starting with `- <word>` in the Tag Taxonomy section
    in_taxonomy = False
    for line in content.split("\n"):
        if "## Tag Taxonomy" in line:
            in_taxonomy = True
            continue
        if in_taxonomy and line.startswith("## ") and "Tag" not in line:
            break
        if in_taxonomy and line.strip().startswith("- `"):
            # Format: - `tag-name`
            m = re.match(r"\s*-\s*`([^`]+)`", line)
            if m:
                tags.add(m.group(1))
        elif in_taxonomy and line.strip().startswith("-"):
            # Format: - tag-name
            m = re.match(r"\s*-\s*([\w-]+)", line)
            if m:
                tags.add(m.group(1))
    return tags


def lint():
    pages = get_all_wiki_pages()
    if not pages:
        print("No wiki pages to lint.")
        return {}

    schema_tags = load_schema_taxonomy()
    today = datetime.now().strftime("%Y-%m-%d")
    today_dt = datetime.strptime(today, "%Y-%m-%d")

    issues = {
        "critical": [],
        "warning": [],
        "info": [],
    }

    all_basenames = set()
    for p in pages:
        basename = os.path.basename(p).replace(".md", "")
        all_basenames.add(basename)
        rel = os.path.relpath(p, WIKI_ROOT).replace(".md", "")
        all_basenames.add(rel)

    # Build link graph
    inbound = defaultdict(set)
    for p in pages:
        fm, body = read_page(p)
        if body:
            for target, _ in extract_wikilinks(body):
                inbound[target].add(p)

    for page_path in pages:
        fm, body = read_page(page_path)
        rel_path = os.path.relpath(page_path, WIKI_ROOT)
        basename = os.path.basename(page_path).replace(".md", "")

        # 1. Missing frontmatter
        if not fm or not isinstance(fm, dict):
            issues["critical"].append(f"Missing frontmatter: {rel_path}")
            continue

        # 2. Required fields
        required = ["title", "created", "updated", "type", "tags"]
        for field in required:
            if field not in fm:
                issues["critical"].append(f"Missing '{field}' in frontmatter: {rel_path}")

        # 3. Tag validation
        page_tags = fm.get("tags", [])
        if isinstance(page_tags, str):
            page_tags = [page_tags]
        for tag in page_tags:
            if schema_tags and tag not in schema_tags:
                issues["warning"].append(f"Unknown tag '{tag}': {rel_path}")

        # 4. Orphan check
        if basename not in inbound or len(inbound[basename]) == 0:
            # Check relative path too
            rel_no_ext = rel_path.replace(".md", "")
            if rel_no_ext not in inbound or len(inbound[rel_no_ext]) == 0:
                # Exempt index and log
                if basename not in ["index", "log", "SCHEMA", "README", "AGENTS", "CLAUDE"]:
                    issues["warning"].append(f"Orphan page (no inbound links): {rel_path}")

        # 5. Broken outbound links
        if body:
            for target, _ in extract_wikilinks(body):
                if target not in all_basenames:
                    # Check if target exists as file
                    found = False
                    for directory in [ENTITIES_DIR, CONCEPTS_DIR, COMPARISONS_DIR, QUERIES_DIR]:
                        if os.path.exists(os.path.join(directory, f"{target}.md")):
                            found = True
                            break
                        # Try relative path resolution
                        candidate = os.path.join(WIKI_ROOT, f"{target}.md")
                        if os.path.exists(candidate):
                            found = True
                            break
                    if not found:
                        issues["critical"].append(f"Broken link [[{target}]] in: {rel_path}")

        # 6. Minimum outbound links
        if body:
            outbound = extract_wikilinks(body)
            if len(outbound) < 2:
                # Exempt certain page types
                if fm.get("type") not in ["book-overview", "query"]:
                    issues["warning"].append(f"Fewer than 2 outbound links: {rel_path}")

        # 7. Page size
        if body and len(body.split("\n")) > 250:
            issues["info"].append(f"Page exceeds 250 lines: {rel_path}")

        # 8. Arabic diacritics check (heuristic)
        if body and re.search(r'[\u0621-\u064A]', body):
            # Contains Arabic letters — check if key terms have diacritics
            # Very loose check: at least some combining marks present
            if not re.search(r'[\u064B-\u065F]', body):
                issues["info"].append(f"Arabic text without diacritics: {rel_path}")

        # 9. Stale content
        updated = fm.get("updated")
        if updated:
            try:
                updated_dt = datetime.strptime(str(updated), "%Y-%m-%d")
                days_old = (today_dt - updated_dt).days
                if days_old > 90:
                    issues["info"].append(f"Stale (not updated in {days_old} days): {rel_path}")
            except ValueError:
                pass

    # 10. Index completeness
    with open(INDEX_PATH, "r") as f:
        index_content = f.read()
    for p in pages:
        basename = os.path.basename(p).replace(".md", "")
        if f"[[{basename}" not in index_content and basename not in ["index", "log"]:
            issues["warning"].append(f"Not in index.md: {os.path.relpath(p, WIKI_ROOT)}")

    return issues


def print_report(issues):
    print(f"\n{'='*70}")
    print("WIKI LINT REPORT")
    print(f"{'='*70}")

    total = sum(len(v) for v in issues.values())
    print(f"Total issues: {total}")
    print(f"  CRITICAL: {len(issues['critical'])}")
    print(f"  WARNING:  {len(issues['warning'])}")
    print(f"  INFO:     {len(issues['info'])}")

    for severity in ["critical", "warning", "info"]:
        if issues[severity]:
            print(f"\n--- {severity.upper()} ({len(issues[severity])}) ---")
            for issue in issues[severity]:
                print(f"  {issue}")

    # Write summary to log
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## [{today}] lint | {total} issues found\n"
    entry += f"- critical: {len(issues['critical'])}\n"
    entry += f"- warning: {len(issues['warning'])}\n"
    entry += f"- info: {len(issues['info'])}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="Lint the Qaradawi wiki")
    parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix issues")
    args = parser.parse_args()

    issues = lint()
    print_report(issues)

    if args.fix:
        print("\nAuto-fix not yet implemented. Manual fixes required for critical issues.")


if __name__ == "__main__":
    main()
