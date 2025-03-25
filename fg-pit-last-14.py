import pandas as pd

df = pd.read_csv("Fangraphs Leaderboard (5).csv", index_col=["playerid"]) #Pitchers Last 14 Days

df.columns = df.columns.str.replace('[+,-,%,]', '')
df.rename(columns={'K/BB':'KToBB', 'HR/9':'HRPer9', 'xFIP-':'XFIPMinus'}, inplace=True)
df.fillna(0)

df['Barrel'] = df['Barrel'] = df['Barrel'].str.rstrip('%').astype('float')
df['CSW'] = df['CSW'] = df['CSW'].str.rstrip('%').astype('float')

filters1 = df[(df['Barrel'] < 7) & (df['Starting'] > 5) & (df['GS'] > 1)].sort_values(by='Starting', ascending=False)
filters2 = df[(df['Barrel'] < 7) & (df['Relieving'] > 1)].sort_values(by='Relieving', ascending=False)

finalSP=(filters1.drop(['Relieving','SV'],axis=1))
finalRP=(filters2.drop(['Starting','GS'],axis=1))

finalSP.to_excel("pitchingSPlast14.xlsx", sheet_name='StartersSeason')
finalRP.to_excel("pitchingRPlast14.xlsx", sheet_name='RelieversSeason')