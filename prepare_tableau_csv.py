#!/usr/bin/env python3
"""
Prepare the pydebug-gold CSV dataset for Tableau Public.

What this script does:
1) Cleans and normalizes text columns.
2) Converts numeric fields safely.
3) Extracts useful analytics fields from Context.
4) Creates Tableau-friendly output files.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


EXPECTED_COLUMNS = [
    "Instruction",
    "Context",
    "Response",
    "Rejected_Response",
    "Category",
    "Complexity",
]

ENV_PATTERN = re.compile(r"Environment:\s*([^.|]+)")
LOG_PATTERN = re.compile(r"Log_ID:\s*(\d+)")
ERROR_PATTERN = re.compile(r"System error:\s*([^.|]+)")
WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_text(value: str) -> str:
    """Trim and normalize whitespace for stable Tableau grouping."""
    if value is None:
        return ""
    return WHITESPACE_PATTERN.sub(" ", value).strip()


def safe_int(value: str) -> int | None:
    """Convert to int if possible, else return None."""
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def extract_with_pattern(pattern: re.Pattern[str], text: str) -> str:
    """Return first regex group match or empty string."""
    match = pattern.search(text or "")
    return match.group(1).strip() if match else ""


def derive_record(row: dict[str, str]) -> dict[str, object]:
    """Build one enriched, Tableau-ready record."""
    instruction = clean_text(row.get("Instruction", ""))
    context = clean_text(row.get("Context", ""))
    response = clean_text(row.get("Response", ""))
    rejected_response = clean_text(row.get("Rejected_Response", ""))
    category = clean_text(row.get("Category", ""))
    complexity = safe_int(row.get("Complexity", ""))

    environment = extract_with_pattern(ENV_PATTERN, context)
    log_id = extract_with_pattern(LOG_PATTERN, context)
    system_error = extract_with_pattern(ERROR_PATTERN, context)

    instruction_words = len(instruction.split())
    response_words = len(response.split())
    rejected_words = len(rejected_response.split())

    response_characters = len(response)
    rejected_characters = len(rejected_response)
    response_minus_rejected_words = response_words - rejected_words

    complexity_bucket = "Unknown"
    if complexity is not None:
        if complexity <= 2:
            complexity_bucket = "Low (1-2)"
        elif complexity <= 4:
            complexity_bucket = "Medium (3-4)"
        else:
            complexity_bucket = "High (5+)"

    return {
        "Instruction": instruction,
        "Context": context,
        "Response": response,
        "Rejected_Response": rejected_response,
        "Category": category,
        "Complexity": complexity,
        "Environment": environment,
        "System_Error": system_error,
        "Log_ID": log_id,
        "Instruction_Words": instruction_words,
        "Response_Words": response_words,
        "Rejected_Words": rejected_words,
        "Response_Characters": response_characters,
        "Rejected_Characters": rejected_characters,
        "Response_Minus_Rejected_Words": response_minus_rejected_words,
        "Complexity_Bucket": complexity_bucket,
        "Has_Rejected_Response": bool(rejected_response),
    }


def prepare_tableau_csv(
    input_csv: Path,
    output_csv: Path,
    sample_csv: Path | None = None,
    sample_rows: int = 20000,
) -> tuple[int, int]:
    """Read raw CSV and write enriched Tableau-ready CSV."""
    output_fields = [
        "Instruction",
        "Context",
        "Response",
        "Rejected_Response",
        "Category",
        "Complexity",
        "Environment",
        "System_Error",
        "Log_ID",
        "Instruction_Words",
        "Response_Words",
        "Rejected_Words",
        "Response_Characters",
        "Rejected_Characters",
        "Response_Minus_Rejected_Words",
        "Complexity_Bucket",
        "Has_Rejected_Response",
    ]

    total_rows = 0
    sample_written = 0

    with input_csv.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        missing = [col for col in EXPECTED_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Input CSV is missing expected columns: {missing}")

        with output_csv.open("w", encoding="utf-8", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=output_fields)
            writer.writeheader()

            sample_writer = None
            sample_handle = None
            if sample_csv is not None:
                sample_handle = sample_csv.open("w", encoding="utf-8", newline="")
                sample_writer = csv.DictWriter(sample_handle, fieldnames=output_fields)
                sample_writer.writeheader()

            try:
                for row in reader:
                    record = derive_record(row)
                    writer.writerow(record)
                    total_rows += 1

                    if sample_writer is not None and sample_written < sample_rows:
                        sample_writer.writerow(record)
                        sample_written += 1
            finally:
                if sample_handle is not None:
                    sample_handle.close()

    return total_rows, sample_written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean and enrich pydebug CSV for Tableau Public."
    )
    parser.add_argument(
        "--input",
        default="python_expert_debug_150k.csv",
        help="Path to source CSV file.",
    )
    parser.add_argument(
        "--output",
        default="python_expert_debug_150k_tableau_ready.csv",
        help="Path for full Tableau-ready CSV output.",
    )
    parser.add_argument(
        "--sample-output",
        default="python_expert_debug_150k_tableau_sample_20k.csv",
        help="Path for sample CSV output (set empty string to disable).",
    )
    parser.add_argument(
        "--sample-rows",
        type=int,
        default=20000,
        help="Maximum rows to include in sample output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_csv = Path(args.input)
    output_csv = Path(args.output)
    sample_csv = Path(args.sample_output) if args.sample_output.strip() else None

    if not input_csv.exists():
        raise FileNotFoundError(f"Input file not found: {input_csv}")

    rows, sample_rows = prepare_tableau_csv(
        input_csv=input_csv,
        output_csv=output_csv,
        sample_csv=sample_csv,
        sample_rows=args.sample_rows,
    )

    print(f"Done. Wrote {rows} rows to: {output_csv}")
    if sample_csv is not None:
        print(f"Wrote {sample_rows} sample rows to: {sample_csv}")


if __name__ == "__main__":
    main()
