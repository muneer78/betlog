IMPLICIT_SPREADS = {
    (2.5, -115): 2.625,
    (3, 105): 2.625,
    (2.5, -120): 2.750,
    (3, 100): 2.750,
    (2.5, -125): 2.875,
    (3, -105): 2.875,
    (3, -110): 3.000,
    (3, -115): 3.125,
    (3.5, 105): 3.125,
    (3, -120): 3.250,
    (3.5, 100): 3.250,
    (3, -125): 3.375,
    (3.5, -105): 3.375,
    (7, 100): 6.750,
    (6.5, -115): 6.750,
    (7, -105): 6.875,
    (6.5, -120): 6.875,
    (7, -110): 7.000,
    (7.5, 100): 7.250,
    (7, -115): 7.375,
}


def implicit_spread(spread, odds):
    return IMPLICIT_SPREADS.get((spread, odds))


spread = float(input("Spread: "))
odds = int(input("Odds: "))

result = implicit_spread(spread, odds)

if result is None:
    print("No mapping found.")
else:
    print(f"Implicit spread: {result:g}")
