#!/usr/bin/env python3
import os
import re
from datetime import datetime

SRC = os.environ["KINDLE_CLIPPINGS_SRC"]
DEST_BASE = os.environ["KINDLE_DEST_BASE"]
DEST_NAME = os.environ["KINDLE_DEST_NAME"]

TYPE_RE = re.compile(r"Your (Highlight|Note|Bookmark)", re.IGNORECASE)
LOC_RE = re.compile(r"location (\d+)(?:-(\d+))?", re.IGNORECASE)
PAGE_RE = re.compile(r"page (\d+)(?:-(\d+))?", re.IGNORECASE)
DATE_RE = re.compile(r"Added on (.+?)\s*$", re.IGNORECASE)


def parse(raw):
    entries = []
    for block in raw.split("=========="):
        lines = [l.replace("﻿", "").rstrip("\r") for l in block.split("\n")]
        while lines and lines[0].strip() == "":
            lines.pop(0)
        while lines and lines[-1].strip() == "":
            lines.pop()
        if len(lines) < 2:
            continue
        tm = TYPE_RE.search(lines[1])
        if not tm:
            continue
        lm = LOC_RE.search(lines[1])
        pm = PAGE_RE.search(lines[1])
        start = int(lm.group(1)) if lm else None
        end = int(lm.group(2)) if lm and lm.group(2) else start
        page = None
        if pm:
            page = pm.group(1) if not pm.group(2) or pm.group(2) == pm.group(1) else f"{pm.group(1)}-{pm.group(2)}"
        dm = DATE_RE.search(lines[1])
        text_lines = lines[2:]
        while text_lines and text_lines[0].strip() == "":
            text_lines.pop(0)
        entries.append({
            "book": lines[0].strip(),
            "type": tm.group(1).lower(),
            "start": start,
            "end": end,
            "page": page,
            "date": dm.group(1) if dm else None,
            "text": "\n".join(text_lines).strip(),
            "notes": [],
        })
    return entries


def pair(entries):
    highlights = [e for e in entries if e["type"] == "highlight" and e["start"] is not None]
    consumed = set()
    for n in (e for e in entries if e["type"] == "note" and e["start"] is not None):
        for h in highlights:
            if h["book"] == n["book"] and h["start"] <= n["start"] <= h["end"]:
                h["notes"].append(n)
                consumed.add(id(n))
                break
    return consumed


def render(e):
    meta = [e["book"]]
    if e["page"]:
        meta.append(f"page {e['page']}")
    if e["start"] is not None:
        loc = f"{e['start']}-{e['end']}" if e["end"] != e["start"] else str(e["start"])
        meta.append(f"location {loc}")
    if e["date"]:
        meta.append(e["date"])

    parts = ["  \n".join(meta)]
    if e["text"]:
        parts.append("\n".join("> " + l for l in e["text"].split("\n")))
    for n in e["notes"]:
        parts.append(n["text"])
    return "\n\n".join(parts)


def main():
    with open(SRC, encoding="utf-8") as f:
        entries = parse(f.read())
    consumed = pair(entries)
    blocks = [render(e) for e in entries if not (e["type"] == "note" and id(e) in consumed)]

    now = datetime.now()
    head = (
        f"Created: {now:%Y-%m-%d %H:%M}\n"
        "Tags: #resource #kindle-clippings\n\n"
        "---\n## Action\n\n- [ ] read and process\n\n---\n\n"
    )
    content = head + "\n\n---\n\n".join(blocks) + "\n"

    dest = os.path.join(DEST_BASE, f"{DEST_NAME} {now.year}.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Synced clippings to {dest}")


if __name__ == "__main__":
    main()
