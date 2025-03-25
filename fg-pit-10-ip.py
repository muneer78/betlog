import pandas as pd

df = pd.read_csv("Fangraphs Leaderboard.csv", index_col=["playerid"]) #10 IP Pitchers

df.columns = df.columns.str.replace('[+,-,%,]', '')
df.rename(columns={'K-BB':'KMinusBB','K/BB':'KToBB', 'HR/9':'HRPer9', 'xFIP-':'XFIPMinus'}, inplace=True)
df.fillna(0)

df['KMinusBB'] = df['KMinusBB'] = df['KMinusBB'].str.rstrip('%').astype('float')
df['Barrel'] = df['Barrel'] = df['Barrel'].str.rstrip('%').astype('float')
df['CSW'] = df['CSW'] = df['CSW'].str.rstrip('%').astype('float')

filters1 = df[(df['xERA'] < 3) & (df['Barrel'] < 7) & (df['KMinusBB'] > 20) & (df['Starting'] > 5) & (df['GS'] > 1)].sort_values(by='Starting', ascending=False)
filters2 = df[(df['xERA'] < 3) & (df['Barrel'] < 7) & (df['KMinusBB'] > 30) & (df['Relieving'] > 1)].sort_values(by='Relieving', ascending=False)

finalSP=(filters1.drop(['Relieving','SV'],axis=1))
finalRP=(filters2.drop(['Starting','GS'],axis=1))

finalSP.to_excel("pitchingSP10ip.xlsx", sheet_name='StartersSeason')
finalRP.to_excel("pitchingRP10ip.xlsx", sheet_name='RelieversSeason')