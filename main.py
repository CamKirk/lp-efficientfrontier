import pandas as pd
import os
import random

file_list = os.listdir("data")


# grabbing all files
df_dict = {}
for file in file_list:
    name = file.split(".")[0]
    
    series = pd.read_csv(f"./data/{file}", index_col="Date", parse_dates=True, infer_datetime_format=True)[" Close/Last"]
    
    series = series.str.replace("$","").astype("float")
    df_dict[name]  = series

# forming raw dataframe
df = pd.concat(df_dict.values(), axis="columns", join="inner")
df.columns = df_dict.keys()

# calc returns
returns = df.pct_change()

# monte carlo random guesses
trials = 500

results = pd.DataFrame({
    "Weights":[],
    "Final_Value":[],
    "Risk":[]
})

for run in range(trials):
    
    
    preweight = [random.random() for w in range(6)]
    weightsum = sum(preweight)
    weights = [w/weightsum for w in preweight]
    
    initial = 10000
    portfolio_returns = returns.dot(weights)
    cumulative_returns = (1+portfolio_returns).cumprod()
    
    results=results.append({
        "Weights":weights,
        "Final_Value":(initial * cumulative_returns)[-1],
        "Risk": portfolio_returns.std()
    }, ignore_index=True)
    
results.plot(kind="scatter", x="Risk", y="Final_Value")
