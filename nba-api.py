from nba_api.stats.endpoints import playercareerstats
import pandas as pd

# Fetching career statistics for Player of Choice using his player ID
player_career = playercareerstats.PlayerCareerStats(player_id='202681')
player_career_df = player_career.get_data_frames()[0]

# Extracting the seasons of player of choice
seasons_played = player_career_df['SEASON_ID'].unique()
print(seasons_played.tolist())

# Initialize an empty DataFrame to store all game logs
all_seasons_logs_df = pd.DataFrame()

# List of seasons to loop through (update this list as needed)
seasons = ['2019-20', '2020-21', '2021-22', '2022-23', '2023-24']

# Fetch game logs for each season and add a 'SEASON' column
for season in seasons:
    player_logs = playergamelog.PlayerGameLog(player_id='202681', season=season)
    season_logs_df = player_logs.get_data_frames()[0]
    season_logs_df['SEASON'] = season  
    all_seasons_logs_df = pd.concat([all_seasons_logs_df, season_logs_df], ignore_index=True)

# Convert Game_Date to a datetime
all_seasons_logs_df['GAME_DATE'] = pd.to_datetime(all_seasons_logs_df['GAME_DATE'])
# Create Month_Year to faciliate Month/Date Analysis
all_seasons_logs_df['MONTH_YEAR'] = all_seasons_logs_df['GAME_DATE'].dt.to_period('M')

#Aggregate game level data to yearly
yearly_stats = all_seasons_logs_df.groupby('YEAR').agg({
    'FGM': 'sum', 
    'FGA': 'sum', 
    'FG3M': 'sum', 
    'FG3A': 'sum', 
    'FTM': 'sum', 
    'FTA': 'sum', 
}).reset_index()

# This takes the field goals made and attempted to calculate field goal percent
yearly_stats['FG_PCT'] = yearly_stats['FGM'] / yearly_stats['FGA']
yearly_stats['FG3_PCT'] = yearly_stats['FG3M'] / yearly_stats['FG3A']
yearly_stats['FT_PCT'] = yearly_stats['FTM'] / yearly_stats['FTA']
yearly_stats['GAMES'] = lebron_data.groupby('YEAR')['Game_ID'].count().values

# Calculate Cummulative Sum
all_seasons_logs_df['FG3M_CUMSUM'] = all_seasons_logs_df.groupby('YEAR')['FG3M'].cumsum()
all_seasons_logs_df['FGM_CUMSUM'] = all_seasons_logs_df.groupby('YEAR')['FGM'].cumsum()

-------------------

from nba_api.stats.endpoints import leaguedashplayerclutch
import pandas as pd

# Function to fetch clutch stats for a given season and add a season column
def fetch_clutch_stats(season):
    clutch_stats = leaguedashplayerclutch.LeagueDashPlayerClutch(season=season)
    clutch_stats_df = clutch_stats.get_data_frames()[0]
    clutch_stats_df['SEASON'] = season  # Adding a season column
    return clutch_stats_df

# List of seasons to analyze
seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23','2023-24']

# Concatenating data for all seasons into a single DataFrame
all_seasons_clutch_stats = pd.concat([fetch_clutch_stats(season) for season in seasons])

# Adding a column to flag the current season vs previous seasons
current_season = '2023-24'
all_seasons_clutch_stats['SEASON_TYPE'] = all_seasons_clutch_stats['SEASON'].apply(lambda x: 'Current Season' if x == current_season else 'Previous 5 Seasons')

# Displaying the first few rows of the combined DataFrame
print(all_seasons_clutch_stats[['SEASON', 'SEASON_TYPE', 'PLAYER_NAME', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'AST', 'PTS', 'REB', 'TOV', 'STL', 'BLK', 'PF']].head())
