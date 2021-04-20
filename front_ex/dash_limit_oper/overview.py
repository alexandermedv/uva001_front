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

from sqlalchemy import create_engine
from . import dash_app as app
from .utils import get_limit_oper_data, get_limit_oper_ttl_data, get_limit_oper_client_data, get_limit_oper_zuonr_data, get_limit_oper_client_zuonr_data
from .utils import get_limit_oper_client_zuonr_data, get_limit1


def create_layout(app, start_date = None, end_date=None, debug=False):  
    limit_oper_client_data = get_limit_oper_client_data()

    print('1. Загрузка данных из Excel по лимитам')
    # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
    # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
    # print(file)
    # xl = pd.ExcelFile(file)
    dflim = get_limit1().rename(columns={'KUNNR':'kunnr', 'ZUONR': 'zuonr', 'GSBER':'gsber', 'LIMIT':'limit', 'SAP':'sap'})
    # dflim = xl.parse('BSEG').rename(columns={'KUNNR':'kunnr', 'ZUONR': 'zuonr', 'GSBER':'gsber', 'LIMIT':'limit', 'SAP':'sap'})

    print('2. Загрузка данных по контрактам')
    limit_oper_data = get_limit_oper_data() 

    print('3. Загрузка агрегированных данных')
    limit_oper_ttl_data = get_limit_oper_ttl_data()
    dfreit1 = limit_oper_ttl_data

    print('4. Пересчет дат')
    dflim1=dflim[['zuonr', 'limit', 'sap']]
    dfreit2=dfreit1.merge(dflim1, on='zuonr', how='left')

    # dfreit2.insert(8, 'prev', '')
    # print(dfreit2.head(3))

    # dfreit_test = dfreit2[['max_dz','limit']][0:10].copy()

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

    # Узкое место по скорости    
    dfreit2['prev'] = dfreit2[['max_dz','limit']].apply(lambda x: set_prev(x), axis=1)
    dfreit2.head(10)

    # dfreit2.insert(9, 'delta', '')

    def set_delta (x):
        try:
            delta = x[0] - x[1]
        except:
            delta = 'e'
    dfreit2['delta'] = dfreit2[['max_dz','limit']].apply(lambda x: set_prev(x), axis=1)
    
    dfreit3=dfreit2[(dfreit2['delta']>0)&(dfreit2['limit']>0)]
    dfreit4=dfreit3.pivot_table(['prev', 'delta'], ['zuonr', 'kunnr', 'limit', 'sap'], aggfunc={'prev': 'sum', 'delta': [max, min]}).reset_index()
    dfreit4.columns = dfreit4.columns.map(''.join)
    dfreit6=dfreit4.merge(limit_oper_client_data, on='kunnr', how='left').sort_values(['prevsum'], ascending=False)
    dfreit7=dfreit6.merge(dflim[['zuonr', 'gsber']], on='zuonr', how='left')
    dfreit6.columns=['Договор', 'Клиент', 'Лимит', 'Лимит в SAP (1-да, 0-нет)', 'Макс_превышение', 'Мин_превышение', 'Кол-во превышений', 'Имя клиента']

    dfreit8=dfreit7.pivot_table(['kunnr','deltamax', 'deltamin', 'prevsum'], ['gsber', 'sap'], aggfunc={'kunnr': 'count', 'deltamax': 'sum', 'deltamin': 'sum', 'prevsum': 'sum'}).reset_index()
    dfreit8.columns=['Филиал', 'Лимит в SAP (1-да, 0-нет)', 'Сумма Макс_превышение', 'Сумма Мин_превышение', 'Кол-во договоров', 'Сумма превышений']
    print("5. Старт загрузки layout")

    layout = html.Div([
        dbc.Navbar([
            html.Div('Выберите клиента:', style={'width': '15%', 'display': 'inline-block', 'color': 'white'}),
            html.Div(dcc.Dropdown(id='klient', 
                                        options=[{'label':limit_oper_client_data['name1'][limit_oper_client_data['kunnr']==klient], 'value': klient} for klient in limit_oper_client_data['kunnr']], 
                                        value='0001000134'), style={'width': '25%', 'display': 'inline-block'}),
            html.Div('Выберите договор:', style={'width': '15%', 'display': 'inline-block', 'color': 'white'}),
            html.Div(dcc.Dropdown(id='dogovor'), style={'width': '25%', 'display': 'inline-block'})
        # ], dark=True, sticky="top", color='rgb(71, 71, 71)'),
        ], dark=True, color='rgb(71, 71, 71)'),
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
    ], className='twelve columns')
    return layout

@app.callback(
    Output(component_id='dogovor', component_property='options'),
    [
        Input(component_id='klient', component_property='value')
    ]
)
def dogovor(klient):
    print('dogovor')
    # query3="""
    # SELECT DISTINCT(SAPABAP1.BSEG.ZUONR) as ZUONR FROM SAPABAP1.BSEG
    # where SAPABAP1.BSEG.KUNNR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    # """ % klient
    # con = get_connection()
    # df6=pd.read_sql(query3, con)
    df = get_limit_oper_zuonr_data(klient)
    print(df.head())
    if df.empty:
        return None
    else:
        # print('dogovor', df.head())
        # con.close()
        # return [{'label': i, 'value': i} for i in df['zuonr']]
        return None
@app.callback(
    Output(component_id='graph', component_property='children'),
    [
        Input(component_id='klient', component_property='value'),
        Input(component_id='dogovor', component_property='value')
    ]
)
def content(klient, dogovor):
    print('graph')
    # query2="""
    # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM, 
    #     TO_TIMESTAMP(CONCAT(SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM), 'YYYYMMDDHHMISS') as timestamp, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    # LEFT JOIN SAPABAP1.BKPF
    # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    # """ % (klient, dogovor)
    
    # con = get_connection()
    df = get_limit_oper_client_zuonr_data(klient, dogovor)
    if df.empty:
        print('None')
        return None
    else: 
        # df=pd.read_sql(query2, con)
        # con.close()

        # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
        # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
        # xl = pd.ExcelFile(file)
        # dflim = xl.parse('BSEG')
        dflim = get_limit1()

        df4=df.sort_values(['timestamp'], ascending=True)
        lim=dflim[dflim['zuonr']==dogovor]['limit'].max()
        df4.insert(11, 'limit', 99999999)
        for i, item in enumerate (df4['ind']):
            try:
                df4.iloc[i,11]=int(lim)
            except:
                df4.iloc[i,11]=0
        df5=df4
        df5.insert(12, 'summ2', 999999999)
        for i, item in enumerate (df5['ind']):
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
        df5.insert(13, 'zero', 9)
        for i, item in enumerate (df5['ind']):
            try:
                df5.iloc[i,13]=int('0')
            except:
                df5.iloc[i,13]=0
        dates=df5['cpudt']
        dates1=df5['cputm']
        points=df5['summ2']
        points1=df5['limit']
        dates2=df5['timestamp']
        points2=df5['zero']
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
    # query4="""
    # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM, TO_TIMESTAMP(CONCAT(SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM), 'YYYYMMDDHHMISS') as timestamp, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    # LEFT JOIN SAPABAP1.BKPF
    # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    # """ % (klient, dogovor)

    # con = get_connection()
    print('graph2')
    df = get_limit_oper_client_zuonr_data(klient, dogovor)

    if df.empty:
        return None
    else: 
        # df=pd.read_sql(query4, con)
        # con.close()

        # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
        # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
        # xl = pd.ExcelFile(file)
        # dflim = xl.parse('BSEG')
        dflim = get_limit1()

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
    # query5="""
    # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BUDAT, 'YYYYMMDD') as BUDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    # LEFT JOIN SAPABAP1.BKPF
    # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    # """ % (klient, dogovor)

    # con = get_connection()
    print('graph3')
    df = get_limit_oper_client_zuonr_data(klient, dogovor)
    if df.empty:
        return None
    else: 
        # df=pd.read_sql(query5, con)
        # con.close()

        # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
        # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
        # xl = pd.ExcelFile(file)
        # dflim = xl.parse('BSEG')
        dflim = get_limit1()

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
    # query6="""
    # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BUDAT, 'YYYYMMDD') as BUDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    # LEFT JOIN SAPABAP1.BKPF
    # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    # """ % (klient, dogovor)

    # con = get_connection()
    print('graph4')
    df = get_limit_oper_client_zuonr_data(klient, dogovor)
    # df=pd.read_sql(query6, con)
    # con.close()

    # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
    # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
    # xl = pd.ExcelFile(file)
    # dflim = xl.parse('BSEG')
    if df.empty:
        return None
    else: 
        dflim = get_limit1()

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
    # query7="""
    # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BLDAT, 'YYYYMMDD') as BLDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    # LEFT JOIN SAPABAP1.BKPF
    # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    # """ % (klient, dogovor)
    print('graph5')
    # con =get_connection()
    df=get_limit_oper_client_zuonr_data(klient, dogovor)
    # print(df.head(3))
    # df=pd.read_sql(query7, con)
    # con.close()

    # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
    # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
    # xl = pd.ExcelFile(file)
    # dflim = xl.parse('BSEG')
    # print(dflim.head(3))
    dflim = get_limit1()
    if df.empty:
        return None
    else:     
        print('df')
        df4=df.sort_values(['bldat', 'belnr'], ascending=[True, True])
        lim=dflim[dflim['zuonr']==dogovor]['limit'].max()
        df4.insert(10, 'limit', 99999999)
        for i, item in enumerate (df4['ind']):
            try:
                df4.iloc[i,10]=int(lim)
            except:
                df4.iloc[i,10]=0
        df5=df4
        df5.insert(11, 'summ2', 999999999)
        for i, item in enumerate (df5['ind']):
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
        df5.insert(12, 'zero', 9)
        for i, item in enumerate (df5['ind']):
            try:
                df5.iloc[i,12]=int('0')
            except:
                df5.iloc[i,12]=0
        dates=df5['belnr']
        points=df5['summ2']
        points1=df5['limit']
        dates2=df5['bldat']
        points2=df5['zero']
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
    # query8="""
    # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BLDAT, 'YYYYMMDD') as BLDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
    # LEFT JOIN SAPABAP1.BKPF
    # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
    # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
    # """ % (klient, dogovor)

    # con = get_connection()
    print('graph6')
    df = get_limit_oper_client_zuonr_data(klient, dogovor)
    
    # df=pd.read_sql(query8, con)
    # con.close()
    if df.empty:
        return None
    else: 
        df4=df.sort_values(['bldat', 'belnr'], ascending=[True, True])
        df4.insert(10, 'limit', 99999999)

        # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
        # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
        # xl = pd.ExcelFile(file)
        # dflim = xl.parse('BSEG')
        dflim = get_limit1()

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
