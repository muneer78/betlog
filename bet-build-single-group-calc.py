from collections.abc import Sequence
from typing import TypeAlias

import polars as pl

Bet: TypeAlias = tuple[str, float, int | str]


def calculate_betting_results(data: Sequence[Bet]) -> pl.DataFrame:
    """Calculate the return for each possible winning bet in a bet group."""
    if not data:
        raise ValueError("data must contain at least one bet")

    results = pl.DataFrame(
        data,
        schema={
            "bet": pl.String,
            "bet_amount": pl.Float64,
            "odds": pl.String,
        },
        orient="row",
    ).with_columns(pl.col("odds").cast(pl.Int64))

    if results["bet_amount"].le(0).any():
        raise ValueError("bet amounts must be greater than zero")
    if results["odds"].eq(0).any():
        raise ValueError("American odds cannot be zero")

    total_staked = pl.col("bet_amount").sum()
    decimal_odds = (
        pl.when(pl.col("odds") > 0)
        .then(1 + pl.col("odds") / 100)
        .otherwise(1 + 100 / pl.col("odds").abs())
    )

    return (
        results.with_columns(decimal_odds.alias("decimal_odds"))
        .with_columns(
            (pl.col("bet_amount") * (pl.col("decimal_odds") - 1)).alias("gross_profit")
        )
        .with_columns(
            (pl.col("gross_profit") - (total_staked - pl.col("bet_amount"))).alias(
                "net_profit"
            )
        )
        .with_columns(
            (100 * pl.col("net_profit") / pl.col("bet_amount")).round(2).alias("ROI")
        )
    )


def calculate_and_save_betting_results(
    group_name: str, data_list: Sequence[Bet]
) -> pl.DataFrame:
    """Calculate and display betting results; return the numeric DataFrame."""
    results = calculate_betting_results(data_list)

    display_results = results.with_columns(
        pl.col("bet_amount", "gross_profit", "net_profit").map_elements(
            lambda value: f"${value:.2f}",
            return_dtype=pl.String,
        )
    )

    minimum_roi = results["ROI"].min()
    average_roi = results["ROI"].mean()

    print(f"{group_name}:")
    print(display_results)
    print(f"Minimum ROI: {minimum_roi:.2f}")
    print(f"Average ROI: {average_roi:.2f}\n")

    return results


if __name__ == "__main__":
    data = [
        ("Arizona", 1, "+1100"),
        ("Auburn", 1, "+2100"),
        ("Alabama", 1, "+2000"),
        ("Iowa State", 1, "+2000"),
        ("Tennessee", 1, "+1400"),
    ]
    calculate_and_save_betting_results("Build Returns", data)
