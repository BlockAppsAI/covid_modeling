import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from torch import special

researchers = [
    "Dr. Vishal Rao: Dean Academic @ HCG, Bangalore",
    "Ashish Kumar Anshu: Research Engineer @ BlockApps AI, Bangalore",
    "Bhupendra Gupta: Asst. Professor @ IIITDM Jabalpur",
    "Ritesh Kumar Dubey: Assoc. Professor @ SRM-IST Research Institute, Chennai",
    "Subhabrata Pal: Head of Medtech @ BlockApps AI, Bangalore",
    "Anupam Gupta: Research Scientist and CTO @ BlockApps AI, Bangalore"
]

special = [
    "Dr. Ambujam Nair Kapoor: Advisor @ BlockApps AI and Ex-Senior DDG, ICMR Delhi",
    "Srikar Y.: Advisor @ BlockApps AI",
    "Sridhar Y.: Head of Operations and CEO @ BlockApps AI"
]

todo = [
    "- Scenario Analysis based on our modified SEIRDV model",
    "- Multiple horizon forecasts (7/14/21 days)",
    "- All Indian states forecasts",
    "- District-wise metric for Karnataka",
    "- Adjusting forecasts using mobility data",
    "- Peak Prediction"
]

formatted1 = list(map(dbc.ListGroupItemText, researchers))
formatted2 = list(map(dbc.ListGroupItemText, special))
formatted_todo = list(map(dbc.ListGroupItemText, todo))

tab2_content = dbc.Container(children=[
    dbc.ListGroup([
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading("Versions"),
                dbc.ListGroupItemText("Dashboard: 0.2"),
                dbc.ListGroupItemText("Modeling: 0.9")
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading("Comping Up"),
                html.Hr(),
                *formatted_todo
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading("Bibliography"),
                dbc.ListGroupItemText("To be published"),

                dbc.ListGroupItemHeading("Code"),
                dbc.ListGroupItemText("To be published under GNU GPLv3 License"),
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading("Our Manuscripts and Publications"),
                dbc.ListGroupItemText("To be published"),
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading("Research Team"),
                html.Hr(),
                *formatted1
            ]
        ),
        dbc.ListGroupItem(
            [
                dbc.ListGroupItemHeading("Special Mention"),
                html.Hr(),
                *formatted2
            ]
        ),
    ])
])

tab2_body = tab1_body = dbc.Card(
    dbc.CardBody(
        [
            tab2_content
        ]
    ),
)