import string
import pandas as pd
import numpy as np

df = pd.read_csv("FanGraphs.csv", header=None)
df2 = pd.DataFrame(df.values.reshape(25,10))
column_names = df2[0:1].values[0]
df3 = df2[1:]
df3.columns = df2[0:1].values[0]
df3.head()

df4['x5'] = [float(x) for x in df4['x5'].values]
df4['x6'] = [float(x) for x in df4['x6'].values]
df4['x7'] = [float(x) for x in df4['x7'].values]

df4.head(n = 5)