import dash_html_components as html
import dash_core_components  as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import numpy as np
import pickle
from datetime import date

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

import plotly.graph_objs as go
import plotly.express as px

with open('./mapping.pkl', 'rb') as f:
    mapping = pickle.load(f)

with open('./risk_mapping.pkl', 'rb') as f:
    risk_mapping = pickle.load(f)

with open('./log_mod.pkl', 'rb') as f:
    log_mod = pickle.load(f)

with open('./rf_mod.pkl', 'rb') as f:
    rf_mod = pickle.load(f)

with open('./knn_mod.pkl', 'rb') as f:
    knn_mod = pickle.load(f)

models = {'Logistic Regression': log_mod,
          'Random Forest': rf_mod,
          'k-NN': knn_mod}

country = ['Japan', 'United States', 'Unknown', 'Canada', 'China', 'Brazil',
       'India', 'Argentina', 'United Kingdom', 'South Africa', 'Germany',
       'Mexico', 'Sweden', 'Korea Republic of', 'Peru', 'Portugal',
       'Bangladesh', 'France', 'Taiwan; Republic of China (ROC)',
       'Russian Federation', 'Belgium', 'Denmark', 'Netherlands',
       'Iran (ISLAMIC Republic Of)', 'Spain', 'Gabon', 'Saudi Arabia',
       'Hong Kong', 'Georgia', 'Syrian Arab Republic', 'Turkey',
       'New Zealand', 'European Union', 'Australia', 'Ukraine', 'Austria',
       'Israel', 'Malaysia', 'Greece', 'Italy', 'Norway', 'Poland',
       'Venezuela', 'Thailand', 'Chile', 'Morocco', 'Finland', 'Hungary',
       'Indonesia', 'Colombia', 'Ecuador', 'Lithuania', 'Switzerland',
       'Viet Nam', 'Nigeria', 'Egypt', 'Seychelles', 'Kazakhstan',
       'Kenya', 'Moldova Republic of', 'Trinidad and Tobago', 'Qatar',
       'Bolivia', 'Bulgaria', 'Romania', 'Croatia (LOCAL Name: Hrvatska)',
       'Cyprus', 'Czech Republic', 'Algeria', 'Kyrgyzstan', 'Singapore',
       'Guam', 'United Arab Emirates', 'Paraguay', 'Tunisia',
       'Dominican Republic', 'Pakistan', 'Malta', 'Nicaragua', 'Estonia',
       'Mozambique', 'Namibia', 'Macedonia', 'Costa Rica', 'Cuba',
       'Ireland', 'Albania', 'Oman', 'Uruguay', 'Lebanon', 'Puerto Rico',
       'Maldives', 'Turkmenistan', 'Barbados', 'Iceland', 'Philippines',
       'Kuwait', 'Panama', 'New Caledonia', 'Guatemala', 'Ghana',
       'Latvia', 'Malawi', 'Slovenia', 'Senegal',
       'Libyan Arab Jamahiriya', 'Cambodia', 'Belize', 'Mauritius',
       'Tanzania United Republic of', 'Slovakia (SLOVAK Republic)',
       'Iraq', 'El Salvador', 'Bosnia and Herzegowina', 'Serbia',
       'Luxembourg', 'Nepal', 'Belarus', "Cote D'ivoire", 'Djibouti',
       'Armenia', 'Sri Lanka', 'Sudan', 'Jamaica', 'Rwanda', 'Uzbekistan',
       'Jordan', 'Bahrain', 'Azerbaijan', 'South Sudan',
       'Virgin Islands (U.S.)', 'Congo', 'Angola', 'Mongolia', 'Uganda',
       'Haiti', 'Papua New Guinea', 'Gibraltar', 'Cameroon',
       'Palestinian Territory Occupied', 'Myanmar', 'Brunei Darussalam',
       'Zambia', 'Saint Kitts and Nevis', 'Reunion', 'Botswana',
       'Dominica', 'Burkina Faso', 'Montenegro', 'Macau', 'Faroe Islands',
       'Zimbabwe', 'Honduras', 'Monaco',
       'Congo The Democratic Republic of The', 'Cayman Islands', 'Niger',
       'Antigua and Barbuda', 'Lesotho', 'Fiji', 'Afghanistan', 'Bhutan',
       'Bermuda', 'Curacao', 'Ethiopia', 'Vanuatu',
       "Lao People's Democratic Republic",
       'British Indian Ocean Territory', 'Bahamas', 'Madagascar',
       'Bonaire; Sint Eustatius; Saba', 'Liechtenstein', 'Gambia',
       'Benin', 'Cape Verde', 'Tajikistan', 'Saint Martin', 'Yemen',
       'San Marino', 'Burundi', 'Nauru', 'Guadeloupe']

layout = html.Div([
    dbc.Container([
    html.P("Select Model:"),
    dcc.Dropdown(
        id='model-name',
        options=[{'label': x, 'value': x} 
                 for x in models],
        value='Logistic Regression',
        clearable=False
    ),
    dcc.Graph(id="graph"),
    html.P("Source:"),
    dcc.Dropdown(
        id='source',
        options=[{'label': x, 'value': x} 
                 for x in ['SEO', 'Direct', 'Ads']],
        value='SEO',
        clearable=False
    ),
    html.P("Browser:"),
    dcc.Dropdown(
        id='browser',
        options=[{'label': x, 'value': x} 
                 for x in ['Chrome', 'IE', 'FireFox', 'Safari', 'Opera']],
        value='Chrome',
        clearable=False
    ),
    html.P("Gender:"),
    dcc.Dropdown(
        id='gender',
        options=[{'label': x, 'value': x} 
                 for x in ['M','F']],
        value='M',
        clearable=False
    ),
    html.P("Age:"),
    dcc.Slider(
        id='age-slider',
        min=18,
        max=80,
        step=1,
        value=40,
        marks={
        18: '18',
        30: '25',
        50: '40',
        65: '65',
        80: '80'
    },
    ),
    html.Div(id='slider-output-container'),
    html.P("Sign up date:"),
    dcc.DatePickerSingle(
        id='signup-date',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date(2021, 4, 30),
        initial_visible_month=date(2017, 8, 5),
        date=date(2017, 8, 25),
        display_format='YYYY-MM-DD'
    ),
    html.P("Sign up time:"),
    dbc.Row(
        [
            dcc.Dropdown(
                id='hour-signup',
                options=[{'label': x, 'value': x} 
                        for x in range(0,25)],
                value='0',
                clearable=False
            ),
            html.P("  :  "),
            dcc.Dropdown(
                id='minute-signup',
                options=[{'label': x, 'value': x} 
                        for x in range(0,60)],
                value='0',
                clearable=False
            )
        ]
    ),
    html.P("Time difference between sign up and purchase:"),
    dcc.Slider(
        id='time-diff',
        min=1,
        max=90000,
        step=100,
        value=10000,
        marks={
        20000: '20000',
        40000: '40000',
        60000: '60000',
        80000: '80000'
    },
    ),
    html.P("Country:"),
    dcc.Dropdown(
        id='country',
        options=[{'label': x, 'value': x} 
                 for x in country],
        value='Japan',
        clearable=False
    ),
    html.P("")
    ])
])

@app.callback(
    Output("graph", "figure"), 
    [Input('model-name', "value")],
    [Input('source', "value")],
    [Input('browser', "value")],
    [Input('gender', "value")],
    [Input('age-slider', "value")],
    [Input('signup-date', "value")],
    [Input('hour-signup', "value")],
    [Input('minute-signup', "value")],
    [Input('time-diff', "value")],
    [Input('country', "value")],
    )
def train_and_display(name, source, browser, gender, age, signup_date, signup_hour, signup_min, time_diff, country):

    if signup_date is not None:
        date_object = date.fromisoformat(signup_date)
        date_string = date_object.strftime('%B %d, %Y')
        print(date_string)

    if time_diff < 60:
        fast_purchase = 1
    else:
        fast_purchase = 0

    # input_data = {'source':[source, source], 'browser':[browser, browser], 'sex':[gender, gender],
    #    'age':[int(age), int(age)],  'signup_time_month':[1, 1],
    #    'signup_time_day': [1,1],
    #    'purchase_time_month':[1,1], 'purchase_time_day':[1,1], 'fast_purchases':[fast_purchase, fast_purchase], 'count_device_from_countries':[1,1], 'country_risk': [country, country], 'time_difference':[int(time_diff), int(time_diff)]}

    input_data = {'source':[str(source)], 'browser':[str(browser)],'sex':[str(gender)],
       'age':[int(age)],  'signup_time_month':[1],
       'signup_time_day': [1],
       'purchase_time_month':[1], 'purchase_time_day':[1], 'fast_purchases':[fast_purchase], 'count_device_from_countries':[1], 'country_risk': [country], 'time_difference':[int(time_diff)]}

    data = pd.DataFrame.from_dict(input_data)
    data['sex'] = data['sex'].map(mapping[3])
    data['browser'] = data['browser'].map(mapping[2])
    data['source'] = data['source'].map(mapping[1])
    data['country_risk'] = data['country_risk'].map(risk_mapping)
    data['country_risk'] = data['country_risk'].map(mapping[8])
    data['age'] = np.sqrt(data['age'])

    model = models[name]
    prob = model.predict_proba(data)[:,1][0]
    if name == 'Logistic Regression':
        predict = [1 if prob > 0.5 else 0]
    elif name == 'k-NN':
        predict = [1 if prob > 0.3333 else 0]
    else:
        predict = [1 if prob > 0.5 else 0]
    if predict[0] == 1:
        results = {"Predict":[0, predict[0]], "Probability":[0, prob], "Decision":["Valid", "Fraud"]}
        prob_df = pd.DataFrame.from_dict(results)
    else:
        results = {"Predict":[predict[0], 1], "Probability":[prob, 0], "Decision":["Valid", "Fraud"]}
        prob_df = pd.DataFrame.from_dict(results)
    fig = px.bar(prob_df, x="Predict", y="Probability", color='Decision', title=name)
    fig.update_yaxes(range=[0,1])
    fig.update_xaxes(range=[0,1])
    return fig