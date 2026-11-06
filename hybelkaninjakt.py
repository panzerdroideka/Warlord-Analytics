#!/usr/bin/env python3

import csv
import hashlib
import subprocess

from pathlib import Path
from collections import defaultdict
from datetime import datetime

import csv
import hashlib

from pathlib import Path
from collections import defaultdict
from datetime import datetime

INVENTORY = "analytics/file_inventory.csv"

REPORT_FILE = (
    f"FULL_REPORT_{datetime.now().strftime('%Y%m%d')}.txt"
)


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


def is_candidate(path):

    p = path.lower()

    filename = Path(path).name.lower()

    if not filename.startswith("wine_"):
        return False

    if not filename.endswith(".csv"):
        return False

    return (
        "/github/" in p or
        "/nedlastinger/" in p
    )


def keep_priority(path):

    p = path.lower()

    if "/github/" in p:
        return 0

    return 999


print("Leser inventory...")

name_groups = defaultdict(list)

with open(INVENTORY, encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        path = row["path"]

        if not is_candidate(path):
            continue

        name_groups[Path(path).name].append(path)

print("Beregner SHA256...")

hash_groups = defaultdict(list)

for paths in name_groups.values():

    if len(paths) < 2:
        continue

    for path in paths:

        digest = sha256_file(path)

        if digest:

            hash_groups[digest].append(path)

families = []

all_delete_files = []
all_keep_files = []

total_saving = 0

for digest, paths in hash_groups.items():

    if len(paths) < 2:
        continue

    keep = sorted(paths, key=keep_priority)[0]

    try:

        size = Path(keep).stat().st_size

    except Exception:

        continue

    duplicates = [

        p for p in paths
        if p != keep

    ]

    if not duplicates:
        continue

    family_saving = size * len(duplicates)

    total_saving += family_saving

    all_keep_files.append(keep)

    all_delete_files.extend(duplicates)

    families.append({

        "name": Path(keep).name,
        "keep": keep,
        "duplicates": duplicates,
        "saving": family_saving,
        "size": size

    })

families.sort(
    key=lambda x: x["saving"],
    reverse=True
)

#
# FULL RAPPORT
#

report = []

report.append("=" * 80)
report.append("HYBELKANINRAPPORT")
report.append("=" * 80)
report.append("")

for idx, fam in enumerate(families, start=1):

    report.append(
        f"HYBELKANINFAMILIE {idx} AV {len(families)}"
    )

    report.append("-" * 80)

    report.append("")
    report.append("FAMILIENAVN:")
    report.append(f"  {fam['name']}")

    report.append("")
    report.append("MASTERKOPI (BEHOLDES):")
    report.append(f"  {fam['keep']}")

    report.append("")
    report.append("HYBELKANINER:")

    for dup in fam["duplicates"]:

        report.append(f"  {dup}")

    report.append("")

    report.append(
        f"FAMILIEGEVINST: "
        f"{fam['saving']/1024/1024:.2f} MB"
    )

    report.append("")
    report.append("")

report.append("=" * 80)
report.append("MASTERKOPIER SOM OVERLEVER")
report.append("=" * 80)

for file in all_keep_files:

    report.append(file)

report.append("")
report.append("=" * 80)
report.append("HYBELKANINER SOM KAN FJERNES")
report.append("=" * 80)

for file in all_delete_files:

    report.append(file)

report.append("")
report.append("=" * 80)
report.append("SLUTTOPPSUMMERING")
report.append("=" * 80)

report.append(
    f"HYBELKANIN-FAMILIER : {len(families)}"
)

report.append(
    f"MASTERKOPIER       : {len(all_keep_files)}"
)

report.append(
    f"HYBELKANINER       : {len(all_delete_files)}"
)

report.append(
    f"FRIGJØRBAR PLASS   : "
    f"{total_saving/1024/1024:.2f} MB"
)

report.append("")
report.append("MASTERLOKASJON:")
report.append("/home/wils/GitHub")

report.append("")
report.append("RYDDELOKASJONER:")
report.append("/home/wils/Nedlastinger")
report.append("/home/wils/Nedlastinger/wine_2026-")

with open(REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("\n".join(report))

#
# KOMPAKT TERMINALRAPPORT
#

print()
print("=" * 60)
print("HYBELKANIN-RAPPORT")
print("=" * 60)

print()
print(
    f"HYBELKANIN-FAMILIER : "
    f"{len(families)}"
)

print(
    f"MASTERKOPIER       : "
    f"{len(all_keep_files)}"
)

print(
    f"HYBELKANINER       : "
    f"{len(all_delete_files)}"
)

print(
    f"FRIGJØRBAR PLASS   : "
    f"{total_saving/1024/1024:.2f} MB"
)

print()

print("MASTERLOKASJON:")
print("  /home/wils/GitHub")

print()
print("RYDDELOKASJONER:")

print("  /home/wils/Nedlastinger")
print("  /home/wils/Nedlastinger/wine_2026-")

print()
print(
    f"FULL RAPPORT:"
)

print(
    f"  {REPORT_FILE}"
)

print()
print("FAMILIER:")

for idx, fam in enumerate(families, start=1):

    print(
        f"#{idx:02d} "
        f"{fam['name']}"
    )

    print(
        f"    {len(fam['duplicates'])} "
        f"hybelkaniner"
    )

    print(
        f"    "
        f"{fam['saving']/1024/1024:.2f} MB"
    )

print()

confirmation_text = (
    f"JA SLETT "
    f"{len(all_delete_files)} "
    f"HYBELKANINER"
)

print("=" * 60)
print("KLAR FOR OPPRYDDING")
print("=" * 60)

print()
print(
    f"{len(all_delete_files)} "
    f"SHA256-verifiserte hybelkaniner"
)

print(
    f"{total_saving/1024/1024:.2f} MB"
)

print()
print(
    "Disse sendes til PAPIRKURVEN."
)

print(
    "Masterkopiene beholdes."
)

print()
print(
    "For å fortsette må du skrive:"
)

print()
print(f"  {confirmation_text}")
print()

answer = input("> ").strip()

if answer != confirmation_text:

    print()
    print("AVBRUTT")
    raise SystemExit

print()
print("Sender filer til papirkurven...")

removed = 0

for file in all_delete_files:

    try:

        subprocess.run(
    ["gio", "trash", file],
    check=True
)

        removed += 1

    except Exception as e:

        print()
        print("FEIL:")
        print(file)
        print(e)

print()
print("=" * 60)

print(
    f"{removed} HYBELKANINER SENDT TIL PAPIRKURVEN"
)

print("=" * 60)
