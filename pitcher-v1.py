import pandas as pd
from scipy import stats
import numpy as np

df = pd.read_csv("pitcher.csv", index_col=["playerid"]) #Preseason Pitchers

df['F-Strike%'] = df['F-Strike%'] = df['F-Strike%'].str.rstrip('%').astype('float')
df['Barrel%'] = df['Barrel%'] = df['Barrel%'].str.rstrip('%').astype('float')
df['CSW%'] = df['CSW%'] = df['CSW%'].str.rstrip('%').astype('float')
df['SwStr%'] = df['SwStr%'] = df['SwStr%'].str.rstrip('%').astype('float')
df['HardHit%'] = df['HardHit%'] = df['HardHit%'].str.rstrip('%').astype('float')

expr1= (df['GS']/(df['ER']*(df['GS']/df['G']))).fillna(0).replace([np.inf, -np.inf], 0)
expr2= (df['IP']*(df['GS']/df['G'])).fillna(0)
expr3= (((df['GS']+df['G'])/(2*df['G']))**2).fillna(0)
expr4= (expr1*expr2*expr3)
#df['EstimatedQS']=(expr1*expr2*expr3)
#df['Estimated QS']= (expr1*expr2*expr3).fillna(0).astype(float)
df['EstimatedQS']= expr4

numbers = df.select_dtypes(include='number').columns
df[numbers] = df[numbers].apply(stats.zscore)

df['EstimatedQS']= df['EstimatedQS']*1.5
df['Total Z-Score']= df.sum(axis = 1)
df['Total Z-Score']= df['Total Z-Score']*3.5


rounded_df = df.round(decimals=2).sort_values(by='Total Z-Score', ascending=False)

rounded_df.to_excel("Pitchers.xlsx", sheet_name='Pitchers')