import pandas as pd
import scipy.stats as stats

# Your data as a list of dictionaries
data = [
    {"Player": "Damian Lillard", "Team": "Blazers", "Prop Stat": "Rebounds",
     "Which side is being offered in prop?": "Under", "Which side to bet?": "Over", "Odds offered": 125,
     "Prop": 3.5, "Average": 4, "Probability": None, "Break Even Odds": None, "No Hold Probability": "56%",
     "No Hold Line": -125, "Does Over/Under Match?": False, "Action to take": "No Bet"},
    {"Player": "Jerami Grant", "Team": "Blazers", "Prop Stat": "Assists",
     "Which side is being offered in prop?": "Over", "Which side to bet?": "Over", "Odds offered": 120,
     "Prop": 2.5, "Average": 2.7, "Probability": None, "Break Even Odds": None, "No Hold Probability": "55%",
     "No Hold Line": -120, "Does Over/Under Match?": False, "Action to take": "Bet"},
    # ... Add more data entries here ...
]

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)


# Function to calculate Poisson probability for each row
def calculate_poisson_probability(row):
    if pd.notna(row['Average']) and pd.notna(row['Prop']):
        average = row['Average']
        prop = row['Prop']
        probability = stats.poisson.pmf(prop, average)
        return f"{probability * 100:.2f}%"
    return None


# Function to compare "Which side is being offered in prop?" and "Which
# side to bet?" columns
def compare_sides(row):
    return row["Which side is being offered in prop?"] == row["Which side to bet?"]


# Function to calculate Break Even Odds
def calculate_break_even_odds(row):
    if pd.notna(row['Probability']):
        probability = float(row['Probability'].strip('%')) / 100
        return int((-100 if probability > 0.5 else 100)
                   * probability / (1 - probability))
    return None


# Function to calculate No Hold Probability
def calculate_no_hold_probability(row):
    if pd.notna(row['Odds offered']):
        odds_offered = row['Odds offered']
        return f"{odds_offered / (odds_offered + 100) * 100:.2f}%"
    return None


# Function to calculate No Hold Line
def calculate_no_hold_line(row):
    if pd.notna(row['No Hold Probability']):
        no_hold_probability = float(
            row['No Hold Probability'].strip('%')) / 100
        return int((-100 if no_hold_probability > 0.5 else 100) *
                   no_hold_probability / (1 - no_hold_probability))
    return None


# Function to calculate Action to Take
def calculate_action_to_take(row):
    if pd.notna(row['Odds offered']) and pd.notna(row['No Hold Line']) and row[
            'Does Over/Under Match?']:
        return "Bet" if row['Odds offered'] > row['No Hold Line'] else "No Bet"
    return "No Bet"


# Apply the Poisson probability calculation function
df['Probability'] = df.apply(calculate_poisson_probability, axis=1)

# Apply the comparison function to populate "Does Over/Under Match?" column
df['Does Over/Under Match?'] = df.apply(compare_sides, axis=1)

# Apply the Break Even Odds calculation function
df['Break Even Odds'] = df.apply(calculate_break_even_odds, axis=1)

# Apply the No Hold Probability calculation function
df['No Hold Probability'] = df.apply(calculate_no_hold_probability, axis=1)

# Apply the No Hold Line calculation function
df['No Hold Line'] = df.apply(calculate_no_hold_line, axis=1)

# Apply the Action to Take calculation function
df['Action to take'] = df.apply(calculate_action_to_take, axis=1)

# Filter rows where "Action to take" is "Bet"
filtered_df = df[df['Action to take'] == 'Bet']

# Display the DataFrame with updated "Probability" and "Break Even Odds"
# columns
print(df)
