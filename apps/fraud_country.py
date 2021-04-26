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

pv = pd.pivot_table(data, index=['IP_country'], values=['class'], aggfunc=[np.sum, len]).sort_values(by=('sum','class'), ascending=False)[:20]

trace1 = go.Bar(x=pv.index, y=pv[('len', 'class')], name='Valid')
trace2 = go.Bar(x=pv.index, y=pv[('sum', 'class')], name='Fraud')


layout = html.Div(
    children=[
        html.H1(children="Fraud Detection"),
        html.P(
            children="Shows the top 20 countries with the most fraundulent transactions.",
        ),
        dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2],
            'layout':
            go.Layout(title='Top 20 countries with the most fraudulent activity', barmode='stack')
        })
    ]
)