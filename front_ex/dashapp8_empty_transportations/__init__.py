"""Инициализируем Dashboards"""
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from .. import app
# , db, engine_cons

external_scripts = [
    {'src': 'https://code.jquery.com/jquery-3.5.1.js'},
]

dash_app = Dash(__name__, server=app,
                url_base_pathname='/dashboards/empty_transportations_dash/',
                suppress_callback_exceptions=True, external_scripts=external_scripts)
dash_app.config.update(app.config)
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
    if pathname == "/dashboards/empty_transportations_dash/":
        layout_dash1 = layout.create_layout()
        return layout_dash1
        #page_4.create_layout(dash_app)
    else:
        #layout = overview.create_layout(dash_app)
        return 'Не тот путь'
        #return layout
