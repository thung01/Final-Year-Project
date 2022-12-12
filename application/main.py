import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

#STYLE
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

#Read Data
df = pd.read_csv(r'C:\Users\User\Desktop\Grocery Track\trainer.csv')
df2 = pd.read_csv(r'C:\Users\User\Desktop\Grocery Track\tester.csv')

sidebar = html.Div(
    [
        html.Img(src='assets/logo.png', style={"left-padding":"50px"}),
        # html.H2("Sidebar", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Grocery Track Dashboard",
                         style={'fontSize':45, 'textAlign':'center', 'background-color': '#bae8e8'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)

if __name__ == "__main__":
    app.run(debug=False)