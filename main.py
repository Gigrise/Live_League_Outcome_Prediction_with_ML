import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import functions_to_extract_info_from_json as myf
from IPython.display import clear_output
import urllib.request




import joblib
loaded_rf = joblib.load("./random_forest.joblib") #load the pretrained model



def make_prediction(df_row):
    #input: tail of df
    stats_for_predict = df_row.drop(["time","win_probability"],axis=1)
    df_row["win_probability"] = loaded_rf.predict_proba(stats_for_predict)[0][1]
    return df_row

temp = 0
while True:
    clear_output(wait=True)
    try:
        if temp == 0:
            df_current = make_prediction(pd.DataFrame([myf.current_stats(myf.get_live_data())]))
            temp +=1
        else:
            df_new_stats = pd.DataFrame([myf.current_stats(myf.get_live_data())])
            df_new_stats = make_prediction(df_new_stats)
            df_current = df_current.append(df_new_stats)
        print(df_current.plot(x="time",y="win_probability",figsize=(20,7)))
        display(df_current.tail(4))
        plt.show()
        time.sleep(5)
    except urllib.request.URLError:
        pass



#df_match_example.to_csv("df_match_example", encoding='utf-8')
if __name__ == '__main__':
    main()