'''
Downlaad team batting stats as csv from Baseball Reference
'''

import pandas as pd

df = pd.read_csv('mlbbat.csv')

df['OffenseCreated'] = (df['TB'] + df['BB']) / 4
df['Rank'] = df['OffenseCreated'].rank(ascending = False)
cols = ['Rank', 'OffenseCreated']
df[cols] = df[cols].applymap(int)

sorted_df = df[['Rank', 'Tm', 'BatAge', 'R/G', 'OffenseCreated']]
sorted_df = sorted_df.sort_values(by='OffenseCreated', ascending=False)

print(sorted_df)