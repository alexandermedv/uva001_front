# Инициализируем Dashboards
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from .. import flask_app

dash_app = Dash(__name__, server = flask_app, url_base_pathname='/osv_dev/', suppress_callback_exceptions = True)
dash_app.config.update(flask_app.config)
dash_app.layout = html.Div()

# Тест
# dash_app.config..supress_callback_exceptions = True

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id='page-content')]
)

# Инициализируем после Dash
from .pages import overview, page_4

@dash_app.callback(Output("page-content","children"), [Input("url", "pathname")])
def display_page(pathname):
    print(pathname)
    if pathname == "/osv/page-4":
        
        return page_4.create_layout(dash_app)
    else:
        layout = overview.create_layout(dash_app)
        return layout
