import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

from apps import home, fraud_country, fraud_month, purchase_value_age, fraud_time, model


dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Fraud per Country", href="/fraud_country"),
        dbc.DropdownMenuItem("Fraud per Month", href="/fraud_month"),
        dbc.DropdownMenuItem("Age vs Purchase value", href="/purchase_value_age"),
        dbc.DropdownMenuItem("Time difference for fraud", href="/fraud_time"),
        dbc.DropdownMenuItem("Model", href="/model"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/icon.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Fraud Detection Dashboard", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/fraud_country':
        return fraud_country.layout
    elif pathname == '/fraud_month':
        return fraud_month.layout
    elif pathname == '/purchase_value_age':
        return purchase_value_age.layout
    elif pathname == '/fraud_time':
        return fraud_time.layout
    elif pathname == '/model':
        return model.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)