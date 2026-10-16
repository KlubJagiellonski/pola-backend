#!/usr/bin/env python3
"""
Standalone script to mark companies as high tax based on NIP numbers from a CSV file.

What this script does:
- Reads a CSV file that contains a column with Polish NIP (tax ID) numbers.
- Normalizes the NIP values (digits only) and deduplicates them.
- For every company existing in the database with any of those NIP numbers,
  sets its boolean field `high_tax` to True.

CSV expectations:
- The CSV must have a column that contains NIP numbers. By default, the script
  will try to auto-detect a column whose header contains "nip" (case-insensitive),
  or you can specify it explicitly with `--nip-column`.
- The file is read as UTF-8 (with BOM tolerated), and the default delimiter is a comma.

Usage examples:
  DJANGO_SETTINGS_MODULE=pola.config.settings.local \
    python scripts/mark_high_tax_by_nip.py mgbi_idpcit_2024_top200_20260901.csv

  python scripts/mark_high_tax_by_nip.py mgbi_idpcit_2024_top200_20260901.csv \
    --settings pola.config.settings.local --nip-column "Numer NIP"

Notes:
- No changes are made in dry-run mode (`--dry-run`).
"""

import argparse
import csv
import os
import re
import sys
from collections.abc import Iterable, Sequence
from typing import Optional


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=("Manipulate Company.high_tax via NIP list from CSV, or reset all to False.")
    )
    parser.add_argument(
        "--settings",
        default=os.environ.get("DJANGO_SETTINGS_MODULE", "pola.config.settings.local"),
        help=("Django settings module (default: env DJANGO_SETTINGS_MODULE or 'pola.config.settings.local')."),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # from-csv subcommand (previous default behavior)
    p_csv = subparsers.add_parser(
        "from-csv",
        help="Read NIPs from CSV and set high_tax=True for matching companies.",
    )
    p_csv.add_argument(
        "csv_path",
        help="Path to the input CSV file (must contain a NIP column).",
    )
    p_csv.add_argument(
        "--delimiter",
        default=",",
        help="CSV delimiter (default ',').",
    )
    p_csv.add_argument(
        "--nip-column",
        default=None,
        help=("Name of the CSV column containing NIP values. If omitted, auto-detect a header containing 'nip'."),
    )
    p_csv.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write changes; only report what would be done.",
    )

    # reset subcommand
    p_reset = subparsers.add_parser(
        "reset",
        help="Set high_tax=False for all companies (optionally dry-run).",
    )
    p_reset.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write changes; only report what would be done.",
    )

    return parser.parse_args(list(argv))


def setup_django(settings_module: str) -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    try:
        import django  # type: ignore
    except ImportError:
        print("Django is required to run this script.", file=sys.stderr)
        raise
    django.setup()


def normalize_nip(value: str) -> Optional[str]:
    if value is None:
        return None
    # Keep digits only
    digits = re.sub(r"\D+", "", str(value))
    if len(digits) == 10:
        return digits
    return None


def detect_nip_column(fieldnames: Iterable[str]) -> Optional[str]:
    if not fieldnames:
        return None
    candidates = [h for h in fieldnames if "nip" in h.lower()]
    if len(candidates) == 1:
        return candidates[0]
    # Prefer exact match if multiple contain 'nip'
    exact = [h for h in candidates if h.lower() == "nip"]
    if len(exact) == 1:
        return exact[0]
    # Common Polish header seen in provided file
    numer_nip = [h for h in fieldnames if h.strip().lower() == "numer nip"]
    if len(numer_nip) == 1:
        return numer_nip[0]
    return None


def read_nips_from_csv(csv_path: str, delimiter: str, nip_column: Optional[str]) -> tuple[set[str], list[str]]:
    unique_nips: set[str] = set()
    warnings: list[str] = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError("CSV appears to have no header row.")

        column = nip_column or detect_nip_column(reader.fieldnames)
        if not column:
            raise ValueError(
                "Could not auto-detect NIP column. Specify it explicitly with --nip-column. "
                f"Headers found: {', '.join(reader.fieldnames)}"
            )

        for idx, row in enumerate(reader, start=2):  # account for header line
            raw = (row.get(column) or "").strip()
            if raw == "":
                continue
            nip = normalize_nip(raw)
            if nip is None:
                warnings.append(f"Line {idx}: invalid NIP value '{raw}' (ignored)")
                continue
            unique_nips.add(nip)
    return unique_nips, warnings


def run_from_csv(args: argparse.Namespace) -> int:
    from django.db import transaction

    from pola.company.models import Company

    try:
        nips, warns = read_nips_from_csv(args.csv_path, args.delimiter, args.nip_column)
    except Exception as exc:
        print(f"Error reading CSV: {exc}", file=sys.stderr)
        return 1

    for w in warns:
        print(f"WARN: {w}", file=sys.stderr)

    if not nips:
        print("No valid 10-digit NIP values found in CSV.")
        return 0

    existing_nips = set(Company.objects.filter(nip__in=nips).values_list("nip", flat=True).distinct())

    to_update_count = Company.objects.filter(nip__in=existing_nips).count()

    if args.dry_run:
        print("Dry run: no changes written.")
        print(f"Unique NIPs in CSV:   {len(nips)}")
        print(f"NIPs present in DB:   {len(existing_nips)}")
        print(f"Companies to update:  {to_update_count}")
        missing = sorted(nips - existing_nips)
        if missing:
            head = ", ".join(missing[:20])
            more = "" if len(missing) <= 20 else f" ... (+{len(missing) - 20} more)"
            print(f"NIPs not found in DB: {len(missing)}: {head}{more}")
        return 0

    try:
        with transaction.atomic():
            updated = Company.objects.filter(nip__in=existing_nips).update(high_tax=True)
    except Exception as exc:
        print(f"Error updating companies: {exc}", file=sys.stderr)
        return 1

    print("Update summary:")
    print(f"  Unique NIPs in CSV:   {len(nips)}")
    print(f"  NIPs present in DB:   {len(existing_nips)}")
    print(f"  Companies updated:     {updated}")
    missing = sorted(nips - existing_nips)
    if missing:
        head = ", ".join(missing[:20])
        more = "" if len(missing) <= 20 else f" ... (+{len(missing) - 20} more)"
        print(f"  NIPs not found in DB: {len(missing)}: {head}{more}")
    return 0


def run_reset(args: argparse.Namespace) -> int:
    from django.db import transaction

    from pola.company.models import Company

    qs = Company.objects.all()
    current_true = qs.filter(high_tax=True).count()
    if args.dry_run:
        print("Dry run: no changes written.")
        print(f"Companies currently high_tax=True: {current_true}")
        print("Would set high_tax=False for all companies.")
        return 0

    try:
        with transaction.atomic():
            updated = qs.update(high_tax=False)
    except Exception as exc:
        print(f"Error resetting companies: {exc}", file=sys.stderr)
        return 1

    print("Reset summary:")
    print(f"  Companies previously high_tax=True: {current_true}")
    print(f"  Companies updated to high_tax=False: {updated}")
    return 0


def main(argv: list[str]) -> int:
    # Backward compatibility: allow calling without subcommand using a CSV path
    # Example: mark_high_tax_by_nip.py file.csv [options]
    if len(argv) > 1 and argv[1] not in ("from-csv", "reset") and not argv[1].startswith("-"):
        argv = [argv[0], "from-csv"] + argv[1:]

    args = parse_args(argv[1:])

    # Bootstrap Django
    setup_django(args.settings)

    if args.command == "from-csv":
        return run_from_csv(args)
    if args.command == "reset":
        return run_reset(args)

    print("Unknown command.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
