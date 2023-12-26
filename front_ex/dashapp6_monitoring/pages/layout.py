""" Шаблоны для отчета по мониторингу."""
from datetime import date
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine

from ..utils import get_max_date
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

            # Row 2 - 1-й ряд фильтров
            html.Div([
                dbc.Navbar([
                    html.Div(
                        html.Output('Дата:'),
                        className='one column',
                        style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }
                            ),
                    dcc.DatePickerRange(
                        id='dashboard2-date-picker-range',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2050, 1, 1),
                        initial_visible_month=date(2020, 1, 1),
                        start_date=date(2020, 1, 1),
                        end_date=get_max_date().strftime("%m.%d.%Y"),
                        number_of_months_shown = 3,
                        updatemode = 'singledate',
                        display_format='DD.MM.YYYY',
                        start_date_placeholder_text='Начало периода',
                        end_date_placeholder_text='Конец периода',
                    className='four columns'),

                ],)
            ], className="row",
            ),

            html.Div(render_content(), id='tab-content'),
        ], className="sub_page",
        ),
    ], className="page_landscape_a3",
    )

    return layout
