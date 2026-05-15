#!/usr/bin/env python3
"""
cross_reference.py — Add cross-links between related pages and identify contradictions

Usage:
    python3 cross_reference.py
    python3 cross_reference.py --fix-orphans
"""
import argparse
import os
import re
import yaml
from collections import defaultdict
from datetime import datetime

WIKI_ROOT = "/root/qaradawi-library"
ENTITIES_DIR = os.path.join(WIKI_ROOT, "entities")
CONCEPTS_DIR = os.path.join(WIKI_ROOT, "concepts")
COMPARISONS_DIR = os.path.join(WIKI_ROOT, "comparisons")
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
    except Exception:
        fm = {}
    return fm, parts[2].strip()


def write_page(path, fm, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(fm, f, allow_unicode=True, sort_keys=False)
        f.write("---\n\n")
        f.write(body)


def extract_wikilinks(text):
    """Extract all [[wikilinks]] from text."""
    pattern = r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]"
    return re.findall(pattern, text)


def get_all_wiki_pages():
    """Get all wiki pages across all directories."""
    pages = []
    for directory in [ENTITIES_DIR, CONCEPTS_DIR, COMPARISONS_DIR]:
        if not os.path.exists(directory):
            continue
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(".md"):
                    pages.append(os.path.join(root, f))
    return pages


def append_log(action, details):
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## [{today}] {action}\n"
    for k, v in details.items():
        entry += f"- {k}: {v}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)


def build_link_graph(pages):
    """Build outbound and inbound link maps."""
    outbound = defaultdict(set)   # page_path -> set of linked targets
    inbound = defaultdict(set)    # target -> set of pages linking to it

    for page_path in pages:
        fm, body = read_page(page_path)
        if body is None:
            continue
        links = extract_wikilinks(body)
        for target, _ in links:
            # target might be a path like "concept-zakat" or "halal-haram-ch-01"
            outbound[page_path].add(target)
            inbound[target].add(page_path)

    return outbound, inbound


def find_orphans(pages, inbound):
    """Find pages with zero inbound links."""
    orphans = []
    for page_path in pages:
        basename = os.path.basename(page_path).replace(".md", "")
        if basename not in inbound or len(inbound[basename]) == 0:
            # Also check if any parent directory + basename is referenced
            rel = os.path.relpath(page_path, WIKI_ROOT).replace(".md", "")
            if rel not in inbound or len(inbound[rel]) == 0:
                orphans.append(page_path)
    return orphans


def find_broken_links(pages, outbound):
    """Find links to non-existent pages."""
    all_basenames = set()
    for page_path in pages:
        basename = os.path.basename(page_path).replace(".md", "")
        all_basenames.add(basename)
        rel = os.path.relpath(page_path, WIKI_ROOT).replace(".md", "")
        all_basenames.add(rel)

    broken = []
    for page_path, targets in outbound.items():
        for target in targets:
            # Target might be relative path or just basename
            if target not in all_basenames:
                # Try to find if it exists in any directory
                found = False
                for directory in [ENTITIES_DIR, CONCEPTS_DIR, COMPARISONS_DIR, "queries"]:
                    check = os.path.join(WIKI_ROOT, directory, f"{target}.md")
                    if os.path.exists(check):
                        found = True
                        break
                if not found:
                    broken.append((page_path, target))
    return broken


def add_missing_links(pages, inbound, outbound):
    """Add bi-directional links between pages sharing concepts."""
    links_added = 0

    # Group chapter pages by concept
    concept_chapters = defaultdict(list)
    for page_path in pages:
        fm, body = read_page(page_path)
        if fm and fm.get("type") == "chapter":
            # Check which concepts this chapter mentions
            for directory in [CONCEPTS_DIR]:
                if not os.path.exists(directory):
                    continue
                for concept_file in os.listdir(directory):
                    if not concept_file.endswith(".md"):
                        continue
                    concept_slug = concept_file.replace(".md", "")
                    if concept_slug in body:
                        concept_chapters[concept_slug].append(page_path)

    # For each concept with 2+ chapters, ensure they link to each other
    for concept_slug, chapter_pages in concept_chapters.items():
        if len(chapter_pages) < 2:
            continue
        for i, page_a in enumerate(chapter_pages):
            for page_b in chapter_pages[i+1:]:
                # Check if page_a links to page_b
                fm_a, body_a = read_page(page_a)
                basename_b = os.path.basename(page_b).replace(".md", "")
                if basename_b not in body_a:
                    # Add link
                    rel_path = os.path.relpath(page_b, os.path.dirname(page_a)).replace(".md", "")
                    body_a += f"\n- See also: [[{rel_path}|{fm_a.get('title', 'Related chapter') if isinstance(fm_a, dict) else 'Related'}]]"
                    fm_a["updated"] = datetime.now().strftime("%Y-%m-%d")
                    write_page(page_a, fm_a, body_a)
                    links_added += 1

    return links_added


def create_orphan_stubs(orphans):
    """Create minimal stubs for orphaned pages to give them at least 1 link."""
    stubs_created = 0
    for orphan_path in orphans:
        fm, body = read_page(orphan_path)
        if not fm:
            continue

        # For concept pages, link to related concepts if any exist
        if fm.get("type") == "concept":
            # Find the book/chapter pages that mention this concept
            for page_path in get_all_wiki_pages():
                _, other_body = read_page(page_path)
                if other_body and os.path.basename(orphan_path).replace(".md", "") in other_body:
                    # Add a back-link to this page
                    rel = os.path.relpath(page_path, os.path.dirname(orphan_path)).replace(".md", "")
                    body += f"\n\n## Referenced By\n\n- [[{rel}]]\n"
                    fm["updated"] = datetime.now().strftime("%Y-%m-%d")
                    write_page(orphan_path, fm, body)
                    stubs_created += 1
                    break

    return stubs_created


def main():
    parser = argparse.ArgumentParser(description="Cross-reference wiki pages")
    parser.add_argument("--fix-orphans", action="store_true", help="Create stubs for orphan pages")
    parser.add_argument("--report-only", action="store_true", help="Only report, don't modify")
    args = parser.parse_args()

    pages = get_all_wiki_pages()
    if not pages:
        print("No wiki pages found.")
        return

    print(f"Scanning {len(pages)} wiki pages...")

    outbound, inbound = build_link_graph(pages)
    orphans = find_orphans(pages, inbound)
    broken = find_broken_links(pages, outbound)

    print(f"\n{'='*60}")
    print("CROSS-REFERENCE REPORT")
    print(f"{'='*60}")
    print(f"Total pages:       {len(pages)}")
    print(f"Total outbound links: {sum(len(v) for v in outbound.values())}")
    print(f"Orphan pages:       {len(orphans)}")
    print(f"Broken links:       {len(broken)}")

    if orphans:
        print(f"\n--- Orphan Pages ({len(orphans)}) ---")
        for o in orphans:
            print(f"  {os.path.relpath(o, WIKI_ROOT)}")

    if broken:
        print(f"\n--- Broken Links ({len(broken)}) ---")
        for page, target in broken[:20]:
            print(f"  {os.path.relpath(page, WIKI_ROOT)} -> [[{target}]]")
        if len(broken) > 20:
            print(f"  ... and {len(broken)-20} more")

    if args.report_only:
        return

    # Add cross-links
    links_added = add_missing_links(pages, inbound, outbound)
    print(f"\nLinks added: {links_added}")

    if args.fix_orphans and orphans:
        stubs = create_orphan_stubs(orphans)
        print(f"Orphan stubs created: {stubs}")

    append_log("cross-ref", {
        "pages_scanned": len(pages),
        "orphans": len(orphans),
        "broken_links": len(broken),
        "links_added": links_added,
    })

    print(f"\nDone. Run `wiki_lint.py` for full health check.")


if __name__ == "__main__":
    main()
