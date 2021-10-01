import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from matplotlib.container import Container
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State

from flask import Flask, send_from_directory

from data import *
from style import *

from metrics import tab1_body, column_dt
from forecasts import tab3_body
from readme import tab2_body
from navbar import navbar


pio.renderers.default = "browser"
server = Flask(__name__, static_folder='static')
external_stylesheets = [dbc.themes.JOURNAL]
app = dash.Dash(
    server=server,
    external_stylesheets=external_stylesheets,
    # suppress_callback_exceptions=True
)
app.title = "Covid Modelling | BlockApps AI"

# Data
daily_data_t, daily_data_y = dl.get_all_daily()
daily_data_t['vacc_per'] = 100 * daily_data_t['total.vaccinated1']/daily_data_t['population']
daily_data_t['full_vacc_per'] = 100 * daily_data_t['total.vaccinated2']/daily_data_t['population']

daily_data_y['vacc_per'] = 100 * daily_data_y['total.vaccinated1']/daily_data_y['population']
daily_data_y['full_vacc_per'] = 100 * daily_data_y['total.vaccinated2']/daily_data_y['population']


# Aux Data
column_dt = {
    'rt': 'Reproduction Number - R(t)',
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
    'delta.vaccinated1': 'Daily First Vaccination',
    'delta7.vaccinated1': 'Daily First Vaccination (7 Day Average)',
    'total.vaccinated1': 'Total First Vaccination',
    'delta.vaccinated2': 'Daily Fully Vaccinated',
    'delta7.vaccinated2': 'Daily Fully Vaccinated (7 Day Average)',
    'total.vaccinated2': 'Total Fully Vaccinated',
    'vacc_per': 'Vaccinated Population %',
    'full_vacc_per': 'Fully Vaccinated Population %'
}


@server.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(server.root_path, 'assets'),
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )


app.layout = html.Div([
    navbar,
    dbc.Tabs(
        [
            dbc.Tab(label="Day at a Glance", tab_id='tab-4'),
            dbc.Tab(label="Plots", tab_id="tab-1"), # tabClassName="ml-auto"),
            dbc.Tab(label='Forecasts', tab_id='tab-3'),
            dbc.Tab(label='Scenarios', tab_id='tab-5'),
            dbc.Tab(label='Read Me', tab_id='tab-2'),
        ],
        id="tabs",
        active_tab="tab-4",
    ),
    html.Div(
        id="glance-tab",
        children=[
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='geography-glance',
                        options=states,
                        value='TT',
                        multi=False,
                        placeholder="Select Geography",
                        style={
                            'vertical-align': 'middle',
                            'marginLeft': 'auto',
                            'align': 'inline-block'
                        }
                    ),
                    width={'size': 4, 'offset': 4},
                    style={'height': 'inherit', 'align': 'center'},
                ),
            ]),
            dbc.Container([
                dbc.Spinner([
                    dcc.Graph(id='vacc-data', style={'margin-bottom': -50, "padding": 0}),
                    dcc.Graph(id='case-data', style={'margin-top': -60, "padding": 0})
                ])
            ], fluid=True, style={'margin': 0, 'padding': 0}),
            html.Hr(),
            html.Footer(
                dbc.Row([
                    dbc.Col(
                        html.H5("Data Last Updated: Oct 01, 2021 @ 11:20 AM"), 
                        align='start', width={'size': 4}
                    ),
                    dbc.Col(
                        html.H5("green is good, red is bad!"), 
                        align='end', width={'size': 4, 'offset': 4}
                    )
                ])
            )
        ]
    ),
    html.Div(
        id="metrics-tab",
        children=[
            tab1_body
        ],
        style={
            'display': 'none',
        }
    ),
    html.Div(
        id="ka-forecasts-tab",
        children=[
            tab2_body
        ],
        style={
            'display': 'none',
        }
    ),
    html.Div(
        id="scenario-analysis",
        children=[
            html.P("Coming Up!")
        ],
        style={
            'display': 'none',
        }
    ),
    html.Div(
        id="readme-tab",
        children=[
            tab3_body
        ],
        style={
            'display': 'none',
        }
    ),
])


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


@app.callback(
    Output("vacc-data", "figure"),
    Output("case-data", "figure"),
    [Input("geography-glance", "value")]
)
def get_data_cards(geo):
    if geo is None:
        return empty_data_dict

    vacc = [
        'vacc_per', 'full_vacc_per', 'total.vaccinated1', 'total.vaccinated2', 
    ]

    case = [
        'delta.confirmed', 'delta.deceased', 
        'delta.tested', 'delta.vaccinated1', 
        'delta.vaccinated2', 'tpr', 'cfr'
    ]

    fig1 = go.Figure()
    fig2 = go.Figure()

    for i, metric in enumerate(vacc):
        confirmed_t = daily_data_t.loc[geo][metric]
        confirmed_y = daily_data_y.loc[geo][metric]
        
        fig1.add_trace(
            go.Indicator(
                mode="number+delta",
                value=confirmed_t,
                delta={
                    'reference': confirmed_y,
                    'relative': False,
                },
                domain={
                    'row': i//2,
                    'column': i%2
                },
                title={
                    'text': f"{column_dt[metric]}",
                    'align': 'center'
                },
                number={
                    'suffix': '%' if metric in ['vacc_per', 'full_vacc_per'] else None
                }
            )
        )
    
    fig1.update_layout(
        grid={'rows': 2, 'columns': 2, 'pattern': 'independent'}
    )

    for i, metric in enumerate(case):
        confirmed_t = daily_data_t.loc[geo][metric]
        confirmed_y = daily_data_y.loc[geo][metric]

        delta = {
            'reference': confirmed_y,
            'relative': False,
        }

        if metric in ['delta.confirmed', 'delta.deceased', 'tpr', 'cfr']:
            delta['decreasing'] = {
                'color': 'green'
            }
            delta['increasing'] = {
                'color': 'red'
            }
        
        fig2.add_trace(
            go.Indicator(
                mode="number+delta",
                value=confirmed_t,
                delta=delta,
                domain={
                    'row': i//4,
                    'column': i%4
                },
                title={
                    'text': f"{column_dt[metric]}",
                    'align': 'center'
                },
                number={
                    'suffix': '%' if metric in ['tpr', 'cfr'] else None
                }
            )
        )

    fig2.update_layout(
        grid={'rows': 2, 'columns': 4, 'pattern': 'independent'}
    )

    return fig1, fig2


@app.callback(
    [
        Output("metrics-tab", "style"),
        Output("ka-forecasts-tab", "style"),
        Output("readme-tab", "style"),
        Output("glance-tab", "style"),
        Output("scenario-analysis", "style")
    ], 
    [
        Input("tabs", "active_tab")
    ]
)
def tab_content(active_tab):
    on = {'display': 'block'}
    off = {'display': 'none'}
    if active_tab is not None:
        if active_tab == "tab-1":
            return on, off, off, off, off
        elif active_tab == "tab-2":
            return off, on, off, off, off
        elif active_tab == "tab-3":
            return off, off, on, off, off
        elif active_tab == "tab-4":
            return off, off, off, on, off
        elif active_tab == "tab-5":
            return off, off, off, off, on
    return "No tab selected"


if __name__ == "__main__":
    app.run_server(debug=True, host='localhost', port=5555)
