import dash_bootstrap_components as dbc
import dash_html_components as html


card_content = [
    # dbc.CardHeader(id="data-card-header"),
    dbc.CardBody(
        [
            html.H5(id="data-card-title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
                id="data-card-body"
            ),
        ]
    ),
]


cards = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content, id='vaccine-1')),
        dbc.Col(dbc.Card(card_content, id='vaccine-2')),
        dbc.Col(dbc.Card(card_content, id='vaccine-3')),
        dbc.Col(dbc.Card(card_content, id='vaccine-4')),
    ]
)
