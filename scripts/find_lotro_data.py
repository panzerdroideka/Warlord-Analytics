#!/usr/bin/env python3

import csv
from collections import Counter

inventory = "analytics/file_inventory.csv"

keywords = [
    "lotro",
    "mangohud",
    "combat",
    "telemetry",
    "userpreferences",
]

matches = []

with open(inventory, encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:

        path = row["path"].lower()

        for keyword in keywords:

            if keyword in path:
                matches.append(row)
                break

print()
print("=" * 60)
print("LOTRO RELATED FILES")
print("=" * 60)

print(f"Found: {len(matches)}")
print()

for row in matches[:100]:
    print(row["path"])

print()
print("=" * 60)
