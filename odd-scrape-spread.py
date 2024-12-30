# from sbrscrape import Scoreboard
# from pprint import pprint

# games = Scoreboard(sport="NCAAB").games
# games[0]

# # Filter out games with status 'Final'
# filtered_games = [game for game in games if game.get('status') != 'Final']

# # Pretty print the filtered games
# pprint(filtered_games)

# '''print entire spread odds response'''
# from sbrscrape import Scoreboard
# from pprint import pprint

# games = Scoreboard(sport="NCAAB").games

# # Filter out games with status containing 'Final' or 'OT' and check the spread odds condition
# filtered_games = [
#     game for game in games 
#     if 'Final' not in game.get('status', '') and 'OT' not in game.get('status', '') and (
#         any(odds > 11 for odds in game.get('home_spread', {}).values()) or
#         any(odds > 11 for odds in game.get('away_spread', {}).values())
#     )
# ]

# # Pretty print the filtered games
# pprint(filtered_games)

from sbrscrape import Scoreboard
from pprint import pprint

# Fetch games for multiple sports
sports = ["NCAAB", "NBA", "NFL"]
games = []
for sport in sports:
    games.extend(Scoreboard(sport=sport).games)

# Filter out games with status containing 'Final' or 'OT' and check the spread odds condition
filtered_games = [
    game for game in games 
    if 'Final' not in game.get('status', '') and 'OT' not in game.get('status', '') and (
        any(odds > 15 for odds in game.get('home_spread', {}).values()) or
        any(odds > 15 for odds in game.get('away_spread', {}).values())
    )
]

# Extract and print only the 'spread_odds' responses
spread_odds_responses = [
    {
        'date': game.get('date', ''),
        'home_team': game.get('home_team', {}),
        'home_spread': game.get('home_spread', {}),
        'away_team': game.get('away_team', {}),
        'away_spread': game.get('away_spread', {})
    }
    for game in filtered_games
]

# Pretty print the spread odds responses
pprint(spread_odds_responses)