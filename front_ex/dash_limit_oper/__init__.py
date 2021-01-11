# Инициализируем Dashboards
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from .. import flask_app

# Базовые URL определяет куст все страниц на сайте
dash_app = Dash(__name__, server = flask_app, url_base_pathname='/limit_oper_dash/', suppress_callback_exceptions = True)
dash_app.config.update(flask_app.config)
# Тест
# dash_app.config..supress_callback_exceptions = True

dash_app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id='page-content')]
)

@dash_app.callback(Output("page-content","children"), [Input("url", "pathname")])
def display_page(pathname):
    print('render')
    if pathname == "/limit_oper/page-2":
        return html.H3('URL Error!')
    else:
        return overview.create_layout(dash_app) 
            # overview.create_layout(dash_app) 
        
        # html.H3('URL Error!')

        # overview.create_layout(dash_app)

# Инициализируем после Dash страницы
from .pages import overview, page_2