"""Compare a moneyline price with the equivalent point-spread price."""

from dataclasses import dataclass
from typing import Literal, cast


Side = Literal["F", "U"]


@dataclass(frozen=True)
class SpreadPrice:
    point_spread: float
    favorite_moneyline: int
    underdog_moneyline: int


# Moneyline equivalents for each half-point spread. Favorite prices are
# negative American odds; underdogs can be negative near a pick'em.
SPREAD_PRICES = tuple(
    SpreadPrice(spread / 2, -favorite, underdog)
    for spread, favorite, underdog in zip(
        range(2, 41),
        (
            116, 123, 130, 137, 170, 197, 210, 222, 237, 252,
            277, 299, 335, 368, 397, 427, 441, 456, 510, 561,
            595, 631, 657, 681, 730, 781, 904, 1024, 1086, 1147,
            1223, 1300, 1418, 1520, 1664, 1803, 1985, 2182, 2390,
        ),
        (
            -104, 102, 108, 113, 141, 163, 174, 184, 196, 208,
            229, 247, 277, 305, 328, 353, 365, 377, 422, 464,
            492, 522, 543, 564, 604, 646, 748, 847, 898, 949,
            1012, 1076, 1173, 1257, 1377, 1492, 1642, 1805, 1977,
        ),
        strict=True,
    )
)


def normalize_side(value: str) -> Side:
    """Validate and normalize a favorite/underdog selection."""
    side = value.strip().upper()
    if side not in {"F", "U"}:
        raise ValueError("Side must be 'F' for favorite or 'U' for underdog.")
    return cast(Side, side)


def nearest_spread_price(point_spread: float) -> SpreadPrice:
    """Return the closest table entry, resolving ties toward the lower spread."""
    return min(SPREAD_PRICES, key=lambda row: abs(row.point_spread - point_spread))


def should_bet_moneyline(point_spread: float, moneyline: int, side: Side) -> bool:
    """Return whether the offered moneyline is better than its spread equivalent."""
    reference = nearest_spread_price(point_spread)
    reference_moneyline = (
        reference.favorite_moneyline if side == "F" else reference.underdog_moneyline
    )
    return moneyline > reference_moneyline


def main() -> None:
    """Prompt for a bet and print the preferred market."""
    try:
        point_spread = float(input("Enter the Point Spread: "))
        moneyline = int(input("Enter the Moneyline: "))
        side = normalize_side(input("Enter 'F' for Favorite or 'U' for Underdog: "))
    except ValueError as error:
        raise SystemExit(f"Invalid input: {error}") from error

    decision = (
        "moneyline"
        if should_bet_moneyline(point_spread, moneyline, side)
        else "spread"
    )
    print(f"Bet {decision}")


if __name__ == "__main__":
    main()
