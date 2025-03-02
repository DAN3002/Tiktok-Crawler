import pandas as pd

# Read 2 excel files with sheet names = "chaychungcu"

df1 = pd.read_excel("./output/chaychungcu.xlsx", sheet_name="chaychungcu")
df2 = pd.read_excel("./output/backup.xlsx", sheet_name="chaychungcu")

# convert video_id to string 
df1["video_id"] = df1["video_id"].astype(str)
df2["video_id"] = df2["video_id"].astype(str)

# Find record in df2 that is not in df1 and append to df1
df = pd.concat([df1, df2[~df2["video_id"].isin(df1["video_id"])]])
df.to_excel("./output/chaychungcu_new.xlsx", sheet_name="chaychungcu", index=False)
