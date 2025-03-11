"""Инициализируем Dashboards"""
from dash import Dash
from dash.dependencies import Input, Output
# import dash_html_components as html
from dash import html
# import dash_core_components as dcc
from dash import dcc

from .. import app
# , db, engine_cons

dash_app = Dash(__name__, server=app,
                url_base_pathname='/dashboards/repairs_dash/',
                suppress_callback_exceptions=True)
# dash_app.config.update(app.config)
dash_app.layout = html.Div()

# Тест
# dash_app.config..supress_callback_exceptions = True

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id='page-content')]
)

# Инициализируем после Dash
# from .pages import callbacks
from .pages import layout


@dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    """Выбор шаблона"""
    print(pathname)
    if pathname == "/dashboards/repairs_dash/":
        layout_dash1 = layout.create_layout()
        return layout_dash1
        #page_4.create_layout(dash_app)
    else:
        #layout = overview.create_layout(dash_app)
        return 'Не тот путь'
        #return layout
