import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from flask import Flask, send_from_directory

from data import *
from style import *

from raw_data import tab1_body, column_dt
from metrics import tab2_body
from forecasts import tab3_body


pio.renderers.default = "browser"
server = Flask(__name__, static_folder='static')
external_stylesheets = [dbc.themes.SANDSTONE]
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)
app.title = "Covid Modelling | BlockApps AI"


@server.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(server.root_path, 'static'),
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )


card = dbc.Card(
    [
        dbc.CardHeader([
            dbc.Tabs(
                [
                    dbc.Tab(label="Spread Parameters", tab_id="tab-2", tab_style={"marginLeft": "auto"}),
                    dbc.Tab(label='Forecasts', tab_id='tab-3'),
                    dbc.Tab(label="Daily Raw Data", tab_id="tab-1"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            ),
        ],), # style={'background-color': colors['background']},),
        dbc.CardBody(tab1_body, id="card-content",),
    ],
)

app.layout = dbc.Container([
    html.H1(children="Covid 19 in India", 
            style={'text-align': "center",
                    'color': colors['text'],
                  }),
    html.Div([
        "Data is updated every day at 10:00 AM from ",
        dcc.Link(html.A("covid19india.org"), href="https://covid19india.org/")
    ], style={'text-align': 'center',}),
    card,
    html.Footer(dcc.Link(html.H5('© BlockApps AI'), href="https://blockappsai.com/")),
], fluid=True)


@app.callback(
    Output('geography-metric', 'figure'),
    Input('geography', 'value'),
    Input('metric', 'value')
)
def update_plots(geography, metric):
    data = None
    fig = go.Figure()
    try:
        data = dl.get_data(state_codes=geography)
    except ValueError:
        return empty_data_dict

    if data is None or metric is None:
        # raise PreventUpdate
        return empty_data_dict
    else:
        if isinstance(data, dict):
            for key, df in data.items():
                fig.add_trace(
                    go.Scatter(
                        x=df['date'],
                        y=df[metric],
                        **scatter_style,
                        name=codes[key]
                    )
                )
            fig.update_layout(
                title=column_dt[metric],
                **figure_params
            )
            fig.update_yaxes(
                autorange=True,
                fixedrange=False
            )
            fig.update_xaxes(rangeslider_thickness=0.05)
        else:
            fig.add_trace(
                go.Scatter(
                    x=data['date'],
                    y=data[metric],
                    **scatter_style,
                    name=codes[geography]
                )
            )
            fig.update_layout(
                title=column_dt[metric],
                **figure_params
            )
            fig.update_yaxes(
                autorange=True,
                fixedrange=False
            )
            fig.update_xaxes(rangeslider_thickness=0.05)

        return fig


@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == 'tab-2':
        return tab2_body
    elif active_tab == 'tab-1':
        return tab1_body
    elif active_tab == 'tab-3':
        return tab3_body


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=5555)