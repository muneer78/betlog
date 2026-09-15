```python
#!/usr/bin/env python3
"""
Build ladder-bet results and ROI summaries using DuckDB.

OVERVIEW
--------
This script reads ladder bets from a CSV file, calculates decimal odds,
profit, and ROI, and produces two clean CSV files:

    ladder_builds.csv
        Detailed results. Contains one row per bet and includes the
        original bet_group, Odds, Amount, plus calculated decimal_odds,
        profit, and ROI.

    ladder_builds_summary.csv
        One row per bet_group containing the minimum and average ROI.

The calculations are performed by DuckDB rather than Pandas. The input
CSV is loaded into DuckDB once and all transformations and aggregations
are performed there.

INPUT
-----
The default input file is:

    recladders.csv

The input CSV must contain at least these columns:

    bet_group
    Odds
    Amount

Example:

    bet_group,Odds,Amount
    1,100,10
    1,-110,20
    2,150,25

ODDS
----
Odds are expected to be American odds.

Examples:

    +150 -> 2.50 decimal odds
    +100 -> 2.00 decimal odds
    -110 -> 1.90909... decimal odds
    -200 -> 1.50 decimal odds

ROI is calculated as:

    ROI = 100 * profit / Amount

For a winning bet:

    profit = Amount * (decimal_odds - 1)

USAGE
-----
Run with the default filenames:

    python ladder-build.py

This reads:

    recladders.csv

and creates:

    ladder_builds.csv
    ladder_builds_summary.csv

Specify a different input file:

    python ladder-build.py --input my_ladders.csv

Specify custom output filenames:

    python ladder-build.py \
        --input my_ladders.csv \
        --output results.csv \
        --summary-output summary.csv

Show command-line help:

    python ladder-build.py --help

REQUIREMENTS
------------
Python 3.10+ and DuckDB.

Install DuckDB with:

    pip install duckdb

OUTPUT FORMAT
-------------
The detailed output is a standard rectangular CSV suitable for loading
into DuckDB, Pandas, Polars, Excel, or other analytical tools.

Example:

    bet_group,Odds,Amount,decimal_odds,profit,ROI
    1,100,10.00,2.000000,10.00,100.00
    1,-110,20.00,1.909091,18.18,90.91
    2,150,25.00,2.500000,37.50,150.00

The summary output is also a standard CSV:

    bet_group,minimum_roi,average_roi
    1,90.91,95.45
    2,150.00,150.00

NOTES
-----
- Amount, profit, and ROI remain numeric in the output. Currency symbols
  are intentionally not added so the files remain easy to process.
- ROI is rounded to two decimal places.
- Decimal odds are written to six decimal places.
- Invalid numeric values are rejected rather than silently converted.
- The original bet_group column is retained in the detailed output.
- The script does not modify the input CSV.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb


DEFAULT_INPUT = Path("recladders.csv")
DEFAULT_OUTPUT = Path("ladder_builds.csv")
DEFAULT_SUMMARY_OUTPUT = Path("ladder_builds_summary.csv")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Build ladder betting results and ROI summaries using DuckDB."
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Input CSV file (default: {DEFAULT_INPUT})",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Detailed output CSV (default: {DEFAULT_OUTPUT})",
    )

    parser.add_argument(
        "-s",
        "--summary-output",
        type=Path,
        default=DEFAULT_SUMMARY_OUTPUT,
        help=f"Summary output CSV (default: {DEFAULT_SUMMARY_OUTPUT})",
    )

    return parser.parse_args()


def build_ladder_files(
    input_file: Path,
    output_file: Path,
    summary_output_file: Path,
) -> None:
    """Read ladder bets, calculate results, and write two CSV outputs."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Create parent directories when custom output paths are supplied.
    output_file.parent.mkdir(parents=True, exist_ok=True)
    summary_output_file.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()

    try:
        # Load the source data once into DuckDB.
        con.execute(
            """
            CREATE OR REPLACE TEMP TABLE bets AS
            SELECT
                bet_group,
                TRY_CAST(Odds AS DOUBLE) AS Odds,
                TRY_CAST(Amount AS DOUBLE) AS Amount
            FROM read_csv_auto(?)
            """,
            [str(input_file)],
        )

        # Validate that the required columns contain usable numeric data.
        invalid_rows = con.execute(
            """
            SELECT COUNT(*)
            FROM bets
            WHERE Odds IS NULL
               OR Amount IS NULL
            """
        ).fetchone()[0]

        if invalid_rows:
            raise ValueError(
                f"Found {invalid_rows} row(s) with invalid Odds or Amount values."
            )

        # Build the detailed result set.
        con.execute(
            """
            CREATE OR REPLACE TEMP TABLE ladder_results AS
            SELECT
                bet_group,
                Odds,
                Amount,

                CASE
                    WHEN Odds > 0
                        THEN 1.0 + Odds / 100.0
                    WHEN Odds < 0
                        THEN 1.0 + 100.0 / ABS(Odds)
                    ELSE NULL
                END AS decimal_odds,

                CASE
                    WHEN Odds > 0
                        THEN Amount * (Odds / 100.0)
                    WHEN Odds < 0
                        THEN Amount * (100.0 / ABS(Odds))
                    ELSE NULL
                END AS profit

            FROM bets
            """
        )

        # Add ROI after profit has been calculated.
        con.execute(
            """
            CREATE OR REPLACE TEMP TABLE final_results AS
            SELECT
                bet_group,
                Odds,
                Amount,
                decimal_odds,
                profit,
                ROUND(
                    100.0 * profit / NULLIF(Amount, 0),
                    2
                ) AS ROI
            FROM ladder_results
            """
        )

        # Write a normal rectangular CSV containing every bet.
        con.execute(
            """
            COPY (
                SELECT
                    bet_group,
                    Odds,
                    ROUND(Amount, 2) AS Amount,
                    ROUND(decimal_odds, 6) AS decimal_odds,
                    ROUND(profit, 2) AS profit,
                    ROI
                FROM final_results
                ORDER BY bet_group
            )
            TO ?
            WITH (
                FORMAT CSV,
                HEADER TRUE
            )
            """,
            [str(output_file)],
        )

        # Produce a separate, normal summary CSV.
        con.execute(
            """
            COPY (
                SELECT
                    bet_group,
                    MIN(ROI) AS minimum_roi,
                    ROUND(AVG(ROI), 2) AS average_roi
                FROM final_results
                GROUP BY bet_group
                ORDER BY bet_group
            )
            TO ?
            WITH (
                FORMAT CSV,
                HEADER TRUE
            )
            """,
            [str(summary_output_file)],
        )

        # Get row counts for a useful completion message.
        bet_count = con.execute(
            "SELECT COUNT(*) FROM final_results"
        ).fetchone()[0]

        group_count = con.execute(
            "SELECT COUNT(DISTINCT bet_group) FROM final_results"
        ).fetchone()[0]

        print(f"Processed {bet_count:,} bets across {group_count:,} bet groups.")
        print(f"Wrote detailed results: {output_file}")
        print(f"Wrote summary:          {summary_output_file}")

    finally:
        con.close()


def main() -> None:
    """Run the ladder build."""
    args = parse_args()

    build_ladder_files(
        input_file=args.input,
        output_file=args.output,
        summary_output_file=args.summary_output,
    )


if __name__ == "__main__":
    main()
```
