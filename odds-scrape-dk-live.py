# cleaned up terminal print statements to only show when changes were detected - 5pm

import requests
import pandas as pd
import time


# Fetch data from API


def fetch_data():
    url = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkusks/v1/leagues/88808"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    return response.json()


# Process API data into a DataFrame


def process_data(data):
    rows = []
    events = data.get("events", [])
    markets = data.get("markets", [])
    selections = data.get("selections", [])

    for event in events:
        event_id = event["id"]
        game = event["name"]
        start_time = event["startEventDate"]

        for market in markets:
            if market["eventId"] != event_id:
                continue
            for selection in selections:
                if selection["marketId"] == market["id"]:
                    rows.append(
                        {
                            "event_id": event_id,
                            "game": game,
                            "start_time": start_time,
                            "bet_type": market["name"],
                            "team": selection["label"],
                            "line": selection.get("points"),
                            "price": selection["displayOdds"]["american"],
                        }
                    )

    return pd.DataFrame(rows)


# Save data to CSV files


def save_data(df):
    totals = df[df["bet_type"] == "Total"].drop_duplicates(subset=["event_id"])
    totals_df = totals[["game", "team", "line", "price"]]
    totals_df.to_csv("totals.csv", index=False, encoding="utf-8-sig")

    spreads = df[df["bet_type"] == "Spread"]
    spreads.to_csv("spreads.csv", index=False, encoding="utf-8-sig")

    moneylines = df[df["bet_type"] == "Moneyline"]
    moneylines.to_csv("moneylines.csv", index=False, encoding="utf-8-sig")


# Detect and display changes


def detect_changes(new_data, prev_data):
    if prev_data.empty:
        # No previous data: just return current data, no print.
        return new_data
    # Compare using pandas compare
    try:
        changes = new_data.reset_index().compare(prev_data.reset_index())
    except ValueError:
        # If there's an error comparing, return current data, no print.
        return new_data
    if changes.empty:
        # No changes: no print.
        return new_data

    # Print changes
    output = []
    processed_games = set()

    for idx in changes.index:
        if idx not in new_data.index or idx not in prev_data.index:
            continue

        game = new_data.loc[idx, "game"]
        team = new_data.loc[idx, "team"]
        bet_type = new_data.loc[idx, "bet_type"]

        if "line" in changes.columns.levels[0]:
            line_new = (
                changes.at[idx, ("line", "self")]
                if ("line", "self") in changes.columns
                else None
            )
            line_old = (
                changes.at[idx, ("line", "other")]
                if ("line", "other") in changes.columns
                else None
            )
        else:
            line_new, line_old = None, None

        if "price" in changes.columns.levels[0]:
            price_new = (
                changes.at[idx, ("price", "self")]
                if ("price", "self") in changes.columns
                else None
            )
            price_old = (
                changes.at[idx, ("price", "other")]
                if ("price", "other") in changes.columns
                else None
            )
        else:
            price_new, price_old = None, None

        # Spread changes
        if bet_type == "Spread" and (line_new is not None or price_new is not None):
            output.append(
                f"{team} spread moved from {line_old} ({price_old}) to {line_new} ({price_new})"
            )

        # Moneyline changes
        elif bet_type == "Moneyline" and (price_new is not None):
            output.append(f"{team} moneyline moved from {price_old} to {price_new}")

        # Totals changes
        elif (
            bet_type == "Total"
            and game not in processed_games
            and (line_new is not None)
        ):
            processed_games.add(game)
            try:
                over_new = new_data[
                    (new_data["game"] == game) & (new_data["team"] == "Over")
                ]["price"].iloc[0]
                under_new = new_data[
                    (new_data["game"] == game) & (new_data["team"] == "Under")
                ]["price"].iloc[0]

                over_old = prev_data[
                    (prev_data["game"] == game) & (prev_data["team"] == "Over")
                ]["price"].iloc[0]
                under_old = prev_data[
                    (prev_data["game"] == game) & (prev_data["team"] == "Under")
                ]["price"].iloc[0]

                output.append(
                    f"{game} total changed from {line_old} to {line_new}. Over/Under prices changed from Over: {over_old} Under: {under_old} to Over: {over_new} Under: {under_new}"
                )
            except IndexError:
                continue

    for change in output:
        print(change)

    return new_data


def main():
    prev_df = pd.DataFrame()
    while True:
        try:
            raw_data = fetch_data()
            processed_df = process_data(raw_data)
            save_data(processed_df)
            prev_df = detect_changes(processed_df, prev_df)
        except Exception:
            pass  # If error, do nothing (no prints)
        time.sleep(30)


if __name__ == "__main__":
    main()
