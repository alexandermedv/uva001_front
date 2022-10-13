import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
# from dash.dash_table.Format import Format, Group
import dash_bootstrap_components as dbc
import dash_table
from datetime import date
import pandas as pd
import os
from functools import lru_cache
import pyhdb
import datetime as dt
from datetime import datetime
import numpy as np

from sqlalchemy import create_engine
from . import dash_app as app
from ..utils import  get_credit_data, get_credit_data_all, get_credit_data_clients#get_credit_data_filials,
# from .utils import get_limit_oper_client_zuonr_data, get_limit1, get_limit
def sum_nonlimit(s , n=0.13):
    if n in s.values:
        return n
    else:
        return s.sum()
def get_matrix_stat_1(df3_1, s_d=None, e_d=None):
    if s_d is not None:
        df3_1=df3_1[df3_1['date']>=s_d]
    if e_d is not None:
        df3_1=df3_1[df3_1['date']<=e_d]
    if df3_1.shape[0]==0:
        return pd.DataFrame()
    df3_1=df3_1.sort_values([ 'id_rcm', 'client_name','date'])
    df6=pd.DataFrame()
    i0=0
    res=0
    dg_n=0
    for dg, dt, dp in df3_1[[ 'id_rcm', 'date','dept_over_lim']].values:
        if dg_n==0:
            # set_trace()
            dg_n=dg
            m=dp
        elif  dg_n!=dg:
            # set_trace()
            # print(dg)
            df6_1=pd.DataFrame({'id_rcm': [dg_n],
            'res': [res],
            'max': [m]})
            df6=pd.concat([df6, df6_1], ignore_index=True)
            if (dp>0):
                res=1
                i0=dp
            else:
                i0=0
            m=dp
            dg_n=dg
        else:
            if (i0==0) & (dp>0):
                res=res+1
                i0=dp
            elif (dp==0):
                i0=0
            if dp>m:
                m=dp
    df6_1=pd.DataFrame({'id_rcm': [dg_n],
            'res': [res],
            'max': [m]})
    df6=pd.concat([df6, df6_1], ignore_index=True)
    col0=[i  for i in ['client_name', 
        'dog_number',
       # 'date',  
        'dinamic_saldo', 'lim_sum',
       'dept_over_lim', #'rating', 'garanty',
       'res','max'] if (i in df3_1.columns) | (i in df6.columns )]
    
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    # df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)

    return df3_1.loc[df3_1['date']==df3_1['date'].max(),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)
def get_matrix_stat_2(df3_1,  e_d=None):
    if (e_d is None) :
        df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),['client_name', 'dog_number', 
         'dinamic_saldo', #'rating', 'garanty',
         ]]
    else:
        df3_1=df3_1.loc[df3_1['date']==e_d,['client_name', 'dog_number', 
         'dinamic_saldo', #'rating', 'garanty',
         ]]
    df3_1['postpone_pay']=np.nan
    df3_1['prosrochka']=np.nan
    df3_1['percent']=np.nan
        
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    
    return df3_1.sort_values(['dinamic_saldo', ],  ascending=False)

def get_dates_for_table():
    print('1. Загрузка данных')
    df = get_credit_data()
    
    print('2. Все контракты')
    df_dog_2=df.loc[(df['3_group']==2) , ['id_rcm','client_name', 'dog_number', 
       'date',  'dinamic_saldo', 'lim_sum', 'rating', 'garanty',
       'dept_over_lim']]
    df_dog_3=df.loc[(df['3_group']==3) , ['id_rcm','client_name', 'dog_number', 
       'date',  'dinamic_saldo', 'rating', 'garanty',
       ]]
    df_dog_1=df.loc[(df['3_group']==1) , ['id_rcm','client_name', 'dog_number', 
       'date',  'dinamic_saldo', 'rating', 'dept_over_lim'
       ]]
    # df_dog_2_1=get_matrix_stat_1(df_dog_2)
    # df_dog_3_1=get_matrix_stat_2(df_dog_3)
    # df_dog_1_1=get_matrix_stat_1(df_dog_1)
    return [df_dog_1,df_dog_2,df_dog_3]

def create_layout(): 
    df_dog_1,df_dog_2,df_dog_3=get_dates_for_table()
    df_dog_2_1=get_matrix_stat_1(df_dog_2)
    df_dog_3_1=get_matrix_stat_2(df_dog_3)
    df_dog_1_1=get_matrix_stat_1(df_dog_1)
    # contracts_2 = df_dog_2[['dog_number', 'id_rcm']].drop_duplicates()
    # clients_2 = df_dog_2[[ 'client_name']].drop_duplicates()
       
    
    # print('3. Все клиенты')
    # df_clients0=get_credit_data_clients()
    # df_clients=df_clients0[df_clients0['date']=='2022-08-31'].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)
    # clients = df_clients0[[ 'client_name']].drop_duplicates()
    # print('4. Все филиалы')
    # df_filial0=get_credit_data_filials()
    # df_filial0.loc[:,['dinamic_saldo', 'dept_over_lim','debitor','dept_over_lim_y', ] ] *=-1

    # df_filial=df_filial0[df_filial0['date']=='2022-08-31']
    # filials = df_filial['filial'].drop_duplicates()
    print('5. Все и безлимитные')
    df_all0=get_credit_data_all()
    max_date=df_all0['date'].max()
    min_date=df_all0['date'].min()
    df_all0=df_all0.set_index('date')
    col_name_rus={
        'clients_count':['Кол-во превышений лимита','numeric', 1],
        'postpone_pay':['Кол-во дней отсрочки платежа','numeric', 1],
        'prosrochka':['Просроченная задолжность','numeric', 1],
        'percent':['Доля долга','percent', 1],
        'res':['Кол-во превышений лимита','numeric', 1], 
        'max':['Максимальное превышение лимита','numeric', 1],
        'rating':['Рейтинг','numeric', 1],
        'garanty':['Гарантии','numeric', 1],
        'date':['Дата','str', 0],
        'client':['id клиента','numeric', 0], 
        'client_name':['Клиента','str', 0],
        'id_rcm':['id договора','numeric', 0], 
        'filial':['Филиал','str', 0],
        'dog_number':['Договор','str', 0],
        'dinamic_saldo':['Сальдо','numeric', 1],
        'lim_sum':['Лимит','numeric', 1], 
        'dept_over_lim':['Превышение лимита','numeric', 1], 
        'dinamic_saldo_X':['Сальдо безлимитных','numeric', 1],
        'debitor':['debitor','numeric', 1],   
        'debitor_X':['debitor_X','numeric', 1], 

        'dinamic_saldo_min':['Минимальное сальдо','numeric', 1], 
        'dinamic_saldo_mean_below_zero':['Средняя задолженность','numeric', 1], 
        'dept_over_lim_min':['Максимальное превышение лимита','numeric', 1], 
        'dept_over_lim_mean':['Среднее превышение лимита','numeric', 1],
        'days_over_limit_max':['Максимум дней выше лимита','numeric', 1], 
        'days_over_limit_mean':['Среднее число дней выше лимита','numeric', 1], 
        'days_over_limit_count_days_over':['Число превышений лимита','numeric', 1], 
        'days_over_limit':['Текущее число дней выше лимита','numeric', 1], 
        'debitor_min':['debitor_min','numeric', 1], 
        'debitor_mean_below_zero':['debitor_mean_below_zero','numeric', 1], 
        'dept_over_lim_min_y':['dept_over_lim_min_y','numeric', 1],
        'dept_over_lim_mean_y':['dept_over_lim_mean_y','numeric', 1], 
        'days_over_limit_max_y':['days_over_limit_max_y','numeric', 1], 
        'days_over_limit_mean_y':['days_over_limit_mean_y','numeric', 1], 
        'days_over_limit_count_days_over_y':['days_over_limit_count_days_over_y','numeric', 1],
        'dept_over_lim_y':['dept_over_lim_y','numeric', 1], 
        'days_over_limit_y':['days_over_limit_y','numeric', 1]
	
    }
    
    
    dates=df_all0.index.date

    df_all0_M=df_all0.groupby([pd.Grouper( freq="1M"),'3_group']).mean().reset_index(1)
    df_all0_M_1=df_all0_M[df_all0_M['3_group']==1]
    df_all0_M_2=df_all0_M[df_all0_M['3_group']==2]
    df_all0_M_3=df_all0_M[df_all0_M['3_group']==3]
    dates1_1=df_all0_M_1.index.date
    dates1_2=df_all0_M_2.index.date
    dates1_3=df_all0_M_3.index.date
    df_all0_M_1=df_all0_M_1.reset_index()
    df_all0_M_2=df_all0_M_2.reset_index()
    df_all0_M_3=df_all0_M_3.reset_index()
    # df_all0_M['date'] = df_all0_M['date'].dt.strftime('%m-%Y')
    
    # df_filial['date'] = df_filial['date'].dt.strftime('%d/%m/%Y')
    # df_clients['date'] = df_clients['date'].dt.strftime('%d/%m/%Y')
    # points1=df_all0['lim_sum'].values
    points_1=df_all0_M_3['dinamic_saldo'].values
    points_1_c=df_all0_M_1['clients_count'].values
    points_2=df_all0_M_2['dinamic_saldo'].values
    points_3=df_all0_M_3['dinamic_saldo'].values

    # points3=df_all0['dinamic_saldo_X'].values
    # points4=df_all0['dept_over_lim'].values
    points_1_0=[0 for i in dates1_1]
    points_2_0=[0 for i in dates1_2]
    points_3_0=[0 for i in dates1_3]
    print("5. Старт загрузки layout")

    layout = html.Div(
        [
            html.Div(
                html.H5("Отчет кредитных рисков"), className='row', 
                style={'marginBottom': 15, 'margin-left': 30,'marginTop': 40}
            ),
            dcc.Graph(
                id="all_bar",
                figure=go.Figure(
                    data=[
                        go.Bar(name='Отсрочка платежа без потолка лимита', x=dates1_1, y=df_all0_M_1['dinamic_saldo'].values,
                        hovertemplate =
                                '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1'),
                        go.Bar(name='Кредитный лимит с отсрочкой платежа', x=dates1_2,hovertemplate =
                                '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>', y=points_2, xaxis='x1'),
                        go.Bar(name='Предоплата', x=dates1_3, y=points_3,hovertemplate =
                                '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1')
                    ],
                    
                    layout=go.Layout(
                        title= 'Помесячная динамика дебиторской задолженности',
                        barmode='stack',
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        # xaxis=dict(
                        #     showticklabels=False,
                        #     overlaying='x2',
                        #     showdividers=False),
                        margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
                        legend={'x': 0, 'y': 1},
                        showlegend=True
                    )
                ), style={'width': '80%'},
                config={'displayModeBar': False}
            ),
            dcc.Graph(
                id="all_limit",
                figure=go.Figure(
                    data=[
                        go.Scatter(x=dates1_2, y=points_2, mode='lines',
                        hovertemplate =
                                '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>',
                          name= 'Динамическое сальдо долг', #line_color='rgb(40,80,0)', 
                        fill='tonexty',line_shape='spline', xaxis='x1'),
                        # go.Bar(name='Динамическое сальдо долг', x=dates1_2, y=points_2, xaxis='x1'),
                        go.Scatter(x=dates1_2, y=df_all0_M_2['lim_sum'].values, mode='lines',
                        hovertemplate =
                                '<i><b>Лимит</b></i>: \u20bd %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>',
                         name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
                        go.Scatter(x=dates1_2, y=points_2_0, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2'),
                        go.Scatter(x=dates1_2, y=[4800000000 for i in dates1_2], hoverinfo='none',mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, xaxis='x2')

                        ],
                    layout=go.Layout(
                        title= 'Динамика задолженности клиентов с кредитным лимитом с отсрочкой платежа',
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        xaxis=dict(
                            showticklabels=False,
                            overlaying='x2',
                            showdividers=False),
                        margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
                        legend={'x': 0, 'y': 1},
                        showlegend=True
                    )
                ), style={'width': '80%'},
                config={'displayModeBar': False}
            ),
            html.Div(    dbc.Navbar(
                [
                    html.Div('Выберите начальную дату:', 
                        style={'width': '15%', 
                        'display': 'inline-block', 'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
                        'color': 'white'}
                    ),
                    dcc.DatePickerSingle(
                        # calendar_orientation='vertical',
                        clearable=True,
                        id='risk_str_date',
                        date=min_date,
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        initial_visible_month=min_date,
                        number_of_months_shown = 3,
                        display_format='DD.MM.YYYY',
                        style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
                    ),
                    html.Div('Выберите последнюю дату:', 
                        style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
                    ),
                    dcc.DatePickerSingle(
                        calendar_orientation='vertical',
                        clearable=True,
                        id='risk_end_date',
                        date=max_date,
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        initial_visible_month=min_date,
                        number_of_months_shown = 3,
                        display_format='DD.MM.YYYY',
                        style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
                    ),
                    html.Button('Submit', id='submit-val', n_clicks=0,
                        style={'width': '15%', 'display': 'inline-block', 'background-color': 'white', }),
                ],dark=True, color='rgb(71, 71, 71)'
                )
            ),

            html.Div([
                html.H6('Детальная информация по задолженности клиентов с кредитным лимитом с отсрочкой платежа'),
                dbc.Col(dash_table.DataTable(
                    id='datatable_clients_limit',
                    columns=[{"name": col_name_rus[i][0], "id": i,
                    #  "deletable": True, 
                     'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
                    {"name": col_name_rus[i][0], "id": i,
                    #  "deletable": True, 
                     'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
                     for i in    df_dog_2_1.columns if i not in ['rating', 'garanty']],
                    data=(df_dog_2_1).to_dict('records'),
                    # editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    # column_selectable="single",
                    # row_selectable="multi",
                    # row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    # page_action="native",
                    # page_current= 0,
                    page_size= 10, 
                    # style_cell = {'textAlign': 'center'},
                    style_cell={
                            'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'right'
                        },
                    style_as_list_view=True,
                    style_table={#'height': 530, 
                            # 'width':800,
                            'overflowY': 'auto',
                            'lineHeight': '30px'},
                    style_header={
                                # 'backgroundColor': 'rgb(138,36,50)',
                                # 'color': 'white',
                                'whiteSpace':'normal',
                                # 'fontWeight': 'bold',
                                # 'font_size': '16px'
                                'overflowY': 'auto',
                                'height': 'auto',
                    },
                    style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'font_size': '12px',
                            'line-height': 0.9
                            # 'width': '100px',
                            # 'maxWidth': '100px',
                            # 'minWidth': '100px',
                        },
                    # style_data_conditional=[
                    #     {'if': {'column_id': 'Лимит в SAP'},
                    #     'width': '35px'},
                    # ]
                ), width=12),
                dcc.Graph(
                id="all_x",
                figure=go.Figure(
                    data=[
                        go.Scatter(x=dates1_3, y=points_3, mode='lines', hovertemplate =
                                '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>',
                        name= 'Динамическое сальдо долг', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
                        go.Scatter(x=dates1_3, y=points_3_0, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
                    ],
                    layout=go.Layout(
                        title= 'Динамика задолженности клиентов с отсрочкой платежа без потолка лимита',
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        xaxis=dict(
                            showticklabels=False,
                            overlaying='x2',
                            showdividers=False),
                        margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
                        legend={'x': 0, 'y': 1},
                        showlegend=True
                    )
                ), style={'width': '80%'},
                config={'displayModeBar': False}
            ),
                html.H6('Детальная информация по задолженности клиентов с отсрочкой платежа без потолка лимита'),
                dbc.Col(dash_table.DataTable(
                    id='datatable_clients_X',
                    columns=[{"name": col_name_rus[i][0], "id": i,
                     "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
                    {"name": col_name_rus[i][0], "id": i,
                     "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
                     for i in    df_dog_3_1.columns],
                    data=(df_dog_3_1).to_dict('records'),
                    # editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    # column_selectable="single",
                    # row_selectable="multi",
                    # row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10, 
                   # style_cell = {'textAlign': 'center'},
                    style_cell={
                            'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'right'
                        },
                    style_as_list_view=True,
                    style_table={#'height': 530, 
                            # 'width':800,
                            'overflowY': 'auto',
                            'lineHeight': '30px'},
                    style_header={
                                # 'backgroundColor': 'rgb(138,36,50)',
                                # 'color': 'white',
                                'whiteSpace':'normal',
                                # 'fontWeight': 'bold',
                                # 'font_size': '16px'
                                'overflowY': 'auto',
                                'height': 'auto',
                    },
                    style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'font_size': '12px',
                            'line-height': 0.9
                            # 'width': '100px',
                            # 'maxWidth': '100px',
                            # 'minWidth': '100px',
                        }, 
                    # style_data_conditional=[
                    #     {'if': {'column_id': 'Лимит в SAP'},
                    #     'width': '35px'},
                    # ]
                ), width=12),
                dcc.Graph(
                    id="all_prepaid",
                    figure=go.Figure(
                        data=[
                            go.Bar(x=dates1_1, y=points_1_c,  yaxis='y1',
                            hovertemplate =
                                '<i><b>Кол-во клиентов</b></i>:  %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>',  width=500000000, name= 'Кол-во клиентов', xaxis='x1', opacity=0.5),
                            go.Scatter(x=dates1_1, y=points_1, mode='lines', name= 'Динамическое сальдо долг',
                            hovertemplate =
                                '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
                                '<br><b>Дата</b>: %{x}<br><extra></extra>',
                                   yaxis='y2',#line_color='rgb(40,80,0)', 
                            line_shape='spline'),
                            go.Scatter(x=dates1_1, y=[12000000000 for i in dates1_1],
                                hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y2', xaxis='x2'),
                            go.Scatter(x=dates1_1, y=[200 for i in dates1_1]
                            , hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y1', xaxis='x2'),
                            # go.Scatter(x=dates1_1, y=points_1_c, mode='bar', secondary_y=True,name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
                            go.Scatter(x=dates1_1, y=points_1_0, mode='lines',
                                hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, yaxis='y1',xaxis='x2')
                        ],
                        layout=go.Layout(
                            title= 'Динамика задолженности предоплатных клиентов ',
                            plot_bgcolor='white',
                            paper_bgcolor='white',
                            xaxis=dict(
                                showticklabels=False,
                                overlaying='x2',
                                showdividers=False),
                            yaxis=dict(title='Кол-во клиентов', side='right'),
                            yaxis2=dict(title='Долг',
                                    overlaying='y',
                                    side='left'),
                            margin={'l': 30, 'b': 30, 't': 40, 'r': 0},
                            legend={'x': 0, 'y': 1},
                            showlegend=True
                        )
                    ), style={'width': '80%'},
                    config={'displayModeBar': False}
                ),
                html.H6('Детальная информация по задолженности предоплатных клиентов'),
                dbc.Col(dash_table.DataTable(
                    id='datatable_clients_prepaid',
                    columns=[{"name": col_name_rus[i][0], "id": i,
                     "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
                    {"name": col_name_rus[i][0], "id": i,
                     "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
                     for i in    df_dog_1_1.columns],
                    data=(df_dog_1_1).to_dict('records'),
                    # editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    # column_selectable="single",
                    # row_selectable="multi",
                    # row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10, 
                    # style_cell = {'textAlign': 'center'},
                    style_cell={
                            'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'right'
                        },
                    style_as_list_view=True,
                    style_table={#'height': 530, 
                            # 'width':800,
                            'overflowY': 'auto',
                            'lineHeight': '30px'},
                    style_header={
                                # 'backgroundColor': 'rgb(138,36,50)',
                                # 'color': 'white',
                                'whiteSpace':'normal',
                                # 'fontWeight': 'bold',
                                # 'font_size': '16px'
                                'overflowY': 'auto',
                                'height': 'auto',
                    },
                    style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'font_size': '12px',
                            'line-height': 0.9
                            # 'width': '100px',
                            # 'maxWidth': '100px',
                            # 'minWidth': '100px',
                        },
                    # style_data_conditional=[
                    #     {'if': {'column_id': 'Лимит в SAP'},
                    #     'width': '35px'},
                    # ]
                ), width=12)

 ], className='eleven columns', style={'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
                        }),
        ], 
        className='twelve columns', style={'fontSize': 12})
    return layout

