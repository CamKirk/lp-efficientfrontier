import pandas as pd 
import os
import random

def import_data_dir(directory):

    file_list = os.listdir(directory)

    df_dict = {}
    for file in file_list:

        if file.endswith(".csv"):
            name = file.split(".")[0]

            series = pd.read_csv(f"{directory}/{file}", index_col="Date", parse_dates=True,
                                infer_datetime_format=True)[" Close/Last"]
            
            series = series.str.replace("$","").astype("float")
            df_dict[name]  = series

    combined_df = pd.concat(df_dict.values(), axis="columns", join="inner")

    combined_df.columns = df_dict.keys()
    
    return combined_df


# need to 
def monte_carlo():
    results = pd.DataFrame({
    "Weights":[],
    "Total_Return":[],
    "Risk":[],
    "Sharpe":[]
    })

    trials = 5000
    risk_free_rate = 0.0072

    for run in range(trials):
        
        
        preweight = [random.random() for w in range(6)]
        weightsum = sum(preweight)
        weights = [w/weightsum for w in preweight]
        
        initial = 10000
        portfolio_returns = returns.dot(weights)
        cumulative_returns = (1+portfolio_returns).cumprod()
        
        risk = portfolio_returns.std()
    #     final_value = (initial * cumulative_returns)[-1] # in case you want this
        total_return = cumulative_returns[-1]
        
        results=results.append({
            "Weights":weights,
            "Total_Return": total_return,
            "Risk": risk,
            "Sharpe": (total_return-risk_free_rate)/risk
        }, ignore_index=True)

        return results