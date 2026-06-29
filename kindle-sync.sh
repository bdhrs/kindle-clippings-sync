#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
set -a
source "$SCRIPT_DIR/kindle-sync.env"
set +a

# udev fires on connect before udisks2 finishes mounting, so wait for the file.
for _ in $(seq 1 30); do
    [[ -f "$KINDLE_CLIPPINGS_SRC" ]] && break
    sleep 1
done

[[ -f "$KINDLE_CLIPPINGS_SRC" ]] || { echo "Kindle clippings not found: $KINDLE_CLIPPINGS_SRC" >&2; exit 1; }

exec python3 "$SCRIPT_DIR/kindle-sync.py"
