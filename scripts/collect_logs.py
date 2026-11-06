#!/usr/bin/env python3

from pathlib import Path
import csv
from datetime import datetime

SEARCH_ROOT = Path.home()

OUTPUT_DIR = Path("analytics")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "file_inventory.csv"

EXTENSIONS = {
    ".txt",
    ".csv",
    ".log",
    ".ini",
}

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".cache",
    "node_modules",
    ".local/share/Trash",
}


def should_skip(path: Path) -> bool:
    path_str = str(path)

    for excluded in EXCLUDED_DIRS:
        if excluded in path_str:
            return True

    return False


rows = []

print(f"Scanning: {SEARCH_ROOT}")
print()

for file in SEARCH_ROOT.rglob("*"):

    if not file.is_file():
        continue

    if should_skip(file):
        continue

    if file.suffix.lower() not in EXTENSIONS:
        continue

    try:

        stat = file.stat()

        rows.append([
            file.suffix.lower(),
            str(file),
            round(stat.st_size / 1024, 2),
            datetime.fromtimestamp(
                stat.st_mtime
            ).isoformat()
        ])

    except Exception as exc:
        print(f"SKIP: {file}")
        print(exc)

rows.sort()

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "extension",
        "path",
        "size_kb",
        "modified"
    ])

    writer.writerows(rows)

print("=" * 60)
print(f"Files indexed : {len(rows)}")
print(f"Output        : {OUTPUT_FILE}")
print("=" * 60)

