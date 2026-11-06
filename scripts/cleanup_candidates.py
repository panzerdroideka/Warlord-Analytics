#!/usr/bin/env python3

import csv
import hashlib

from pathlib import Path
from collections import defaultdict, Counter

INVENTORY = "analytics/file_inventory.csv"

EXCLUDES = [

    ".venv",
    "/venv/",
    "site-packages",
    "dist-packages",
    "miniconda",
    "__pycache__",

    ".cache",
    ".config",
    ".local",

    ".log",
    "combat.log",

    "journal",
    "telemetry.log",
    "network.log",

    "arkiv_privat",
    "warlord-logs-private/lotro/combat",

    "license",
]

def excluded(path):

    p = path.lower()

    return any(x in p for x in EXCLUDES)


def sha256_file(path):

    h = hashlib.sha256()

    try:

        with open(path, "rb") as f:

            while True:

                chunk = f.read(1024 * 1024)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()

    except Exception:

        return None


def rank(path):

    p = path.lower()

    if "/github/" in p:
        return 0

    if "/wilsnorsediscoveries/" in p:
        return 1

    if "/dokumenter/" in p:
        return 2

    if "/nedlastinger/" in p:
        return 3

    return 999


candidate_groups = defaultdict(list)

print("Reading inventory...")

with open(INVENTORY, encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        path = row["path"]

        if excluded(path):
            continue

        candidate_groups[Path(path).name].append(path)

hash_groups = defaultdict(list)

print("Calculating SHA256...")

for _, paths in candidate_groups.items():

    if len(paths) < 2:
        continue

    for path in paths:

        digest = sha256_file(path)

        if digest:

            hash_groups[digest].append(path)

folder_savings = Counter()

groups = []

for digest, paths in hash_groups.items():

    if len(paths) < 2:
        continue

    keep = sorted(paths, key=rank)[0]

    try:
        size = Path(keep).stat().st_size
    except:
        size = 0

    delete_candidates = [

        p for p in paths
        if p != keep

    ]

    if not delete_candidates:
        continue

    for path in delete_candidates:

        folder = str(Path(path).parent)

        folder_savings[folder] += size

    groups.append({

        "keep": keep,
        "delete": delete_candidates,
        "size": size,
        "saving": size * len(delete_candidates)

    })

groups.sort(

    key=lambda x: x["saving"],
    reverse=True

)

print()
print("=" * 80)
print("KEEP / DELETE CANDIDATES")
print("=" * 80)

total = 0

for item in groups:

    total += item["saving"]

    print()

    print(
        f"SAVING : {item['saving']/1024/1024:.2f} MB"
    )

    print(
        f"KEEP   : {item['keep']}"
    )

    print()

    print("DELETE CANDIDATES:")

    for p in item["delete"]:

        print("  ", p)

print()
print("=" * 80)
print("SPACE SAVINGS BY FOLDER")
print("=" * 80)

for folder, size in sorted(

        folder_savings.items(),
        key=lambda x: x[1],
        reverse=True

):

    print(
        f"{size/1024/1024:8.2f} MB  {folder}"
    )

print()
print("=" * 80)

print(
    f"TOTAL POSSIBLE SAVING : "
    f"{total/1024/1024/1024:.2f} GB"
)

print("=" * 80)
