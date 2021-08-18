import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

tab2_content = html.P("Research and Development details will be published here.")

tab2_body = tab1_body = dbc.Card(
    dbc.CardBody(
        [
            tab2_content
        ]
    ),
)