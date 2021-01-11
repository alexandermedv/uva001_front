import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State

import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import os

import pyhdb
import datetime as dt
from datetime import datetime
import numpy as np

from ..pages import dash_app as app
from ..utils import get_connection

def create_layout(app, start_date = None, end_date=None, debug=False):  
    connection_hana = pyhdb.connect(
        host = "sap-db-s4q.sap.tc",
        port = 30115,
        user = "PGKAUDIT",
        password = "Rfh,jyfhf20"
        )
    print(connection_hana)

    cursor_hana = connection_hana.cursor()
    query="""
        SELECT DISTINCT(SAPABAP1.BSEG.KUNNR)as KUNNR, SAPABAP1.KNA1.NAME1 FROM SAPABAP1.BSEG
            LEFT JOIN SAPABAP1.KNA1
                ON SAPABAP1.BSEG.KUNNR=SAPABAP1.KNA1.KUNNR
                where HKONT in ('6201010100', '6202010100')
        """
    df1=pd.read_sql(query, connection_hana)
    print(df1.head(3)) 

    print(os.getcwd())
    file = '/home/locadm/git/uva001_front/Limit1.xlsx'
    xl = pd.ExcelFile(file)
    dflim = xl.parse('BSEG')

    query11="""
        DROP VIEW PGKAUDIT.TEST2;
    """
    cursor_hana.execute(query11)

    df1=pd.read_sql(query, connection_hana)

    query12="""
        CREATE VIEW PGKAUDIT.TEST2 AS
            SELECT 
                CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, 
                ZUONR,
                SHKZG,
                HKONT,
                KUNNR,
                H_BLART,
                DMBTR,
                SAPABAP1.BKPF.CPUDT,
                SAPABAP1.BKPF.CPUTM,
                TO_TIMESTAMP(SAPABAP1.BKPF.BUDAT, 'YYYYMMDD') as BUDAT,
                SAPABAP1.BSEG.BELNR,
                SAPABAP1.BKPF.STBLG,
                CASE
                    WHEN SHKZG = 'S' THEN DMBTR
                    ELSE DMBTR*(-1)
                END as DMBTR_sign
            FROM SAPABAP1.BSEG 
                LEFT JOIN SAPABAP1.BKPF
                ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR) 
            WHERE  
                STBLG<'1' 
                and H_BLART not in ('DC', 'DN') 
                and HKONT in ('6201010100', '6202010100')
            ORDER BY BUDAT;
    """
    cursor_hana.execute(query12)

    query13="""
    DROP TABLE "PGKAUDIT"."RESULT1";
    """
    cursor_hana.execute(query13)

    query14="""
    CREATE TABLE "PGKAUDIT"."RESULT1" AS(
        SELECT ZUONR,
            KUNNR,
            BUDAT,
            max(total) as max_dz,
            min(total) as min_dz,
            avg(total) as avg_dz
        FROM (
            SELECT *,
                (SELECT SUM(DMBTR_sign) 
                FROM PGKAUDIT.TEST2
                WHERE BUDAT <= a.BUDAT
                AND ZUONR = a.ZUONR) as total
            FROM PGKAUDIT.TEST2 a
            ORDER BY BUDAT
            )
        GROUP BY BUDAT,
            KUNNR,
            ZUONR
        ORDER BY BUDAT)
    """
    cursor_hana.execute(query14)

    query15="""
        SELECT * from "PGKAUDIT"."RESULT1"
        """
    dfreit=pd.read_sql(query15, connection_hana)

    dfreit1=dfreit

    dflim1=dflim[['ZUONR', 'LIMIT', 'SAP']]

    dfreit2=dfreit1.merge(dflim1, on='ZUONR', how='left')
    print(dfreit2.head(3))

    dfreit2.insert(8, 'PREV', '')
    print(dfreit2.head(3))

    dfreit_test = dfreit2[['MAX_DZ','LIMIT']][0:10].copy()

    def set_prev(x):
        prev = 0 
        # print(x[0],x[1],prev)
        try:
            if x[0] < 0:
                prev = 0
            elif x[1] < x[0]:
                prev=1
            elif x[1] >= x[0]:
                prev = 0
        except:
            prev = 'E'

        return prev
    dfreit2['PREV'] = dfreit2[['MAX_DZ','LIMIT']].apply(lambda x: set_prev(x), axis=1)

    dfreit2.insert(9, 'DELTA', '')

    def set_delta (x):
        try:
            delta = x[0] - x[1]
        except:
            delta = 'E'
        
    dfreit2['DELTA'] = dfreit2[['MAX_DZ','LIMIT']].apply(lambda x: set_prev(x), axis=1)
    dfreit3=dfreit2[(dfreit2['DELTA']>0)&(dfreit2['LIMIT']>0)]
    dfreit4=dfreit3.pivot_table(['PREV', 'DELTA'], ['ZUONR', 'KUNNR', 'LIMIT', 'SAP'], aggfunc={'PREV': 'sum', 'DELTA': [max, min]}).reset_index()
    dfreit4.columns = dfreit4.columns.map(''.join)
    dfreit5=dfreit4.merge(df1, on='KUNNR', how='left')
    dfreit6=dfreit5.sort_values(['PREVsum'], ascending=False)

    dflim2=dflim[['ZUONR', 'GSBER']]

    dfreit7=dfreit6.merge(dflim2, on='ZUONR', how='left')
    print(dfreit7.head(3))

    dfreit6.columns=['Договор', 'Клиент', 'Лимит', 'Лимит в SAP (1-да, 0-нет)', 'Макс_превышение', 'Мин_превышение', 'Кол-во превышений', 'Имя клиента']
    dfreit8=dfreit7.pivot_table(['KUNNR','DELTAmax', 'DELTAmin', 'PREVsum'], ['GSBER', 'SAP'], aggfunc={'KUNNR': 'count', 'DELTAmax': 'sum', 'DELTAmin': 'sum', 'PREVsum': 'sum'}).reset_index()

    dfreit8.columns=['Филиал', 'Лимит в SAP (1-да, 0-нет)', 'Сумма Макс_превышение', 'Сумма Мин_превышение', 'Кол-во договоров', 'Сумма превышений']
    cursor_hana.close()

    layout = html.Div([
        dbc.Navbar(
                dbc.NavbarBrand(html.Div("УВА. Отчет по превышению лимита. Оперирование.", style={'fontSize': 25})), 
            color='#97151c', dark=True),
        dbc.Navbar([
            html.Div('Выберите клиента:', style={'width': '15%', 'display': 'inline-block', 'color': 'white'}),
            html.Div(dcc.Dropdown(id='klient', 
                                        options=[{'label':df1['NAME1'][df1['KUNNR']==klient], 'value': klient} for klient in df1['KUNNR']], 
                                        value='0001000134'), style={'width': '25%', 'display': 'inline-block'}),
            html.Div('Выберите договор:', style={'width': '15%', 'display': 'inline-block', 'color': 'white'}),
            html.Div(dcc.Dropdown(id='dogovor'), style={'width': '25%', 'display': 'inline-block'})
        ], dark=True, sticky="top", color='rgb(71, 71, 71)'),
        html.Div([
            html.H6('Рейтинг клиентов:'),
            dbc.Col(dash_table.DataTable(
                id='datatable',
                columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in dfreit6.columns],
                data=dfreit6.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10
            ), width=12)
        ], className='eleven columns'),
        html.Div([
            html.H6('Рейтинг филиалов:'),
            dbc.Col(dash_table.DataTable(
                id='datatable2',
                columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in dfreit8.columns],
                data=dfreit8.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10
            ), width=12)
        ], className='eleven columns'),
        dbc.Row(
            html.H4('    По дате ввода')
        ),
        html.Div(
            html.H6('      С учетом сторно, рублей')
        ),
        dbc.Row(
            dbc.Col(html.Div(id='graph2'), width=12)
        ),
        dbc.Row(
            dbc.Col(html.H6('      Сторно исключено, рублей'), width=12)
        ),
        dbc.Row(
            dbc.Col(html.Div(id='graph'), width=12)
        ),
        dbc.Row(
            html.H4('    По дате проводки')
        ),
        dbc.Row(
            html.H6('      С учетом сторно, рублей')
        ),
        dbc.Row(
            dbc.Col(html.Div(id='graph4'), width=12)
        ),
        dbc.Row(
dbc.Col(html.H6('      Сторно исключено, рублей'), width=12)),
        dbc.Row(dbc.Col(html.Div(id='graph3'), width=12)),
        dbc.Row(html.H4('    По дате документа')),
        dbc.Row(html.H6('      С учетом сторно, рублей')),
        dbc.Row(dbc.Col(html.Div(id='graph6'), width=12)),
        dbc.Row(dbc.Col(html.H6('      Сторно исключено, рублей'), width=12)),
        dbc.Row(dbc.Col(html.Div(id='graph5'), width=12))
    #    ,
    ])
    return layout

@app.callback(
    Output(component_id='dogovor', component_property='options'),
    [
        Input(component_id='klient', component_property='value')
    ]
)
def dogovor(klient):
    query3="""
    SELECT DISTINCT(SAPABAP1.BSEG.ZUONR) as ZUONR FROM SAPABAP1.BSEG
    where SAPABAP1.BSEG.KUNNR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    """ % klient
    con = get_connection()
    df6=pd.read_sql(query3, con)
    print(df6.head())
    con.close()
    return [{'label': i, 'value': i} for i in df6['ZUONR']]

@app.callback(
    Output(component_id='graph', component_property='children'),
    [
        Input(component_id='klient', component_property='value'),
        Input(component_id='dogovor', component_property='value')
    ]
)
def content(klient, dogovor):
    query2="""
    SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM, TO_TIMESTAMP(CONCAT(SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM), 'YYYYMMDDHHMISS') as timestamp, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    LEFT JOIN SAPABAP1.BKPF
    ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    """ % (klient, dogovor)

    df=pd.read_sql(query2, connection_hana)
    df4=df.sort_values(['TIMESTAMP'], ascending=True)
    lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
    df4.insert(11, 'LIMIT', 99999999)
    for i, item in enumerate (df4['IND']):
        try:
            df4.iloc[i,11]=int(lim)
        except:
            df4.iloc[i,11]=0
    df5=df4
    df5.insert(12, 'SUMM2', 999999999)
    for i, item in enumerate (df5['IND']):
        if df5.iloc[0,2]=='S':
            df5.iloc[0,12]=df5.iloc[0,6]
        else:
            df5.iloc[0,12]=df5.iloc[0,6]*(-1)
        try:
            if df5.iloc[i+1,2]=='S':
                df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])
            else:
                df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])*(-1)
        except:
            if df5.iloc[i,2]=='S':
                df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])
            else:
                df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])*(-1)
    df5.insert(13, 'ZERO', 9)
    for i, item in enumerate (df5['IND']):
        try:
            df5.iloc[i,13]=int('0')
        except:
            df5.iloc[i,13]=0
    dates=df5['CPUDT']
    dates1=df5['CPUTM']
    points=df5['SUMM2']
    points1=df5['LIMIT']
    dates2=df5['TIMESTAMP']
    points2=df5['ZERO']
    return dcc.Graph(figure=go.Figure(
        data=[go.Scatter(x=[dates2, dates, dates1], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
            go.Scatter(x=[dates2, dates, dates1], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
            go.Scatter(x=dates2, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
        layout=go.Layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showticklabels=False,
                overlaying='x2',
                showdividers=False),
            margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
            legend={'x': 0, 'y': 1},
            showlegend=True
        )
    ), config={'displayModeBar': False})

@app.callback(
    Output(component_id='graph2', component_property='children'),
    [
        Input(component_id='klient', component_property='value'),
        Input(component_id='dogovor', component_property='value')
    ]
)
def content2(klient, dogovor):
    query4="""
    SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM, TO_TIMESTAMP(CONCAT(SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM), 'YYYYMMDDHHMISS') as timestamp, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    LEFT JOIN SAPABAP1.BKPF
    ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    """ % (klient, dogovor)

    df=pd.read_sql(query4, connection_hana)
    df4=df.sort_values(['CPUDT', 'CPUTM'], ascending=[True, True])
    df4.insert(11, 'LIMIT', 99999999)
    lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
    for i, item in enumerate (df4['IND']):
        try:
            df4.iloc[i,11]=int(lim)
        except:
            df4.iloc[i,11]=0
    df5=df4
    df5.insert(12, 'SUMM2', 999999999)
    for i, item in enumerate (df5['IND']):
        if df5.iloc[0,2]=='S':
            df5.iloc[0,12]=df5.iloc[0,6]
        else:
            df5.iloc[0,12]=df5.iloc[0,6]*(-1)
        try:
            if df5.iloc[i+1,2]=='S':
                df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])
            else:
                df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])*(-1)
        except:
            if df5.iloc[i,2]=='S':
                df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])
            else:
                df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])*(-1)
    df5.insert(13, 'ZERO', 9)
    for i, item in enumerate (df5['IND']):
        try:
            df5.iloc[i,13]=int('0')
        except:
            df5.iloc[i,13]=0
    dates=df5['CPUDT']
    dates2=df5['CPUTM']
    points=df5['SUMM2']
    points1=df5['LIMIT']
    dates4=df5['TIMESTAMP']
    points2=df5['ZERO']
    return dcc.Graph(figure=go.Figure(
        data=[go.Scatter(x=[dates4, dates, dates2], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_shape='spline', line_color='grey', xaxis='x1'),
            go.Scatter(x=[dates4, dates, dates2], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
            go.Scatter(x=dates4, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
        layout=go.Layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showticklabels=False,
                overlaying='x2',
                showdividers=False
            ),
            margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
            legend={'x': 0, 'y': 1},
            showlegend=True
        )
    ), config={'displayModeBar': False})

@app.callback(
    Output(component_id='graph3', component_property='children'),
    [
        Input(component_id='klient', component_property='value'),
        Input(component_id='dogovor', component_property='value')
    ]
)
def content3(klient, dogovor):
    query5="""
    SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BUDAT, 'YYYYMMDD') as BUDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    LEFT JOIN SAPABAP1.BKPF
    ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    """ % (klient, dogovor)

    df=pd.read_sql(query5, connection_hana)
    df4=df.sort_values(['BUDAT', 'BELNR'], ascending=[True, True])
    lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
    df4.insert(10, 'LIMIT', 99999999)
    for i, item in enumerate (df4['IND']):
        try:
            df4.iloc[i,10]=int(lim)
        except:
            df4.iloc[i,10]=0
    df5=df4
    df5.insert(11, 'SUMM2', 999999999)
    for i, item in enumerate (df5['IND']):
        if df5.iloc[0,2]=='S':
            df5.iloc[0,11]=df5.iloc[0,6]
        else:
            df5.iloc[0,11]=df5.iloc[0,6]*(-1)
        try:
            if df5.iloc[i+1,2]=='S':
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
            else:
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
        except:
            if df5.iloc[i,2]=='S':
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
            else:
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
    df5.insert(12, 'ZERO', 9)
    for i, item in enumerate (df5['IND']):
        try:
            df5.iloc[i,12]=int('0')
        except:
            df5.iloc[i,12]=0
    dates=df5['BELNR']
    points=df5['SUMM2']
    points1=df5['LIMIT']
    dates2=df5['BUDAT']
    points2=df5['ZERO']
    return dcc.Graph(figure=go.Figure(
        data=[go.Scatter(x=[dates2, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
            go.Scatter(x=[dates2, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
            go.Scatter(x=dates2, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
        layout=go.Layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showticklabels=False,
                overlaying='x2',
                showdividers=False),
            margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
            legend={'x': 0, 'y': 1},
            showlegend=True
        )
    ), config={'displayModeBar': False})

@app.callback(
    Output(component_id='graph4', component_property='children'),
    [
        Input(component_id='klient', component_property='value'),
        Input(component_id='dogovor', component_property='value')
    ]
)
def content4(klient, dogovor):
    query6="""
    SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BUDAT, 'YYYYMMDD') as BUDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    LEFT JOIN SAPABAP1.BKPF
    ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    """ % (klient, dogovor)

    df=pd.read_sql(query6, connection_hana)
    df4=df.sort_values(['BUDAT', 'BELNR'], ascending=[True, True])
    df4.insert(10, 'LIMIT', 99999999)
    lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
    for i, item in enumerate (df4['IND']):
        try:
            df4.iloc[i,10]=int(lim)
        except:
            df4.iloc[i,10]=0
    df5=df4
    df5.insert(11, 'SUMM2', 999999999)
    for i, item in enumerate (df5['IND']):
        if df5.iloc[0,2]=='S':
            df5.iloc[0,11]=df5.iloc[0,6]
        else:
            df5.iloc[0,11]=df5.iloc[0,6]*(-1)
        try:
            if df5.iloc[i+1,2]=='S':
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
            else:
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
        except:
            if df5.iloc[i,2]=='S':
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
            else:
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
    df5.insert(12, 'ZERO', 9)
    for i, item in enumerate (df5['IND']):
        try:
            df5.iloc[i,12]=int('0')
        except:
            df5.iloc[i,12]=0
    dates=df5['BELNR']
    points=df5['SUMM2']
    points1=df5['LIMIT']
    dates4=df5['BUDAT']
    points2=df5['ZERO']
    return dcc.Graph(figure=go.Figure(
        data=[go.Scatter(x=[dates4, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_shape='spline', line_color='grey', xaxis='x1'),
            go.Scatter(x=[dates4, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
            go.Scatter(x=dates4, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
        layout=go.Layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showticklabels=False,
                overlaying='x2',
                showdividers=False
            ),
            margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
            legend={'x': 0, 'y': 1},
            showlegend=True
        )
    ), config={'displayModeBar': False})

@app.callback(
    Output(component_id='graph5', component_property='children'),
    [
        Input(component_id='klient', component_property='value'),
        Input(component_id='dogovor', component_property='value')
    ]
)

def content5(klient, dogovor):
    query7="""
    SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BLDAT, 'YYYYMMDD') as BLDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    LEFT JOIN SAPABAP1.BKPF
    ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    """ % (klient, dogovor)

    df=pd.read_sql(query7, connection_hana)
    df4=df.sort_values(['BLDAT', 'BELNR'], ascending=[True, True])
    lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
    df4.insert(10, 'LIMIT', 99999999)
    for i, item in enumerate (df4['IND']):
        try:
            df4.iloc[i,10]=int(lim)
        except:
            df4.iloc[i,10]=0
    df5=df4
    df5.insert(11, 'SUMM2', 999999999)
    for i, item in enumerate (df5['IND']):
        if df5.iloc[0,2]=='S':
            df5.iloc[0,11]=df5.iloc[0,6]
        else:
            df5.iloc[0,11]=df5.iloc[0,6]*(-1)
        try:
            if df5.iloc[i+1,2]=='S':
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
            else:
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
        except:
            if df5.iloc[i,2]=='S':
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
            else:
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
    df5.insert(12, 'ZERO', 9)
    for i, item in enumerate (df5['IND']):
        try:
            df5.iloc[i,12]=int('0')
        except:
            df5.iloc[i,12]=0
    dates=df5['BELNR']
    points=df5['SUMM2']
    points1=df5['LIMIT']
    dates2=df5['BLDAT']
    points2=df5['ZERO']
    return dcc.Graph(figure=go.Figure(
        data=[go.Scatter(x=[dates2, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
            go.Scatter(x=[dates2, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
            go.Scatter(x=dates2, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
        layout=go.Layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showticklabels=False,
                overlaying='x2',
                showdividers=False),
            margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
            legend={'x': 0, 'y': 1},
            showlegend=True
        )
    ), config={'displayModeBar': False})

@app.callback(
    Output(component_id='graph6', component_property='children'),
    [
        Input(component_id='klient', component_property='value'),
        Input(component_id='dogovor', component_property='value')
    ]
)
def content6(klient, dogovor):
    query8="""
    SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BLDAT, 'YYYYMMDD') as BLDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    LEFT JOIN SAPABAP1.BKPF
    ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    """ % (klient, dogovor)

    df=pd.read_sql(query8, connection_hana)
    df4=df.sort_values(['BLDAT', 'BELNR'], ascending=[True, True])
    df4.insert(10, 'LIMIT', 99999999)
    lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
    for i, item in enumerate (df4['IND']):
        try:
            df4.iloc[i,10]=int(lim)
        except:
            df4.iloc[i,10]=0
    df5=df4
    df5.insert(11, 'SUMM2', 999999999)
    for i, item in enumerate (df5['IND']):
        if df5.iloc[0,2]=='S':
            df5.iloc[0,11]=df5.iloc[0,6]
        else:
            df5.iloc[0,11]=df5.iloc[0,6]*(-1)
        try:
            if df5.iloc[i+1,2]=='S':
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
            else:
                df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
        except:
            if df5.iloc[i,2]=='S':
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
            else:
                df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
    df5.insert(12, 'ZERO', 9)
    for i, item in enumerate (df5['IND']):
        try:
            df5.iloc[i,12]=int('0')
        except:
            df5.iloc[i,12]=0
    dates=df5['BELNR']
    points=df5['SUMM2']
    points1=df5['LIMIT']
    dates4=df5['BLDAT']
    points2=df5['ZERO']
    return dcc.Graph(figure=go.Figure(
        data=[go.Scatter(x=[dates4, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_shape='spline', line_color='grey', xaxis='x1'),
            go.Scatter(x=[dates4, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
            go.Scatter(x=dates4, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
        layout=go.Layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showticklabels=False,
                overlaying='x2',
                showdividers=False
            ),
            margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
            legend={'x': 0, 'y': 1},
            showlegend=True
        )
    ), config={'displayModeBar': False})
