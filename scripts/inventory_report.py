#!/usr/bin/env python3

import csv
from collections import Counter

counter = Counter()

with open(
    "analytics/file_inventory.csv",
    encoding="utf-8"
) as f:

    reader = csv.DictReader(f)

    for row in reader:
        counter[row["extension"]] += 1

print()
print("=" * 50)
print("FILE TYPES")
print("=" * 50)

for ext, count in sorted(counter.items()):
    print(f"{ext:6} {count}")

print("=" * 50)
