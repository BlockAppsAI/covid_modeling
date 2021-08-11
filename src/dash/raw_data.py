import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from data import *


column_dt = {
    'tpr': 'Test Positivity Rate %',
    'cfr': 'Case Fatality Rate %',
    'delta.confirmed': 'Daily Confimed Cases',
    'delta7.confirmed': 'Daily Confirmed Cases (7 Day Average)',
    'total.confirmed': 'Total Confirmed Cases',
    'delta.recovered': 'Daily Recovered',
    'delta7.recovered': 'Daily Recovered (7 Day Average)',
    'total.recovered': 'Total Recovered', 
    'delta.deceased': 'Daily Deceased', 
    'delta.tested': 'Daily Tested',
    'delta7.deceased': 'Daily Deceased (7 Day Average)',
    'delta7.tested': 'Daily Tested (7 Day Average)',
    'total.deceased': 'Total Deceased',
    'total.tested': 'Total Tested',
    'delta.other': 'Daily (Other)',
    'delta7.other': 'Daily (Other) (7 Day Average)',
    'total.other': 'Total Other',
    'delta.vaccinated1': 'Daily Vaccinated 1',
    'delta7.vaccinated1': 'Daily Vaccinated 1 (7 Day Average)',
    'total.vaccinated1': 'Total Vaccinated 1',
    'delta.vaccinated2': 'Daily Vaccinated 2',
    'delta7.vaccinated2': 'Daily Vaccinated 2 (7 Day Average)',
    'total.vaccinated2': 'Total Vaccinated 2',
}

dt_column = {
    v: k for k, v in column_dt.items()
}


dt_column_dd = [{
    'label': value, 'value': key
} for key, value in column_dt.items()]


tab1_body = tab1_body = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='geography',
                options=states,
                value=['KA'], #'KL', 'TN', 'MH', 'AP', 'TG'], 
                multi=True,
                placeholder="Select Geographies",
                style={'vertical-align': 'middle', 'marginLeft': 'auto', 'align': 'inline-block'}
            ), width={
                "size": 6, 
                'order': 'first',
                'offset': 0,
            }
        ),
        dbc.Col(
            dcc.Dropdown(
                id='metric',
                options=dt_column_dd,
                value='tpr',
                placeholder="Select A Metric",
                style={'vertical-align': 'middle', 'marginLeft': 'auto', 'align': 'inline-block'}
            ), width={"size": 3, "offset": 0, 'order': 'last'},
        ),
    ], style={'marginTop': '0px', 'vertical-align': 'middle'}),

    dbc.Spinner(
        id="loading-1",
        children=dcc.Graph(
            id='geography-metric',
            animate=False,
            style={'width': '90hh', 'height': '75vh'}
        ),
        spinner_style={#"width": "5rem", "height": "5rem", 
                       'color': "primary", 'type': "grow"},
    ),
])