import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

from data import *
from style import *


df_forecasts = fl.get_forecasts()
df_daily = dl.get_data('KA')

fig1 = go.Figure()
fig1.add_traces([
    go.Scatter(
        x=df_forecasts['date'],
        y=df_forecasts['delta confirmed'],
        name='Forecast',
        **scatter_style
    ),
    go.Scatter(
        x=df_daily['date'],
        y=df_daily['delta.confirmed'],
        name='Actual',
        **scatter_style
    )
])
fig1.update_layout(xaxis=xaxis)

fig2 = go.Figure()
fig2.add_traces([
    go.Scatter(
        x=df_forecasts['date'],
        y=df_forecasts['delta deceased'],
        name='Forecast',
        **scatter_style
    ),
    go.Scatter(
        x=df_daily['date'],
        y=df_daily['delta.deceased'],
        name='Actual',
        **scatter_style
    )
])
fig2.update_layout(xaxis=xaxis)


tab3_content = html.Div([
    dbc.Row([
        dbc.Col(
            html.H5('Karnataka Daily Confirmed Cases Forecast', style={'text-align': 'center'})
        ),
        dbc.Col(
            html.H5('Karnataka Daily Deceased Forecast', style={'text-align': 'center'})
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Spinner(
                id="loading-confirmed",
                children=dcc.Graph(
                    id='confirmed',
                    animate=False,
                    style={'width': '90hh', 'height': '75vh'},
                    figure=fig1
                ),
                spinner_style={'color': "primary", 'type': "grow"},
            ),
        ),
        dbc.Col(
            dbc.Spinner(
                id="loading-deaths",
                children=dcc.Graph(
                    id='deaths',
                    animate=False,
                    style={'width': '90hh', 'height': '75vh'},
                    figure=fig2
                ),
                spinner_style={'color': "primary", 'type': "grow"},
            ),
        ),
    ]),
], id='tab3-content')

tab3_body = dbc.Card(
    dbc.CardBody([tab3_content], id='tab3-body'),
)