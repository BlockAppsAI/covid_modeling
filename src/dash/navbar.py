import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

LOGO = "assets/logo-cropped.png"


navbar = dbc.Navbar(
    [
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row([
            dbc.Col(
                html.A(
                    html.Img(src=LOGO, height="30px"),
                    href="https://blockappsai.com/",
                ), align="center"
            ),
            dbc.Col(
                dbc.NavbarBrand("Covid 19 in India"),
                align="center"
            ),
        ], no_gutters=False, justify="between", align="center"),
        # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        # dbc.Collapse(
        #     id="navbar-collapse", navbar=True, is_open=False
        # ),
    ],
    color="dark",
    dark=True,
    sticky='top',
    expand='True',
)