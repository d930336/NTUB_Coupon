import datetime
import pandas as pd

df = pd.read_excel("KFC1028.xlsx").dropna(thresh=3)

df["add_time"] = datetime.datetime.now()

print(df)

df.to_excel("KFC1101.xlsx")