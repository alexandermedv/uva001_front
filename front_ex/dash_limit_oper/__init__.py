# Инициализируем Dashboards
from dash import Dash
# from dash import html
# from dash import dcc
# import dash_html_components as html
from dash import html
# import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output

import os

import dash_bootstrap_components as dbc

from .. import app

# Базовые URL определяет куст все страниц на сайте
dash_app = Dash(__name__, server=app, url_base_pathname='/limit_oper_dash/', 
    suppress_callback_exceptions = True,
    external_stylesheets=[dbc.themes.BOOTSTRAP])
# dash_app.config.suppress_callback_exceptions = True
# dash_app.config.update(app.config)

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id='page-content')]
)

@dash_app.callback(Output("page-content","children"), [Input("url", "pathname")])
def display_page(pathname):
    # print('render')
    if pathname == "/limit_oper/page-2":
        return html.H3('URL Error!')
    else:
        return overview.create_layout(dash_app) 

# Инициализируем после Dash страницы
from . import overview, page_2