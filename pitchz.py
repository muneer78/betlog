import pandas as pd
from scipy import stats
import numpy as np

df = pd.read_csv("pitcher.csv", index_col=["playerid"]) #Preseason Pitchers


expr1= (df['GS']/(df['ER']*(df['GS']/df['G']))).fillna(0).replace([np.inf, -np.inf], 0)
expr2= (df['IP']*(df['GS']/df['G'])).fillna(0)
expr3= (((df['GS']+df['G'])/(2*df['G']))**2).fillna(0)
expr4= (expr1*expr2*expr3)
#df['EstimatedQS']=(expr1*expr2*expr3)
#df['Estimated QS']= (expr1*expr2*expr3).fillna(0).astype(float)
df['ER']=(df['ER']*-1)
df['EstimatedQS']= expr4
df=df.drop(['ER','GS', 'G'],axis=1) 

df['F-Strike%'] = df['F-Strike%'].str.rstrip('%').astype('float')
df['Barrel%'] = df['Barrel%'].str.rstrip('%').astype('float')
df['CSW%'] = df['CSW%'].str.rstrip('%').astype('float')
df['SwStr%'] = df['SwStr%'].str.rstrip('%').astype('float')
df['HardHit%'] = df['HardHit%'].str.rstrip('%').astype('float')
df['Barrel%']= df['Barrel%']*-1

numbers = df.select_dtypes(include='number').columns
df[numbers] = df[numbers].apply(stats.zscore)
df['SV']=df['SV']*1.5
df['Barrel%']= df['Barrel%']*1.5
df['xFIP-']= df['xFIP-']*1.5
df['SwStr%']= df['SwStr%']*1.5
df['F-Strike%']= df['F-Strike%']*1.5
df['CSW%']= df['CSW%']*1.5
df['K%+']= df['K%+']*5
df['BB%+']= df['BB%+']*5
df['EstimatedQS']= df['EstimatedQS']*5
# numbers2 = df[['SV', 'xFIP-', 'SV', 'SwStr%', 'F-Strike%', 'Barrel%','CSW%','K%+', 'BB%+', 'EstimatedQS']]
#df[numbers2]= (float(df[numbers2]))*2

df['Total Z-Score']= df.sum(axis = 1)
#df['Total Z-Score']= df['Total Z-Score']

rounded_df = df.round(decimals=2).sort_values(by='Total Z-Score', ascending=False)

#rounded_df.to_excel("Pitchers.xlsx", sheet_name='Pitchers')

print(rounded_df)