#!/usr/bin/env python3

import csv
import hashlib
from pathlib import Path
from collections import defaultdict

INVENTORY = "analytics/file_inventory.csv"

candidate_groups = defaultdict(list)

print("Reading inventory...")

with open(INVENTORY, encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        path = row["path"]

        filename = Path(path).name

        candidate_groups[filename].append(path)

print("Finding duplicate filenames...")

duplicates = {
    name: paths
    for name, paths in candidate_groups.items()
    if len(paths) > 1
}

print(f"Candidate groups: {len(duplicates)}")
print()

hash_groups = defaultdict(list)

def sha256_file(filepath):

    h = hashlib.sha256()

    try:

        with open(filepath, "rb") as f:

            while True:

                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()

    except Exception:
        return None


for filename, paths in duplicates.items():

    for path in paths:

        digest = sha256_file(path)

        if digest:

            hash_groups[digest].append(path)

true_duplicates = {
    digest: paths
    for digest, paths in hash_groups.items()
    if len(paths) > 1
}

print("=" * 70)
print("TRUE DUPLICATES (SHA256 VERIFIED)")
print("=" * 70)
print()

for digest, paths in true_duplicates.items():

    print(f"SHA256: {digest}")

    for p in paths:
        print(f"  {p}")

    print()

print("=" * 70)
print(f"Verified duplicate groups: {len(true_duplicates)}")
print("=" * 70)
