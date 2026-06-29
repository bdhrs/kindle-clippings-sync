# kindle-clippings-sync

Plug in your Kindle and your highlights and notes get copied to a Markdown file automatically.

It reads `My Clippings.txt` off the Kindle, pairs each note with the passage it was written on, and writes a tidy per-year Markdown file (e.g. `Kindle Clippings 2026.md`). Runs by itself every time you connect the Kindle.

## What you get

Each highlight looks like this:

```
The Example Book (Some Author)
page 42
location 600-601
Monday, 1 January 2024 12:00:00

> A sentence you highlighted in the book.

A note you typed about that sentence.
```

The blockquote is what you highlighted. The plain line under it is the note you typed.

## Requirements

- Linux with systemd and udev (most desktop distros)
- Python 3
- [`just`](https://github.com/casey/just) (only for the one-line install; optional)

## Setup

1. Clone the repo.

2. Copy the config and edit the paths:
   ```
   cp kindle-sync.env.example kindle-sync.env
   ```
   - `KINDLE_CLIPPINGS_SRC` – where the Kindle mounts (check with `lsblk` while it's plugged in)
   - `KINDLE_DEST_BASE` – the folder to write into
   - `KINDLE_DEST_NAME` – the filename prefix (year and `.md` are added automatically)

3. Edit `kindle-sync.service` – set `User=` to your username and the `ExecStart=` path to where you cloned the repo.

4. Edit `99-kindle-sync.rules` if your Kindle isn't an Amazon device with id `1949:0324`. Find yours with `lsusb` (look for Amazon).

5. Install:
   ```
   just install
   ```
   (or do it by hand: copy the `.service` to `/etc/systemd/system/`, the `.rules` to `/etc/udev/rules.d/`, then `sudo systemctl daemon-reload && sudo udevadm control --reload-rules`)

6. Replug the Kindle. The Markdown file appears in your chosen folder.

## Run it manually

```
./kindle-sync.sh
```

## Note

The file is overwritten on every sync, so don't hand-edit it — your changes will be wiped next time you plug in.
