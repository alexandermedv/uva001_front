""" Шаблоны для отчетов по запчастям."""
from datetime import date
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from . import engine_cons
#from ..utils import get_max_date, get_resellers_count
from sqlalchemy import create_engine
# import front_ex.config as config

#import dash_table
#import pandas as pd

#from flask_app import engine_analysis, engine_cons

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    layout = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            html.Div([
                html.Div(
                    [
                        html.H5("Количество запросов СПАРК"),
                        html.Br([]),
                    ], className="product",
                )
            ], className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(id="content"),
                            html.Br(),
                            html.Button('Обновление отчета', id='button'),
                        ], className="six columns"
                    ),
                    html.Div([dcc.Graph(id="pie")], className="six columns"),
                ], className="row",
            ),
            html.Div([dcc.Graph(id="bar")])
        ], className="sub_page",)
    ], className="page_landscape_a3",)

    return layout
