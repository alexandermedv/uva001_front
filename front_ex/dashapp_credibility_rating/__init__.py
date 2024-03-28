"""Инициализируем Dashboards"""
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from .. import app

dash_app = Dash(__name__, server=app,
                url_base_pathname='/dashboards/credibility_rating_dash/',
                 suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])#external_scripts=external_scripts
dash_app.layout = html.Div()

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id='page-content')]
)

# Инициализируем после Dash
from .pages import layout


@dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    """Выбор шаблона"""
    print(pathname)
    if pathname == "/dashboards/credibility_rating_dash/":
        layout_dash1 = layout.create_layout()
        return layout_dash1
    else:
        #layout = overview.create_layout(dash_app)
        return 'Не тот путь'
