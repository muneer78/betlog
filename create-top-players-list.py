import pandas as pd

dffghit = pd.read_csv('fg.csv')
dffgpit = pd.read_csv('fg2.csv')
dfadp = pd.read_csv('adp.csv')

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

dfadp = dfadp.drop(['ESPN','CBS','RTS','NFBC','FT'], axis=1)

df1 = dfadp.merge(dffgpit[['Key', 'playerid']], on=["Key"], how="left").merge(dffghit[['Key', 'playerid']], on=["Key"], how="left")
df1 = df1.fillna(value=0)
df1['playerid'] = df1['playerid_x'].mask(df1['playerid_x'].eq(0), df1['playerid_y'])
df1['playerid'] = df1['playerid'].astype(int)

df1 = df1[['Player', 'playerid']]
result = df1[:75]

result.to_csv('excluded.csv', index=False)