#!/usr/bin/env python3
"""Validate a CSV file and create a cleaned copy plus an error report."""

import argparse
import csv
import re
from pathlib import Path

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_csv(input_path: Path):
    errors = []
    valid_rows = []

    with input_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("The CSV file is empty or has no header row.")

        seen_rows = set()
        for row_number, row in enumerate(reader, start=2):
            row_errors = []

            # Check every field for missing values.
            for column, value in row.items():
                if value is None or not value.strip():
                    row_errors.append(f"Missing value in '{column}'")

            # Optional email validation when an Email column exists.
            email = row.get("Email", "")
            if email and email.strip() and not EMAIL_RE.match(email.strip()):
                row_errors.append("Invalid email format")

            # Optional numeric validation when an Age column exists.
            age = row.get("Age", "")
            if age and age.strip():
                try:
                    age_value = int(age)
                    if age_value < 0 or age_value > 120:
                        row_errors.append("Age must be between 0 and 120")
                except ValueError:
                    row_errors.append("Age must be a whole number")

            row_key = tuple((key, value or "") for key, value in row.items())
            if row_key in seen_rows:
                row_errors.append("Duplicate row")
            else:
                seen_rows.add(row_key)

            if row_errors:
                for issue in row_errors:
                    errors.append({
                        "row": row_number,
                        "column_or_check": issue,
                        "details": str(row)
                    })
            else:
                valid_rows.append(row)

        fieldnames = reader.fieldnames

    return fieldnames, valid_rows, errors


def main():
    parser = argparse.ArgumentParser(
        description="Check a CSV file for missing, duplicate, and invalid data."
    )
    parser.add_argument("input_csv", help="Path to the CSV file to validate")
    args = parser.parse_args()

    input_path = Path(args.input_csv)
    if not input_path.is_file():
        parser.error(f"File not found: {input_path}")

    try:
        fieldnames, valid_rows, errors = validate_csv(input_path)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Could not process CSV: {exc}")
        raise SystemExit(1)

    cleaned_path = input_path.with_name(input_path.stem + "_cleaned.csv")
    report_path = input_path.with_name(input_path.stem + "_validation_report.csv")

    with cleaned_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid_rows)

    with report_path.open("w", newline="", encoding="utf-8") as file:
        columns = ["row", "column_or_check", "details"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(errors)

    print(f"Rows accepted: {len(valid_rows)}")
    print(f"Issues found: {len(errors)}")
    print(f"Cleaned CSV: {cleaned_path}")
    print(f"Validation report: {report_path}")


if __name__ == "__main__":
    main()
