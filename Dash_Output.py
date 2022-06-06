import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pickle
import urllib.request

import functions_to_extract_info_from_json as myf

import joblib
loaded_rf = joblib.load("./random_forest.joblib") #load the pretrained model



def make_prediction(df_row):
    #input: tail of df
    stats_for_predict = df_row.drop(["time","win_probability"],axis=1)
    df_row["win_probability"] = loaded_rf.predict_proba(stats_for_predict)[0][1]
    return df_row

df_current = pd.DataFrame([{}])

try:
    df_new_stats = pd.DataFrame([myf.current_stats(myf.get_live_data())])
    df_current = make_prediction(df_new_stats)
    #df_current = df_current.append(df_new_stats)
except urllib.request.URLError:
    pass
print(df_current)

pd.options.plotting.backend = "plotly"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],update_title = None )
app.title = "Outcome Prediction"
app.layout = html.Div([
    html.H1("Real time outcome prediction:"),
    dcc.Interval(
        id='interval-component',
        interval=5000, # in milliseconds
        n_intervals=0
                ),
    dcc.Graph(id='graph',
              config={
                      'staticPlot': False,     
                      'scrollZoom': True,      
                      'doubleClick': 'reset',  
                      'showTips': False,       
                      'displayModeBar': True,  
                      'watermark': False,
                        },
              ),
    html.P(" "),
    html.P("Algorithm is evaluating live match data: such as creep score, K/D/A, Dragons, Tower achquisiton of both teams etc."),
    html.P("Live data is inpreted as match state at 15 minute mark."),
    html.P("Hence most accurate result will be around that time.")
])


@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig(value):
    
    global df_current
    
    try:
        df_new_stats = pd.DataFrame([myf.current_stats(myf.get_live_data())])
        df_new_stats = make_prediction(df_new_stats)
        df_current = df_current.append(df_new_stats)
        print(df_current)
    except urllib.request.URLError:
        pass
    fig = df_current.plot(x="time",y="win_probability", template = 'plotly_dark')
    return(fig)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
























#df_match_example.to_csv("df_match_example", encoding='utf-8')