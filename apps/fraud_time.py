import dash_html_components as html
import dash_core_components  as dcc
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('./dashboard_mapped.csv')

pv = pd.pivot_table(data, index=['time_difference'], values=['class'], aggfunc='sum').sort_values(by="class", ascending=False)[:200]
trace1 = px.scatter(pv, x=pv.index, y='class', title='Top 20 time difference vs count fraud')

layout = html.Div(
    
    children=[
        html.H1(children="Fraud Detection"),
        html.P(
            children="Top 20 values for difference in signup and purchase time vs number of fraudulent transactions.",
        ),
        dcc.Graph(
        id='age_scatter',
        figure=trace1)
    ]
)