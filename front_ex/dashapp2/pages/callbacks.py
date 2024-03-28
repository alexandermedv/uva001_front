""" Интерактивные элементы для отчетов по запчастям."""
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Group
#from app.dashes import dashapp1
#from app.raw_sql import dashapp1_non_used_details_udv_filial
import plotly.graph_objects as go
import pandas as pd
#from .layout import layout1
import string
import datetime as dt
from sqlalchemy import create_engine
from ..pages import dash_app
#from ..utils import get_osv_detail_by_dates, get_osv_detail_by_dates2, get_branch_names, get_detail_type_names, get_warehouse_names

#from app import engine_analysis, engine_cons

engine_cons = create_engine("postgresql://locadm:Temp001@msc199-sdb04.domain.local:8031/uva_cons", max_identifier_length=128)


# # Выбор отчета на главной странице
# @dash_app.callback(Output('page-content', 'children'),
#                     [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/repair_parts/dashboard1':
#         return layout1
#     elif pathname == '/repair_parts/dashboard2':
#         return layout2
#     else:
#         return index_page
#     # You could also return a 404 "URL not found" page here



# Гистограмма по филиалам для отчета по неликвидным запчастям
@dash_app.callback(
    Output('graph1', 'figure'),
    [Input(component_id='dropdown_system', component_property='value')]
)

def content(system):

    if system == 'УДВ':
        sql = """
        SELECT filial_short_name,
            count(*) AS quantity
        FROM (
            SELECT udw.details_extended.detail_id,
                udw.details_extended.detail_name,
                udw.details_extended.det_num,
                udw.details_extended.det_god,
                udw.details_extended.det_zavod,
                udw.details_extended.source_name,
                udw.details_extended.source_date,
                udw.details_extended.filial_short_name,
                udw.details_extended.details_store_name,
                max(udw.details_operation.oper_date) AS last_oper_date,
                EXTRACT (DAY FROM (now() - max(udw.details_operation.oper_date))) AS time_delta
            FROM udw.details_extended
                LEFT JOIN udw.details_operation
                    ON udw.details_extended.detail_id = udw.details_operation.detail_id
            WHERE udw.details_extended.is_expensed = 'false'
            AND udw.details_extended.is_accepted = 'true'
            AND udw.details_extended.is_scrap = 'false'
            GROUP BY udw.details_extended.detail_id,
                    udw.details_extended.detail_name,
                    udw.details_extended.det_num,
                    udw.details_extended.det_god,
                    udw.details_extended.det_zavod,
                    udw.details_extended.source_name,
                    udw.details_extended.source_date,
                    udw.details_extended.filial_short_name,
                    udw.details_extended.details_store_name
            HAVING EXTRACT (DAY FROM (now() - max(udw.details_operation.oper_date))) > 180
            ) a
        GROUP BY 
                filial_short_name
        ORDER BY quantity DESC
        """
        df = pd.read_sql(sql, con=engine_analysis)
        x = df['filial_short_name'].tolist()
        y = df['quantity'].astype(str).tolist()
    elif system == 'SAP':
        sql = """
        SELECT name1,
            count(*) AS quantity
        FROM (
        SELECT sap_s4.am_equi_extended.*,
            sap_s4.am_t001w.name1,
            sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)" AS last_oper_date,
            EXTRACT (DAY FROM (now() - TO_DATE(sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)", 'YYYYMMDD'))) AS time_delta
        FROM sap_s4.am_equi_extended
            LEFT JOIN sap_s4.am_mseg_last_oper_date
                ON sap_s4.am_equi_extended.equnr = '00000000'||sap_s4.am_mseg_last_oper_date.charg
            LEFT JOIN sap_s4.am_t001w
                ON sap_s4.am_equi_extended.b_werk = sap_s4.am_t001w.werks
        WHERE detail_deleted = '0'
            AND EXTRACT (DAY FROM (now() - TO_DATE(sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)", 'YYYYMMDD'))) > 180
            AND detail_status LIKE '%%НАСК_На складе%%'
        ) a
        GROUP BY name1
        ORDER BY quantity DESC
        """
        df = pd.read_sql(sql, con=engine_analysis)
        x = df['name1'].tolist()
        y = df['quantity'].astype(str).tolist()


    fig = go.Figure(data=[go.Bar(
            x=x, y=y,
        #  text=df['quantity'].astype(str).tolist(),
            text=y,
            textposition='auto',
        )]
    )
        #,layout=go.Layout(title='Распределение неликвидных запчастей по филиалам'))

    return fig

# Таблица со списком неликвидных деталей (обновление данных)
@dash_app.callback(
    Output(component_id='table1', component_property='data'),
    [
    Input(component_id='dropdown_system', component_property='value')
    ]
)

def overstocked_parts(system):

    if system == 'УДВ':
        sql = """
            SELECT  udw.details_extended.detail_id,
                    udw.details_extended.detail_name,
                    udw.details_extended.det_num,
                    udw.details_extended.det_god,
                    udw.details_extended.det_zavod,
                    udw.details_extended.source_name,
                    udw.details_extended.source_date,
                    udw.details_extended.filial_short_name,
                    udw.details_extended.details_store_name,
                    max(udw.details_operation.oper_date) AS last_oper_date,
                    EXTRACT (DAY FROM (now() - max(udw.details_operation.oper_date))) AS time_delta
            FROM udw.details_extended
                LEFT JOIN udw.details_operation
                    ON udw.details_extended.detail_id = udw.details_operation.detail_id
            WHERE udw.details_extended.is_expensed = 'false'
                AND udw.details_extended.is_accepted = 'true'
                AND udw.details_extended.is_scrap = 'false'
            GROUP BY udw.details_extended.detail_id,
                    udw.details_extended.detail_name,
                    udw.details_extended.det_num,
                    udw.details_extended.det_god,
                    udw.details_extended.det_zavod,
                    udw.details_extended.source_name,
                    udw.details_extended.source_date,
                    udw.details_extended.filial_short_name,
                    udw.details_extended.details_store_name
            HAVING EXTRACT (DAY FROM (now() - max(udw.details_operation.oper_date))) > 180
        """
        df = pd.read_sql(sql, con=engine_analysis)
    elif system == 'SAP':
        sql = """
            SELECT sap_s4.am_equi_extended.*,
                sap_s4.am_t001w.name1,
                sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)" AS last_oper_date,
                EXTRACT (DAY FROM (now() - TO_DATE(sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)", 'YYYYMMDD'))) AS time_delta
            FROM sap_s4.am_equi_extended
                LEFT JOIN sap_s4.am_mseg_last_oper_date
                    ON sap_s4.am_equi_extended.equnr = '00000000'||sap_s4.am_mseg_last_oper_date.charg
                LEFT JOIN sap_s4.am_t001w
                    ON sap_s4.am_equi_extended.b_werk = sap_s4.am_t001w.werks
            WHERE detail_deleted = '0'
            AND EXTRACT (DAY FROM (now() - TO_DATE(sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)", 'YYYYMMDD'))) > 180
            AND detail_status LIKE '%%НАСК_На складе%%'
        """
        df = pd.read_sql(sql, con=engine_analysis)

    return df.to_dict(orient='records')



# Таблица со списком неликвидных деталей (обновление заголовков)
@dash_app.callback(
    Output(component_id='table1', component_property='columns'),
    [
    Input(component_id='dropdown_system', component_property='value')
    ]
)

def overstoked_parts_headers(system):

    if system == 'УДВ':
        sql = """
            SELECT  udw.details_extended.detail_id,
                    udw.details_extended.detail_name,
                    udw.details_extended.det_num,
                    udw.details_extended.det_god,
                    udw.details_extended.det_zavod,
                    udw.details_extended.source_name,
                    udw.details_extended.source_date,
                    udw.details_extended.filial_short_name,
                    udw.details_extended.details_store_name,
                    max(udw.details_operation.oper_date) AS last_oper_date,
                    EXTRACT (DAY FROM (now() - max(udw.details_operation.oper_date))) AS time_delta
            FROM udw.details_extended
                LEFT JOIN udw.details_operation
                    ON udw.details_extended.detail_id = udw.details_operation.detail_id
            WHERE udw.details_extended.is_expensed = 'false'
                AND udw.details_extended.is_accepted = 'true'
                AND udw.details_extended.is_scrap = 'false'
            GROUP BY udw.details_extended.detail_id,
                    udw.details_extended.detail_name,
                    udw.details_extended.det_num,
                    udw.details_extended.det_god,
                    udw.details_extended.det_zavod,
                    udw.details_extended.source_name,
                    udw.details_extended.source_date,
                    udw.details_extended.filial_short_name,
                    udw.details_extended.details_store_name
            HAVING EXTRACT (DAY FROM (now() - max(udw.details_operation.oper_date))) > 180
        """
        df = pd.read_sql(sql, con=engine_analysis)
    elif system == 'SAP':
        sql = """
            SELECT sap_s4.am_equi_extended.*,
                sap_s4.am_t001w.name1,
                sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)" AS last_oper_date,
                EXTRACT (DAY FROM (now() - TO_DATE(sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)", 'YYYYMMDD'))) AS time_delta
            FROM sap_s4.am_equi_extended
                LEFT JOIN sap_s4.am_mseg_last_oper_date
                    ON sap_s4.am_equi_extended.equnr = '00000000'||sap_s4.am_mseg_last_oper_date.charg
                LEFT JOIN sap_s4.am_t001w
                    ON sap_s4.am_equi_extended.b_werk = sap_s4.am_t001w.werks
            WHERE detail_deleted = '0'
            AND EXTRACT (DAY FROM (now() - TO_DATE(sap_s4.am_mseg_last_oper_date."MAX(BUDAT_MKPF)", 'YYYYMMDD'))) > 180
            AND detail_status LIKE '%%НАСК_На складе%%'
        """
        df = pd.read_sql(sql, con=engine_analysis)

    return [{"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns]