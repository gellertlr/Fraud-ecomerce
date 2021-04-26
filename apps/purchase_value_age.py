import dash_html_components as html
import dash_core_components  as dcc
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('./dashboard_mapped.csv')

pv = pd.pivot_table(data, index=['age'], values=['purchase_value'])

trace1 = px.line(pv, x=pv.index, y='purchase_value', hover_data=['purchase_value'], title='Age vs Purchase value')

layout = html.Div(
    children=[
        html.H1(children="Fraud Detection"),
        html.P(
            children="Shows the average purchase value for an age.",
        ),
        dcc.Graph(
        id='age_scatter',
        figure=trace1)
    ]
)