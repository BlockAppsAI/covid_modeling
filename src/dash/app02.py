import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


sys.path.append('..')
from consumer.api_consumer import DataLoader
from style import *
from constants import *
pio.renderers.default = "browser"


external_stylesheets = [dbc.themes.SANDSTONE]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dl = DataLoader()
states = dl.get_all_states_with_codes()
codes = {value: key for key, value in states.items()}
states = [{'label': key.title(), 'value': value} for key, value in states.items()]


tab1_body = tab1_body = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='geography',
                options=states,
                value=['KA', 'KL', 'TN', 'MH', 'AP', 'TG'], 
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
                value='delta.confirmed',
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
        ],), # style={'background-color': colors['background']},),
        dbc.CardBody(tab1_body, id="card-content",),
    ],
)

app.layout = dbc.Container([
    html.H1(children="Covid 19 India", 
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
    Output('geography-metric', 'figure'),
    Input('geography', 'value'),
    Input('metric', 'value')
)
def update_plots(geography, metric):
    data = dl.get_data(state_codes=geography)
    fig = go.Figure()
    if geography is None or metric is None:
        raise PreventUpdate
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
                # title=column_dt[metric],
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
                # title=column_dt[metric],
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


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=5555)