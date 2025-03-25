import pandas as pd

df = pd.read_csv("Fangraphs Leaderboard (3).csv", index_col=["playerid"]) #Hitters Last 14 Days

df.columns = df.columns.str.replace('[+,-,%,]', '')
df.rename(columns={'K%-':'K','BB%-':'BB'}, inplace=True)
df.fillna(0)

df['Barrel'] = df['Barrel'] = df['Barrel'].str.rstrip('%').astype('float')

filters = df[(df['wRC'] >135) & (df['OPS'] > .8) & (df['K'] < 95) & (df['BB'] > 100) & (df['Off'] > 3) & (df['Barrel'] > 10)].sort_values(by='Off', ascending=False)

print (filters)

filters.to_excel("hitlast14.xlsx", sheet_name='Hitters Last 14 Days')