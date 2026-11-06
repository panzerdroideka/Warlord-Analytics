#!/usr/bin/env python3

import csv
from pathlib import Path
from collections import Counter, defaultdict

inventory = "analytics/file_inventory.csv"

stats = Counter()
folders = Counter()
duplicates = defaultdict(list)

with open(inventory, encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        path = row["path"]
        lower = path.lower()

        try:
            size_kb = float(row["size_kb"])
        except:
            size_kb = 0

        if "lotro" not in lower and "wine_" not in lower:
            continue

        stats["files"] += 1
        stats["size_kb"] += size_kb

        filename = Path(path).name

        duplicates[filename].append(path)

        if "lotroclient64" in lower:
            stats["telemetry"] += 1

        if "_summary.csv" in lower:
            stats["summary"] += 1

        if "wine_" in lower:
            stats["wine"] += 1

        if "warlord-logs-private" in lower:
            stats["private"] += 1

        if "warlord-logs-public" in lower:
            stats["public"] += 1

        parent = str(Path(path).parent)

        folders[parent] += 1

print()
print("=" * 60)
print("WARLORD ANALYTICS - LOTRO REPORT")
print("=" * 60)

print(f"LotRO files      : {stats['files']}")
print(f"Telemetry files  : {stats['telemetry']}")
print(f"Summary files    : {stats['summary']}")
print(f"Wine files       : {stats['wine']}")
print(f"Private repo     : {stats['private']}")
print(f"Public repo      : {stats['public']}")

print()

print(f"Total size MB    : {stats['size_kb'] / 1024:.2f}")
print(f"Total size GB    : {stats['size_kb'] / 1024 / 1024:.2f}")

print()
print("=" * 60)
print("TOP FOLDERS")
print("=" * 60)

for folder, count in folders.most_common(10):
    print(f"{count:5}  {folder}")

print()
print("=" * 60)
print("POSSIBLE DUPLICATES")
print("=" * 60)

duplicate_groups = 0

for filename, paths in duplicates.items():

    if len(paths) > 1:

        duplicate_groups += 1

        print()
        print(filename)

        for p in paths[:5]:
            print("  ", p)

print()
print(f"Duplicate groups found: {duplicate_groups}")

print("=" * 60)
