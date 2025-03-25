import pandas as pd
from scipy import stats

df = pd.read_csv("hitter.csv", index_col=["playerid"]) #Preseason Hitters

df['Barrel%'] = df['Barrel%'] = df['Barrel%'].str.rstrip('%').astype('float')

filter= df[(df['PA'] > 250) & (df['HR'] > 5)]

numbers = df.select_dtypes(include='number').columns
df[numbers] = df[numbers].apply(stats.zscore)

df['Total Z-Score']= df.sum(axis = 1)

rounded_df = df.round(decimals=2).sort_values(by='Total Z-Score', ascending=False)

#rounded_df.to_excel("Hitters.xlsx", sheet_name='Hitters')
rounded_df.to_csv("ZHitters.csv")