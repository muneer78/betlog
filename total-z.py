import pandas as pd

#hitters = pd.ExcelFile('Hitters.xlsx')
#pitchers = pd.ExcelFile('Pitchers.xlsx')

hitters='Hitters.xlsx'
pitchers='Pitchers.xlsx'

df1= pd.read_excel(hitters)
df2= pd.read_excel(pitchers)

df3=df1[['Name','Total Z-Score']]
df4=df2[['Name','Total Z-Score']]

df5= df3.append(df4[['Name','Total Z-Score']]).sort_values(by='Total Z-Score', ascending=False)

df5.to_excel("TotalZScore.xlsx", sheet_name='Total Z-Scores')