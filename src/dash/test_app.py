import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd

sys.path.append('..')
from consumer.api_consumer import DataLoader
from style import *


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dl = DataLoader()
states = dl.get_all_states_with_codes()
states = [{'label': key.title(), 'value': value} for key, value in states.items()]

tab1_body = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id="tpr",
                ),
                width=6
            ),
            dbc.Col(
                dcc.Graph(
                    id="cfr",
                ),
                width=6
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id="daily-confirmed",
                ),
                width=6
            ),
            dbc.Col(
                dcc.Graph(
                    id="daily-tests",
                ),
                width=6
            ),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                    id="total-v1",
                ),
                width=6
            ),
            dbc.Col(
                dcc.Graph(
                    id="total-v2",
                ),
                width=6
            ),
        ]),
    ])
])

tab2_body = html.P("I am under construction.")

card = dbc.Card(
    [
        dbc.CardHeader([
            dbc.Tabs(
                [
                    dbc.Tab(label="Daily Data", tab_id="tab-1", tab_style={"marginLeft": "auto"}),
                    dbc.Tab(label="Analysis", tab_id="tab-2"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            ),
            html.Div([
                dcc.Dropdown(
                    id='geography',
                    options=states,
                    value='TT', 
                    style={'vertical-align': 'middle', 'align': 'center', 'marginLeft': 'auto'}
                )
            ], style={'width': '20%', 'align': "inline-block", 'marginTop': '-40px', 'vertical-align': 'middle'})
        ], style={'background-color': colors['background']},),
        dbc.CardBody(tab1_body, id="card-content",),
    ],
)

app.layout = dbc.Container([
    html.H1(children="Covid 19: India Analysis Dashboard", 
            style={'text-align': "center",
                    'color': colors['text'],
                  }),
    html.P(
        "(Data is updated every day at 10:00 AM.)",
        style={'text-align': 'center',}
    ),
    card,
], fluid=True)


@app.callback(
    Output("daily-confirmed", "figure"),
    Output("daily-tests", "figure"),
    Output("total-v1", "figure"),
    Output("total-v2", "figure"),
    Output("tpr", "figure"),
    Output("cfr","figure"),
    Input("geography", "value")
)
def update_plots(geography):

    if geography is None:
        raise PreventUpdate
    else:
        df = dl.get_data(state_codes=geography)

        fig1 = go.Figure()
        fig1.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['delta.confirmed'],
                **scatter_style
            )
        )
        fig1.update_layout(
            title="Daily Confirmed Cases",
            **figure_params
        )
        fig1.update_yaxes(
            autorange=True,
            fixedrange=False
        )

        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['delta.tested'],
                **scatter_style
            )
        )
        fig2.update_layout(
            title="Daily Tests",
            **figure_params
        )
        fig2.update_yaxes(
            autorange=True,
            fixedrange=False
        )

        fig3 = go.Figure()
        fig3.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['total.vaccinated1'],
                **scatter_style
            )
        )
        fig3.update_layout(
            title="Total Vaccinated (first)",
            **figure_params
        )
        fig3.update_yaxes(
            autorange=True,
            fixedrange=False
        )

        fig4 = go.Figure()
        fig4.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['total.vaccinated2'],
                **scatter_style
            )
        )
        fig4.update_layout(
            title="Total Vaccinated (second)",
            **figure_params
        )
        fig4.update_yaxes(
            autorange=True,
            fixedrange=False
        )

        fig5 = go.Figure()
        fig5.add_trace(
            go.Scatter(
                x=df['date'],
                y=100 * df['delta.confirmed'] / df['delta.tested'],
                **scatter_style
            )
        )
        fig5.update_layout(
            title="Test Positivity Rate (TPR)",
            yaxis_title="%",
            **figure_params
        )
        fig5.update_yaxes(
            autorange=True,
            fixedrange=False
        )

        fig6 = go.Figure()
        fig6.add_trace(
            go.Scatter(
                x=df['date'],
                y=100 * df['delta.deceased'] / df['delta.confirmed'],
                **scatter_style
            )
        )
        fig6.update_layout(
            title="Case Fatality Rate (CFR)",
            yaxis_title="%",
            **figure_params
        )
        fig6.update_yaxes(
            autorange=True,
            fixedrange=False,
        )

        return fig1, fig2, fig3, fig4, fig5, fig6

@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == 'tab-2':
        return tab2_body
    elif active_tab == 'tab-1':
        return tab1_body

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=5555)