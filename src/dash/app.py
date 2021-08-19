import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from matplotlib.pyplot import get
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from flask import Flask, send_from_directory

from data import *
from style import *

from metrics import tab1_body, column_dt
from forecasts import tab3_body
from readme import tab2_body


pio.renderers.default = "browser"
server = Flask(__name__, static_folder='static')
external_stylesheets = [dbc.themes.UNITED]
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)
app.title = "Covid Modelling | BlockApps AI"


@server.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(server.root_path, 'assets'),
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )

tabs = html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="Metrics", tab_id="tab-1", tab_style={"marginLeft": "auto"}),
                dbc.Tab(label='KA Forecasts', tab_id='tab-3'),
                dbc.Tab(label='Read Me', tab_id='tab-2'),
            ],
            id="tabs",
            card=True,
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

app.layout = dbc.Container([
    html.H1(children="Covid 19 in India", 
            style={'text-align': "center",
                    'color': colors['text'],
                  }),
    html.Div([
        "Raw Data is updated every day at 12:00 noon from ",
        dcc.Link(html.A("covid19india.org"), href="https://covid19india.org/")
    ], style={'text-align': 'center',}),
    tabs,
    html.Footer(dcc.Link(html.H5('© BlockApps AI'), href="https://blockappsai.com/")),
], fluid=True)


def get_rt(geography, metric):
    fig = go.Figure()
    try:
        data = rtdl.load_rt(state_codes=geography)
    except ValueError:
        return empty_data_dict
    
    if isinstance(data, dict):
        for key, df in data.items():
            fig.add_traces([
                go.Scatter(
                    x=df['date'],
                    y=df['Q0.5'],
                    **rt_scatter_style,
                    name=codes[key]
                ),
                go.Scatter(
                    name="R(t) 95% upper" + codes[key],
                    x=df['date'],
                    y=df['Q0.975'],
                    mode='lines',
                    showlegend=False,
                    line=dict(width=0),
                ),
                go.Scatter(
                    name="R(t) 95% lower" + codes[key],
                    x=df['date'],
                    y=df['Q0.025'],
                    mode='lines',
                    showlegend=False,
                    fill='tonexty',
                    line=dict(width=0),
                ),
                go.Scatter(
                    name="R(t) 50% upper" + codes[key],
                    x=df['date'],
                    y=df['Q0.75'],
                    mode='lines',
                    showlegend=False,
                    line=dict(width=0),
                ),
                go.Scatter(
                    name="R(t) 50% lower" + codes[key],
                    x=df['date'],
                    y=df['Q0.25'],
                    mode='lines',
                    showlegend=False,
                    fill='tonexty',
                    line=dict(width=0),
                ),
            ])
    else:
        fig.add_traces([
            go.Scatter(
                x=data['date'],
                y=data['Q0.5'],
                **rt_scatter_style,
                name=codes[geography]
            ),
            go.Scatter(
                name="R(t) 95% upper" + codes[key],
                x=data['date'],
                y=data['Q0.975'],
                mode='lines',
                showlegend=False,
                line=dict(width=0),
            ),
            go.Scatter(
                name="R(t) 95% lower" + codes[key],
                x=data['date'],
                y=data['Q0.025'],
                mode='lines',
                showlegend=False,
                fill='tonexty',
                line=dict(width=0),
            ),
            go.Scatter(
                name="R(t) 50% upper" + codes[key],
                x=data['date'],
                y=data['Q0.75'],
                mode='lines',
                showlegend=False,
                line=dict(width=0),
            ),
            go.Scatter(
                name="R(t) 50% lower" + codes[key],
                x=data['date'],
                y=data['Q0.25'],
                mode='lines',
                showlegend=False,
                fill='tonexty',
                line=dict(width=0),
            ),
        ])
    
    fig.update_layout(
        title=column_dt[metric],
        **figure_params,
        yaxis_title='R(t) with 95%-CI and 50%-CI',
    )
    fig.update_yaxes(
        autorange=True,
        fixedrange=False,
    )
    fig.update_xaxes(rangeslider_thickness=0.05)
    fig.add_hline(y=1.0, line_dash='dash', line_width=3.0)

    return fig


@app.callback(
    Output('geography-metric', 'figure'),
    Input('geography', 'value'),
    Input('metric', 'value')
)
def update_plots(geography, metric):
    if metric == 'rt':
        return get_rt(geography, metric)

    fig = go.Figure()
    data = None
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


# @app.callback(
#     Output('daily-confirmed', 'figure'),
#     Output('daily-deceased', 'figure'),
#     Input("active_tab", "content"),
# )
# def update_forecast_plots():
#     df_forecasts = fl.get_forecasts()
#     df_daily = dl.get_data('KA')

#     fig1 = go.Figure()
#     fig2 = go.Figure()
#     fig1.add_traces([
#         go.Scatter(
#             x=df_forecasts['date'],
#             y=df_forecasts['daily confirmed'],
#             name='Confirmed Cases Forecast'
#             **scatter_style
#         ),
#         go.Scatter(
#             x=df_daily['date'],
#             y=df_daily['delta.confirmed'],
#             name='Confirmed Cases Actual'
#             **scatter_style
#         )
#     ])

#     return fig1, None


@app.callback(
    Output("content", "children"), [Input("tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == 'tab-1':
        return tab1_body
    elif active_tab == 'tab-3':
        return tab3_body
    elif active_tab == 'tab-2':
        return tab2_body


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=5555)