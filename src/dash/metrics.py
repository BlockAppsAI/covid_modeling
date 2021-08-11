import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from data import *


column_dt = {
    'rt': 'Reproduction Number - R0(t)'
    'dt': 'Doubling Time',
}

dt_column = {
    v: k for k, v in column_dt.items()
}


dt_column_dd = [{
    'label': value, 'value': key
} for key, value in column_dt.items()]


tab2_body = html.Div([
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
                id='analysis-metric',
                options=dt_column_dd,
                value='delta.confirmed',
                placeholder="Select A Metric",
                style={'vertical-align': 'middle', 'marginLeft': 'auto', 'align': 'inline-block'}
            ), width={"size": 3, "offset": 0, 'order': 'last'},
        ),
    ], style={'marginTop': '0px', 'vertical-align': 'middle'}),

    # dbc.Spinner(
    #     id="loading-1",
    #     children=dcc.Graph(
    #         id='geography-metric',
    #         animate=False,
    #         style={'width': '90hh', 'height': '75vh'}
    #     ),
    #     spinner_style={#"width": "5rem", "height": "5rem", 
    #                    'color': "primary", 'type': "grow"},
    # ),
])