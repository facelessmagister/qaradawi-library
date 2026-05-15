#!/bin/bash
# cron-backup.sh — Weekly git backup for Qaradawi Library

set -e

WIKI_ROOT="/root/qaradawi-library"
cd "$WIKI_ROOT"

if git diff --quiet && git diff --cached --quiet; then
    echo "$(date -Iseconds) | No changes to commit" >> "$WIKI_ROOT/.stats/backup.log"
    exit 0
fi

git add -A
git commit -m "auto: weekly wiki snapshot $(date +%F_%H-%M)" || true
git push origin main 2>/dev/null || echo "Push failed — remote not configured"

echo "$(date -Iseconds) | Backup committed" >> "$WIKI_ROOT/.stats/backup.log"
