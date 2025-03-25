'''
1. Go to Average Draft Position on FantasyPros and export files as csv. Update references in script.
'''

import pandas as pd

dffghit = pd.read_csv('pitcher.csv')
dffgpit = pd.read_csv('hitter.csv')
dfadp = pd.read_csv('FantasyPros_2024_Overall_MLB_ADP_Rankings.csv')

dflist = [dffgpit, dffghit, dfadp]
for index in range(len(dflist)):
    dflist[index].replace(r'[^\w\s]|_\*', '', regex=True, inplace = True)
    dflist[index].replace(' Jr', '', regex=True, inplace = True)
    dflist[index].replace(' II', '', regex=True, inplace = True)

dfadp = dfadp.astype(str)

func = lambda x: ''.join([i[:3] for i in x.strip().split(' ')])
dffgpit['Key'] = dffgpit.Name.apply(func)
dfadp['Key'] = dfadp.Player.apply(func)
dffghit['Key'] = dffghit.Name.apply(func)

dfadp = dfadp.drop(['ESPN','CBS','RTS','NFBC'], axis=1)

df1 = dfadp.merge(dffgpit[['Key', 'PlayerId']], on=["Key"], how="left").merge(dffghit[['Key', 'PlayerId']], on=["Key"], how="left")
df1 = df1.fillna(value=0)
df1['PlayerId'] = df1['PlayerId_x'].mask(df1['PlayerId_x'].eq(0), df1['PlayerId_y'])
df1['PlayerId'] = df1['PlayerId'].astype(int)

df1 = df1[['PlayerId','Player']]
result = df1[:100]

result.to_csv('excluded.csv', index=False)