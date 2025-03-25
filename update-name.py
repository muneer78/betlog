import pandas as pd

df_excluded = pd.read_csv("fbexcluded.csv")

def clean_player_data(df):
    df['PLAYER NAME'] = df['PLAYER NAME'].replace(r"[^\w\s]|_\*| Jr| III", "", regex=True)
    return df[['PLAYER NAME']]  # Select only the 'PLAYER NAME' column

df_excluded = clean_player_data(df_excluded)

df_excluded.to_csv('fbexcluded.csv', index=False)