import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from matplotlib.pyplot import get
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from flask import Flask, send_from_directory

from data import *
from style import *

from metrics import tab1_body, column_dt
from forecasts import tab3_body
from readme import tab2_body
from data_cards import card_content, cards
from navbar import navbar


pio.renderers.default = "browser"
server = Flask(__name__, static_folder='static')
external_stylesheets = [dbc.themes.FLATLY]
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)
app.title = "Covid Modelling | BlockApps AI"


@server.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(server.root_path, 'assets'),
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )


tabs = dbc.Tabs([
    dbc.Tab(label="Metrics", tab_id="tab-1", tabClassName="ml-auto"),
    dbc.Tab(label='KA Forecasts', tab_id='tab-3'),
    dbc.Tab(label='Read Me', tab_id='tab-2'),
    dbc.Tab(label="Vaccination", tab_id='tab-4')
    ],
    id="tabs",
    # card=True,
    active_tab="tab-4",
)


tabs_card = dbc.Card([
    dbc.CardHeader(tabs),
    dbc.CardBody(html.Div(id='content'))
])


app.layout = html.Div(
    [navbar, tabs_card]
)


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
    elif active_tab == 'tab-4':
        return cards


@app.callback(
    Output("card-content", "")
)
def update_cards():
    pass


if __name__ == "__main__":
    app.run_server(debug=True, host='localhost', port=5555)