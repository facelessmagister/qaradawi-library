#!/usr/bin/env python3
"""
download_book.py — Download books from Archive.org

Usage:
    python3 download_book.py --book halal-haram
    python3 download_book.py --all
    python3 download_book.py --list
"""
import argparse
import hashlib
import os
import subprocess
import sys
import urllib.request
import json
import yaml

WIKI_ROOT = "/root/qaradawi-library"
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "books.yaml")
PDF_DIR = os.path.join(WIKI_ROOT, "raw", "pdfs")
LOG_PATH = os.path.join(WIKI_ROOT, "log.md")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f, sort_keys=False, allow_unicode=True)


def get_metadata(archive_id):
    url = f"https://archive.org/metadata/{archive_id}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"ERROR: Failed to fetch metadata for {archive_id}: {e}")
        return None


def find_best_file(metadata, preferred_format):
    files = metadata.get("files", [])
    candidates = []
    for f in files:
        name = f.get("name", "")
        fmt = f.get("format", "")
        size = f.get("size", 0)
        # Skip tiny files and derivatives
        if int(size) < 10000:
            continue
        if preferred_format.lower() in fmt.lower():
            candidates.append((name, int(size), fmt))
    if not candidates:
        return None
    # Prefer largest file matching the format
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def download_file(archive_id, filename, dest_path):
    url = f"https://archive.org/download/{archive_id}/{filename}"
    print(f"  Downloading: {url}")
    print(f"  Destination: {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def verify_download(dest_path, min_size=10000):
    if not os.path.exists(dest_path):
        return False
    size = os.path.getsize(dest_path)
    if size < min_size:
        print(f"  WARNING: File too small ({size} bytes), likely failed")
        return False
    return True


def append_log(action, details):
    today = "2026-05-16"  # Will be replaced with actual date in production
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## [{today}] {action}\n"
    for k, v in details.items():
        entry += f"- {k}: {v}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)


def download_book(slug, cfg_data):
    books = cfg_data.get("books", {})
    if slug not in books:
        print(f"ERROR: Book '{slug}' not found in registry")
        return False

    book = books[slug]
    if book.get("downloaded"):
        print(f"Book '{slug}' already downloaded. Use --force to re-download.")
        return True

    archive_id = book["archive_id"]
    preferred = book.get("preferred_format", "Text PDF")

    print(f"Downloading: {book['title']}")
    print(f"  Archive ID: {archive_id}")
    print(f"  Preferred format: {preferred}")

    metadata = get_metadata(archive_id)
    if not metadata:
        return False

    filename = find_best_file(metadata, preferred)
    if not filename:
        # Fallback: try any PDF
        filename = find_best_file(metadata, "PDF")
    if not filename:
        print("  ERROR: No suitable PDF file found in Archive.org metadata")
        return False

    print(f"  Selected file: {filename}")

    dest = os.path.join(PDF_DIR, f"{slug}.pdf")
    os.makedirs(PDF_DIR, exist_ok=True)

    success = download_file(archive_id, filename, dest)
    if not success:
        return False

    if not verify_download(dest):
        os.remove(dest)
        return False

    # Update config
    book["downloaded"] = True
    from datetime import datetime
    book["downloaded_at"] = datetime.now().strftime("%Y-%m-%d")
    book["pdf_filename"] = filename
    book["pdf_size"] = os.path.getsize(dest)
    save_config(cfg_data)

    append_log("download", {
        "book": book["title"],
        "slug": slug,
        "file": filename,
        "size": book["pdf_size"],
    })

    print(f"  SUCCESS: Downloaded to {dest}")
    return True


def list_books(cfg_data):
    books = cfg_data.get("books", {})
    print(f"{'Slug':<30} {'Title':<45} {'Priority':<8} {'Status':<12}")
    print("-" * 100)
    for slug, book in sorted(books.items(), key=lambda x: x[1].get("priority", 99)):
        status = "✅" if book.get("downloaded") else "⬜"
        print(f"{slug:<30} {book['title']:<45} {book.get('priority','-'):<8} {status}")


def main():
    parser = argparse.ArgumentParser(description="Download Qaradawi books from Archive.org")
    parser.add_argument("--book", help="Book slug to download")
    parser.add_argument("--all", action="store_true", help="Download all undownloaded books")
    parser.add_argument("--list", action="store_true", help="List all books in registry")
    parser.add_argument("--force", action="store_true", help="Re-download even if already downloaded")
    args = parser.parse_args()

    cfg = load_config()

    if args.list:
        list_books(cfg)
        return

    if args.all:
        books = cfg.get("books", {})
        for slug, book in sorted(books.items(), key=lambda x: x[1].get("priority", 99)):
            if not book.get("downloaded") or args.force:
                download_book(slug, cfg)
        return

    if args.book:
        download_book(args.book, cfg)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
