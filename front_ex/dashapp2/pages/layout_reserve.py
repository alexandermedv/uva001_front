
import dash_core_components as dcc
import dash_html_components as html

from app.dashes import dashapp2

layout1 = html.Div([
    html.H3('Отчеты по ролям и полномочиям в SAP'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'Отчеты по ролям и полномочиям в SAP - {}'.format(i), 'value': i} for i in [
                'Отчет по S_DEVELOP', 'Отчет по SAP_ALL', 'Конфликтующие полномочия'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    html.A('Перейти к отчетам по запчастям', href='/repair_parts')
])