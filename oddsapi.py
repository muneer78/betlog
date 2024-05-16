import pandas as pd

# Assuming 'odds_json' is the variable holding your JSON data
odds_data = odds_json

# Prepare lists to hold extracted data
events = []
for event in odds_data:
    event_id = event['id']
    sport_key = event['sport_key']
    sport_title = event['sport_title']
    commence_time = event['commence_time']
    home_team = event['home_team']
    away_team = event['away_team']

    for bookmaker in event['bookmakers']:
        bookmaker_key = bookmaker['key']
        bookmaker_title = bookmaker['title']

        for market in bookmaker['markets']:
            if market['key'] == 'spreads':
                for outcome in market['outcomes']:
                    team = outcome['name']
                    price = outcome['price']
                    point = outcome['point']

                    # Append each record to the events list
                    events.append([event_id, sport_key, sport_title, commence_time, home_team, away_team, 
                                   bookmaker_key, bookmaker_title, team, price, point])

# Create a DataFrame from the events list
columns = ['Event ID', 'Sport Key', 'Sport Title', 'Commence Time', 'Home Team', 'Away Team', 
           'Bookmaker Key', 'Bookmaker Title', 'Team', 'Price', 'Point Spread']
df = pd.DataFrame(events, columns=columns)

# Display the DataFrame
print(df)
