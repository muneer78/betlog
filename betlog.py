from pathlib import Path
import csv
import math

import duckdb


INPUT_FILE = Path("bet.csv")

BETLOG_FILE = Path("betlog.csv")
ANALYTICS_FILE = Path("analytics.csv")
PENDING_FILE = Path("pendingbets.csv")
CASHOUTS_FILE = Path("cashouts.csv")


def money(value):
    """Format a numeric value as currency for report output."""
    if value is None:
        return ""

    return f"${float(value):,.2f}"


def write_query_to_csv(connection, query, filename):
    """Run a DuckDB query and write the result to CSV."""
    connection.sql(query).write_csv(str(filename), header=True)


def write_analytics(connection):
    """Generate the combined analytics.csv report."""

    reports = [
        (
            "ROI By Sport",
            """
            SELECT
                Sport,
                ROUND(SUM(ActualPayout), 2) AS Profit,
                ROUND(SUM(Amount), 2) AS MoneyRisked,
                ROUND(
                    SUM(ActualPayout) / NULLIF(SUM(Amount), 0) * 100,
                    2
                ) AS ROI
            FROM bets
            GROUP BY Sport
            ORDER BY Sport
            """,
        ),
        (
            "Profit by Sport",
            """
            SELECT
                Sport,
                ROUND(SUM(ActualPayout), 2) AS Profit
            FROM bets
            GROUP BY Sport
            ORDER BY Sport
            """,
        ),
        (
            "Risk by Sport",
            """
            SELECT
                Sport,
                ROUND(SUM(Amount), 2) AS MoneyRisked
            FROM bets
            GROUP BY Sport
            ORDER BY Sport
            """,
        ),
        (
            "Profit by Month",
            """
            SELECT
                strftime(Date, '%Y-%m') AS Date,
                ROUND(SUM(ActualPayout), 2) AS Profit
            FROM bets
            GROUP BY strftime(Date, '%Y-%m')
            ORDER BY Date
            """,
        ),
        (
            "Profit by Sportsbook",
            """
            SELECT
                Sportsbook,
                ROUND(SUM(ActualPayout), 2) AS Profit
            FROM bets
            GROUP BY Sportsbook
            ORDER BY Sportsbook
            """,
        ),
        (
            "Risk by Sportsbook",
            """
            SELECT
                Sportsbook,
                ROUND(SUM(Amount), 2) AS MoneyRisked
            FROM bets
            GROUP BY Sportsbook
            ORDER BY Sportsbook
            """,
        ),
        (
            "Profit by System",
            """
            SELECT
                System,
                ROUND(SUM(ActualPayout), 2) AS Profit
            FROM bets
            GROUP BY System
            ORDER BY System
            """,
        ),
        (
            "Profit by Bet Type",
            """
            SELECT
                BetType,
                ROUND(SUM(ActualPayout), 2) AS Profit
            FROM bets
            GROUP BY BetType
            ORDER BY BetType
            """,
        ),
        (
            "Risk by Bet Type",
            """
            SELECT
                BetType,
                ROUND(SUM(Amount), 2) AS MoneyRisked
            FROM bets
            GROUP BY BetType
            ORDER BY BetType
            """,
        ),
        (
            "Total ROI",
            """
            SELECT
                ROUND(SUM(ActualPayout), 2) AS TotalWon,
                ROUND(SUM(Amount), 2) AS TotalRisked,
                ROUND(
                    SUM(ActualPayout) /
                    NULLIF(SUM(Amount), 0) * 100,
                    2
                ) AS TotalROI
            FROM bets
            """,
        ),
        (
            "Total Win Percentage",
            """
            WITH results AS (
                SELECT
                    COUNT(*) FILTER (WHERE Result = 'W') AS TotalBetsWon,
                    COUNT(*) FILTER (WHERE Result = 'L') AS TotalBetsLost
                FROM bets
            )
            SELECT
                TotalBetsWon,
                TotalBetsLost,
                ROUND(
                    (TotalBetsWon - TotalBetsLost)
                    / SQRT(TotalBetsWon + TotalBetsLost),
                    2
                ) AS gamblerzscore,
                ROUND(
                    TotalBetsWon /
                    NULLIF(TotalBetsWon + TotalBetsLost, 0) * 100,
                    2
                ) AS winning_pct
            FROM results
            """,
        ),
        (
            "Profit by Free Bet vs. Money Bet",
            """
            SELECT
                FreeBet,
                ROUND(SUM(ActualPayout), 2) AS Profit
            FROM bets
            GROUP BY FreeBet
            ORDER BY FreeBet
            """,
        ),
        (
            "Risk by Free Bet vs. Money Bet",
            """
            SELECT
                FreeBet,
                ROUND(SUM(Amount), 2) AS MoneyRisked
            FROM bets
            GROUP BY FreeBet
            ORDER BY FreeBet
            """,
        ),
    ]

    with ANALYTICS_FILE.open("w", newline="") as output:
        for title, query in reports:
            output.write(f"{title}\n")

            result = connection.sql(query)

            # Preserve the old currency formatting.
            columns = result.columns
            rows = result.fetchall()

            writer = csv.writer(output)
            writer.writerow(columns)

            for row in rows:
                formatted = []

                for column, value in zip(columns, row):
                    if column in {
                        "Profit",
                        "MoneyRisked",
                        "TotalWon",
                        "TotalRisked",
                    }:
                        formatted.append(money(value))
                    else:
                        formatted.append(value)

                writer.writerow(formatted)

            output.write("\n")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    connection = duckdb.connect()

    # ------------------------------------------------------------------
    # Load bet.csv and perform all calculations in DuckDB.
    #
    # This replaces:
    #   pandas.read_csv()
    #   numpy.where()
    #   iterrows()
    #   pandas.groupby()
    #   repeated read_csv() calls
    # ------------------------------------------------------------------

    connection.sql(
        f"""
        CREATE OR REPLACE TABLE bets AS

        WITH source AS (
            SELECT
                *,
                COALESCE(
                    TRY_CAST(Amount AS DOUBLE),
                    0
                ) AS Amount_,
                COALESCE(
                    TRY_CAST(Odds AS DOUBLE),
                    0
                ) AS Odds_,
                COALESCE(
                    TRY_CAST(PushAmount AS DOUBLE),
                    0
                ) AS PushAmount_,
                TRY_STRPTIME(
                    Date,
                    '%m/%d/%Y'
                ) AS Date_
            FROM read_csv_auto(
                '{INPUT_FILE.as_posix()}',
                header = true
            )
        ),

        calculated_profit AS (
            SELECT
                *,

                ABS(Odds_) AS CleanedOdds,

                ROUND(
                    CASE
                        WHEN Odds_ > 0
                            THEN
                                (ABS(Odds_) / 100) * Amount_
                        ELSE
                            (100 / NULLIF(ABS(Odds_), 0))
                            * Amount_
                    END,
                    2
                ) AS PotentialProfit

            FROM source
        ),

        calculated_payout AS (
            SELECT
                *,

                ROUND(
                    CASE
                        WHEN FreeBet = 'Y'
                            THEN PotentialProfit
                        ELSE
                            PotentialProfit + Amount_
                    END,
                    2
                ) AS PotentialPayout,

                /*
                 * IMPORTANT:
                 *
                 * The original script rounds implied probability
                 * before calculating Expected Value. Preserve that
                 * behavior here.
                 */
                ROUND(
                    CASE
                        WHEN Odds_ > 0
                            THEN 100 / (100 + CleanedOdds)
                        ELSE
                            CleanedOdds /
                            (100 + CleanedOdds)
                    END,
                    2
                ) AS ImpliedProbabilityRaw

            FROM calculated_profit
        )

        SELECT
            * EXCLUDE (
                Amount_,
                Odds_,
                PushAmount_,
                Date_,
                ImpliedProbabilityRaw
            ),

            Amount_ AS Amount,
            Odds_ AS Odds,
            PushAmount_ AS PushAmount,
            Date_ AS Date,

            ROUND(
                ImpliedProbabilityRaw * 100,
                2
            ) AS ImpliedProbability,

            ROUND(
                CEIL(
                    ImpliedProbabilityRaw * Amount_
                )
                -
                (
                    (1 - ImpliedProbabilityRaw)
                    * Amount_
                ),
                2
            ) AS "Expected Value",

            CASE
                WHEN Result = 'L'
                    AND FreeBet = 'N'
                    THEN Amount_ * -1

                WHEN Result = 'L'
                    AND FreeBet = 'Y'
                    THEN 0

                WHEN Result = 'W'
                    AND FreeBet = 'Y'
                    THEN PotentialProfit

                WHEN Result = 'W'
                    AND FreeBet = 'N'
                    THEN PotentialPayout

                WHEN Result = 'Pe'
                    THEN 0

                WHEN Result = 'P'
                    THEN PushAmount_

                ELSE NULL
            END AS ActualPayout

        FROM calculated_payout
        """
    )

    # ------------------------------------------------------------------
    # betlog.csv
    #
    # Keep the calculated values numeric internally. Only format them
    # as currency when writing the human-readable CSV.
    # ------------------------------------------------------------------

    betlog_columns = connection.sql(
        "SELECT * FROM bets LIMIT 0"
    ).columns

    currency_columns = {
        "Amount",
        "PushAmount",
        "PotentialProfit",
        "PotentialPayout",
        "Expected Value",
        "ActualPayout",
    }

    result = connection.sql("SELECT * FROM bets")

    with BETLOG_FILE.open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(betlog_columns)

        for row in result.fetchall():
            formatted = []

            for column, value in zip(betlog_columns, row):
                if column in currency_columns:
                    formatted.append(money(value))
                else:
                    formatted.append(value)

            writer.writerow(formatted)

    # ------------------------------------------------------------------
    # analytics.csv
    # ------------------------------------------------------------------

    write_analytics(connection)

    # ------------------------------------------------------------------
    # pendingbets.csv
    #
    # The original script rereads betlog.csv and filters Result = Pe.
    # We can query the already-calculated DuckDB table instead.
    # ------------------------------------------------------------------

    connection.sql(
        f"""
        COPY (
            SELECT * EXCLUDE (
                Result,
                PushAmount,
                CleanedOdds,
                ActualPayout
            )
            FROM bets
            WHERE Result = 'Pe'
        )
        TO '{PENDING_FILE.as_posix()}'
        WITH (HEADER, DELIMITER ',')
        """
    )

    # ------------------------------------------------------------------
    # cashouts.csv
    #
    # Result = P represents pushes/cashouts.
    # ------------------------------------------------------------------

    cashout_rows = connection.sql(
        """
        SELECT
            Sport,
            ROUND(PushAmount, 2) AS ActualPayout,
            ROUND(Amount, 2) AS Amount,
            ROUND(
                PushAmount / NULLIF(Amount, 0) * 100,
                2
            ) AS ROI
        FROM bets
        WHERE Result = 'P'
        """
    )

    with CASHOUTS_FILE.open("w", newline="") as output:
        writer = csv.writer(output)

        # The old pandas to_csv() included an index column.
        # We intentionally omit it here because it has no semantic value.
        writer.writerow(
            [
                "Sport",
                "ActualPayout",
                "Amount",
                "ROI",
            ]
        )

        for sport, payout, amount, roi in cashout_rows.fetchall():
            writer.writerow(
                [
                    sport,
                    money(payout),
                    money(amount),
                    roi,
                ]
            )

    connection.close()

    print("Bet log generated successfully.")
    print(f"  {BETLOG_FILE}")
    print(f"  {ANALYTICS_FILE}")
    print(f"  {PENDING_FILE}")
    print(f"  {CASHOUTS_FILE}")


if __name__ == "__main__":
    main()
