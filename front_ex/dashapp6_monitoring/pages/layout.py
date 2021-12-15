""" Шаблоны для отчета по мониторингу."""
from datetime import date
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
import front_ex.config as config
from .callbacks import render_content


def create_layout():
    """Создание шаблона"""
    layout = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            html.Div([
                html.Div(
                    [
                        html.H5("Отчет по мониторингу устранения недостатков", id='title'),
                        html.Br([]),
                        html.P("\
                            Данный отчет содержит информацию о статусе выполнения корректирующих мероприятий для устранения недостатков, выявленных в результате внутренних аудитов.\
                            Отчет построен на основе данных из системы автоматизации внутреннего аудита Autoaudit.",
                            style={"color": "#ffffff"},
                            className="row",
                        ),
                    ], className="product",
                )
            ], className="row",
            ),

            html.Div(render_content(), id='tab-content'),
        ], className="sub_page",
        ),
    ], className="page_landscape_a3",
    )

    return layout
