import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd


sys.path.append('..')
from consumer.api_consumer import DataLoader

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = DataLoader().get_data(state_codes="TT")

column1_color = 'Red'
column2_color = 'green'
column3_color = 'blue'

xaxis = dict(
    rangeselector=dict(
        buttons=list([
            dict(count=1,
                 label="1m",
                 step="month",
                 stepmode="backward"),
            dict(count=6,
                 label="6m",
                 step="month",
                 stepmode="backward"),
            dict(count=1,
                 label="YTD",
                 step="year",
                 stepmode="todate"),
            dict(count=1,
                 label="1y",
                 step="year",
                 stepmode="backward"),
            dict(step="all")
        ])
    ),
    rangeslider=dict(
        visible=False
    ),
    type="date"
)

fig1 = go.Figure()
fig1.add_trace(
    go.Scatter(
        mode='lines+markers',
        x=df['date'],
        y=df['delta.confirmed'],
        marker=dict(
            color=column1_color,
            size=2,
        ),
        showlegend=False,
    )
)
fig1.update_layout(
    title="Daily Confirmed Cases",
    xaxis=xaxis,
    title_x=0.5
    # plot_bgcolor='rgba(255, 255, 255, 255)',
)

fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        mode='lines+markers',
        x=df['date'],
        y=df['delta.tested'],
        marker=dict(
            color=column2_color,
            size=2,
        ),
        showlegend=False,
    )
)
fig2.update_layout(
    title="Daily Tests",
    xaxis=xaxis,
    title_x=0.5
    # plot_bgcolor='rgba(255, 255, 255, 255)',
)

fig3 = go.Figure()
fig3.add_trace(
    go.Scatter(
        mode='lines+markers',
        x=df['date'],
        y=df['delta.vaccinated1'],
        marker=dict(
            color=column3_color,
            size=2,
        ),
        showlegend=False,
    )
)
fig3.update_layout(
    title="Daily Vaccinated (first)",
    xaxis=xaxis,
    title_x=0.5
    # plot_bgcolor='rgba(255, 255, 255, 255)',
)

app.layout = dbc.Container([
    dbc.Jumbotron([
        html.H1(children="Covid 19: India Analysis Dashboard", style={"text-align": "center"}),
    ], fluid=True),
    html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id="Daily Confirmed Cases",
                    figure=fig1
                ),
                width=4
            ),
            dbc.Col(
                dcc.Graph(
                    id="Daily Tests",
                    figure=fig2
                ),
                width=4
            ),
            dbc.Col(
                dcc.Graph(
                    id="Daily Vaccinated",
                    figure=fig3,
                ),
                width=4
            )
        ], align="start", no_gutters=True),
        # dbc.Row([
        #     dbc.Col(html.Div("One of three columns")),
        #     dbc.Col(html.Div("One of three columns")),
        #     dbc.Col(html.Div("One of three columns")),
        # ], align="center"),
        # dbc.Row([
        #     dbc.Col(html.Div("One of three columns")),
        #     dbc.Col(html.Div("One of three columns")),
        #     dbc.Col(html.Div("One of three columns")),
        # ], align="end"),
        # dbc.Row([
        #     dbc.Col(html.Div("One of three columns"), align="start"),
        #     dbc.Col(html.Div("One of three columns"), align="center"),
        #     dbc.Col(html.Div("One of three columns"), align="end"),
        # ])
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=5555)