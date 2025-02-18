import pandas as pd 

df= pd.read_excel("C:/Xiaomi Cloud/Desktop/1.xlsx").fillna('')

for i in range(len(df)):
    name = df.iloc[i, 0]
    descr = df.iloc[i,1]

    print(name)
    print(descr)
    
    