import dash_html_components as html
import dash_core_components as dcc
import datetime as dt

import pandas as pd

from sqlalchemy import create_engine

def get_osv_detail_by_dates(datefrom, dateto, debug = False):

    sql = '''   
          select "Дата ввода", sum("Сумма во внутренней валюте по дебе") as "Обороты по дебету", 
                sum("Сумма во внутренней валюте по кред") as "Обороты по кредиту", 
                    material."Группа материалов",
                    "Название бизнес-сферы" as "Филиал", "Наименование склада" as "Склад",  
                    sum(sign("Сумма во внутренней валюте по дебе")) as "Обороты по дебету, шт",
                    sum(sign("Сумма во внутренней валюте по кред")) as "Обороты по кредиту, шт"
                    
                    from sap_s4.osv_94 
                    	left join sap_s4.material on material."Код материала" = osv_94."Материал"::int::varchar
                           where "Дата ввода" between '{}' and '{}'
                                --and "Дата ввода" > '20180101'
                                    group by "Дата ввода", "Название бизнес-сферы", "Наименование склада"
                                        , material."Группа материалов"
    '''.format(dt.datetime.strftime(datefrom, '%Y%m%d'), dt.datetime.strftime(dateto, '%Y%m%d'))
    
    if debug: print(sql)
    
    return pd.read_sql(sql, create_engine("postgresql://locadm:Temp001@msc199-sdb04.domain.local:8031/uva_cons", max_identifier_length=128, encoding='utf-8'))


def get_osv_detail():
    sql = '''   
          select "Дата ввода", sum("Сумма во внутренней валюте по дебе") as "Обороты по дебету", 
                sum("Сумма во внутренней валюте по кред") as "Обороты по кредиту", 
                    material."Группа материалов",
                    "Название бизнес-сферы" as "Филиал", "Наименование склада" as "Склад",  
                    sum(sign("Сумма во внутренней валюте по дебе")) as "Обороты по дебету, шт",
                    sum(sign("Сумма во внутренней валюте по кред")) as "Обороты по кредиту, шт"
                    
                    from sap_s4.osv_94 
                    	left join sap_s4.material on material."Код материала" = osv_94."Материал"::int::varchar
                                    group by "Дата ввода", "Название бизнес-сферы", "Наименование склада"
                                        , material."Группа материалов"
    '''
    return pd.read_sql(sql, create_engine("postgresql://locadm:Temp001@msc199-sdb04.domain.local:8031/uva_cons", max_identifier_length=128, encoding='utf-8'))

def get_osv_department(df):

    return None

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        html.Img(
                            src=app.get_asset_url("logo_stayhome.jpg"),
                            className="logo",
                        ),
                        className = "seven columns"
                    ),
                    html.Div(
                        dcc.Link(
                                    "Все страницы",
                                    href="/dash-financial-report/full-view",
                                    className="full-view-link",
                        ),
                        className = 'five columns'
                    ),
                ],
                className="twelve columns",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Мониторинг недостач")],
                        # className="seven columns main-title",
                        className="twelwe columns main-title",
                    ),
                ],
                
                # className="thirteen columns",
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header

def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Обзор",
                href="/dash-financial-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "Детальная информация",
                href="/dash-financial-report/price-performance",
                className="tab",
            ),
            dcc.Link(
                "Поиск аномалий",
                href="/dash-financial-report/portfolio-management",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu