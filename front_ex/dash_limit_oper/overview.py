# from dash import dcc
# from dash import html
# import dash_html_components as html
from dash import html
# import dash_core_components as dcc
from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
# from dash.dash_table.Format import Format, Group
import dash_bootstrap_components as dbc
# import dash_table
from dash import dash_table
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
from .utils import  get_credit_data, get_credit_data_all, get_credit_data_clients#get_credit_data_filials,
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
       'dept_over_lim', 'rating', 'garanty','res','max'] if (i in df3_1.columns) | (i in df6.columns )]
    return df3_1.loc[df3_1['date']==df3_1['date'].max(),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)
def get_matrix_stat_2(df3_1,  e_d=None):
    if (e_d is None) :
        df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),['client_name', 'dog_number', 
         'dinamic_saldo', 'rating', 'garanty',]]
    else:
        df3_1=df3_1.loc[df3_1['date']==e_d,['client_name', 'dog_number', 
         'dinamic_saldo', 'rating', 'garanty',]]
    df3_1['postpone_pay']=np.nan
    df3_1['prosrochka']=np.nan
    df3_1['percent']=np.nan
    return df3_1.sort_values(['dinamic_saldo', ],  ascending=False)

def get_dates_for_table():
    # print('1. Загрузка данных')
    df = get_credit_data()
    
    # print('2. Все контракты')
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

def create_layout(app, start_date = None, end_date=None, debug=False): 
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
    # print('5. Все и безлимитные')
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
    # print("5. Старт загрузки layout")

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
                        go.Bar(name='Безлимитные', x=dates1_1, y=df_all0_M_1['dinamic_saldo'].values, xaxis='x1'),
                        go.Bar(name='Лимитные', x=dates1_2, y=points_2, xaxis='x1'),
                        go.Bar(name='Предоплатные', x=dates1_3, y=points_3, xaxis='x1')
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
                        go.Scatter(x=dates1_2, y=points_2, mode='lines',  name= 'Динамическое сальдо долг', #line_color='rgb(40,80,0)', 
                        fill='tonexty',line_shape='spline', xaxis='x1'),
                        # go.Bar(name='Динамическое сальдо долг', x=dates1_2, y=points_2, xaxis='x1'),
                        go.Scatter(x=dates1_2, y=df_all0_M_2['lim_sum'].values, mode='lines', name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
                        go.Scatter(x=dates1_2, y=points_2_0, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
                    ],
                    layout=go.Layout(
                        title= 'Динамика задолженности по клиентам с кредитным лимитом ',
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
            dbc.Navbar(
            [
                html.Div('Выберите начальную дату:', 
                    style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
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
                    style={'width': '15%', 'display': 'inline-block', }),
            ],dark=True, color='rgb(71, 71, 71)'
            ),

            html.Div([
                html.H6('Таблица по клиентам с кредитным лимитом'),
                dbc.Col(dash_table.DataTable(
                    id='datatable_clients_limit',
                    columns=[{"name": col_name_rus[i][0], "id": i,
                    #  "deletable": True, 
                     'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
                    {"name": col_name_rus[i][0], "id": i,
                    #  "deletable": True, 
                     'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
                     for i in    df_dog_2_1.columns],
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
                ), width=12)
            ], className='eleven columns'),
            dcc.Graph(
                id="all_x",
                figure=go.Figure(
                    data=[
                        go.Scatter(x=dates1_3, y=points_3, mode='lines', 
                        name= 'Динамическое сальдо долг', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
                        go.Scatter(x=dates1_3, y=points_3_0, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
                    ],
                    layout=go.Layout(
                        title= 'Общий уровень задолженности по клиентам с отсрочкой платежа без потолка лимита ',
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
            html.Div([
                html.H6('Таблица по клиентам с отсрочкой платежа'),
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
                ), width=12)
            ], className='eleven columns'),
            dcc.Graph(
                id="all_prepaid",
                figure=go.Figure(
                    data=[
                        go.Bar(x=dates1_1, y=points_1_c,  yaxis='y1',  width=500000000, name= 'Кредитный лимит из SAP', xaxis='x1', opacity=0.5),
                        go.Scatter(x=dates1_1, y=points_1, mode='lines',  name= 'Динамическое сальдо долг', yaxis='y2',#line_color='rgb(40,80,0)', 
                        line_shape='spline'),
                        
                        # go.Scatter(x=dates1_1, y=points_1_c, mode='bar', secondary_y=True,name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
                        go.Scatter(x=dates1_1, y=points_1_0, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, yaxis='y1',xaxis='x2')
                    ],
                    layout=go.Layout(
                        title= 'Динамика задолженности по предоплатным клиентам  ',
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
                        margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
                        legend={'x': 0, 'y': 1},
                        showlegend=True
                    )
                ), style={'width': '80%'},
                config={'displayModeBar': False}
            ),
            html.Div([
                html.H6('Таблица по предоплатным клиентам '),
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
            ], className='eleven columns'),


            

        ], 
        className='twelve columns', style={'fontSize': 12})
    return layout



@app.callback(
        [
        Output('datatable_clients_limit', 'data'),
        Output('datatable_clients_X', 'data'),
        Output('datatable_clients_prepaid', 'data'),
        ]
        ,
        Input('submit-val', 'n_clicks')
        ,
        State('risk_str_date', 'date'),
        State('risk_end_date', 'date'),
        background=True,
        # State('datatable_clients_limit', 'data'),  
        prevent_initial_call=True,
        running=[
        ( Output("submit-val", "disabled"), True, False),
        ]
)
def chose_period(n_c, s_d, e_d):
    df_dog_1,df_dog_2,df_dog_3=get_dates_for_table()
    df_dog_2_1=get_matrix_stat_1(df_dog_2, s_d=s_d, e_d= e_d)
    df_dog_3_1=get_matrix_stat_2(df_dog_3)
    df_dog_1_1=get_matrix_stat_1(df_dog_1)
    return [df_dog_2_1.to_dict('records'),df_dog_3_1.to_dict('records'),df_dog_1_1.to_dict('records'),]

    

        #     dcc.Graph(
        #         id="all",
        #         figure=go.Figure(
        #             data=[
        #                 go.Scatter(x=dates1, y=points, mode='lines', 
        #                 name= 'Динамическое сальдо долг', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
        #                 go.Scatter(x=dates, y=points3, mode='lines', name= 'Динамическое сальдо без лимита', line_color='rgb(138,36,50)', line_shape='spline', xaxis='x1'),
        #                 go.Scatter(x=dates, y=points4, mode='lines', name= 'Долг внелимитов', line_color='rgb(18,215,90)', line_shape='spline', xaxis='x1'),
        #                 go.Scatter(x=dates, y=points1, mode='lines', name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
        #                 go.Scatter(x=dates, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
        #             ],
        #             layout=go.Layout(
        #                 plot_bgcolor='white',
        #                 paper_bgcolor='white',
        #                 xaxis=dict(
        #                     showticklabels=False,
        #                     overlaying='x2',
        #                     showdividers=False),
        #                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
        #                 legend={'x': 0, 'y': 1},
        #                 showlegend=True
        #             )
        #         ), style={'width': '80%'},
        #         config={'displayModeBar': False}
        #     ),

            
        #     html.Div([
        #         html.H6('История лимитов:'),
        #         dbc.Col(dash_table.DataTable(
        #             id='datatable',
        #             columns=[{"name": col_name_rus[i][0], "id": i,
        #              "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
        #             {"name": col_name_rus[i][0], "id": i,
        #              "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
        #              for i in    df_all0_M.columns],
        #             data=(df_all0_M).to_dict('records'),
        #             # editable=True,
        #             filter_action="native",
        #             sort_action="native",
        #             sort_mode="multi",
        #             # column_selectable="single",
        #             # row_selectable="multi",
        #             # row_deletable=True,
        #             selected_columns=[],
        #             selected_rows=[],
        #             page_action="native",
        #             page_current= 0,
        #             page_size= 10, 
        #             style_cell = {'textAlign': 'left'},
        #             style_as_list_view=True, 
        #             # style_data_conditional=[
        #             #     {'if': {'column_id': 'Лимит в SAP'},
        #             #     'width': '35px'},
        #             # ]
        #         ), width=12)
        #     ], className='eleven columns'),
        #     dbc.Row(
        #         html.H5('Детализация по филиалам')
        #     ),
        #     dbc.Navbar(
        #     [
        #         html.Div('Выберите клиента:', 
        #             style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
        #         ),
        #         html.Div(
        #             dcc.Dropdown(
        #                 id='fil', 
        #                 options=[
        #                             {
        #                                 'label':klient , 
        #                                 'value': klient} for klient in filials.values
        #                         ], 
        #                                 value='Владивостокский филиал'
        #             ), 
        #             style={'width': '25%', 'display': 'inline-block'}
        #         )
        #     ],dark=True, color='rgb(71, 71, 71)'
        #     ),
        #     dcc.Graph(
        #         id="filial",
        #         figure=go.Figure(
        #             data=[
        #                 go.Scatter(x=dates1, 
        #                 y= df_filial0[df_filial0['filial']=='Центральный Аппарат']['dinamic_saldo'].values, mode='lines', name= "Центральный Аппарат", line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
        #                 # go.Scatter(x=dates, y=points3, mode='lines', name= 'Динамическое сальдо без лимита', line_color='rgb(138,36,50)', line_shape='spline', xaxis='x1'),
        #                 go.Scatter(x=dates, 
        #                 y=df_filial0[df_filial0['filial']=='Центральный Аппарат']['lim_sum'].values, mode='lines', name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
        #                 go.Scatter(x=dates, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
        #             ],
        #             layout=go.Layout(
        #                 plot_bgcolor='white',
        #                 paper_bgcolor='white',
        #                 xaxis=dict(
        #                     showticklabels=False,
        #                     overlaying='x2',
        #                     showdividers=False),
        #                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
        #                 legend={'x': 0, 'y': 1},
        #                 showlegend=True
        #             )
        #         ), style={'width': '80%'},
        #         config={'displayModeBar': False}
        #     ),
        #     html.Div([
        #         html.H6('Рейтинг филиалов:'),
        #         dbc.Col(
        #             dash_table.DataTable(
        #                 id='datatable2',
        #                  columns=[{"name": col_name_rus[i][0], "id": i,
        #                 "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
        #                 {"name": col_name_rus[i][0], "id": i,
        #                 "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
        #                 for i in    df_filial.columns],
        #                 data=df_filial.to_dict('records'),
        #                 # editable=True,
        #                 filter_action="native",
        #                 sort_action="native",
        #                 sort_mode="multi",
        #                 # column_selectable="single",
        #                 # row_selectable="multi",
        #                 # row_deletable=True,
        #                 selected_columns=[],
        #                 selected_rows=[],
        #                 page_action="native",
        #                 page_current= 0,
        #                 page_size= 10,
        #                 style_as_list_view=True, 
        #                 style_table={#'height': 530, 
        #                     # 'width':800,
        #                     'overflowY': 'auto',
        #                     'lineHeight': '30px'},
        #                 style_data={
        #                     'whiteSpace': 'normal',
        #                     'height': 'auto',
        #                     'font_size': '12px',
        #                     'line-height': 0.9
        #                     # 'width': '100px',
        #                     # 'maxWidth': '100px',
        #                     # 'minWidth': '100px',
        #                 },
        #             #     style_header={
        #             #             'backgroundColor': 'rgb(138,36,50)',
        #             #             'color': 'white',
        #             #             'whiteSpace':'normal',
        #             #             'fontWeight': 'bold',
        #             #             'font_size': '16px'
        #             # },
        #                 style_cell={
        #                     'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'right'
        #                 },
        #             ), width=12
        #         )
        #     ], className='eleven columns'
        #     ),
        #     dbc.Row(
        #         html.H5('Детализация по клиентам')
        #     ),
        #      dbc.Navbar(
        #     [
        #         html.Div('Выберите клиента:', 
        #             style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
        #         ),
        #         html.Div(
        #             dcc.Dropdown(
        #                 id='klient', 
        #                 options=[
        #                             {
        #                                 'label':':'.join(str(x) for x in klient[::-1]) , 
        #                                 'value': klient[0]} for klient in clients.values
        #                         ], 
        #                                 value=1000134
        #             ), 
        #             style={'width': '25%', 'display': 'inline-block'}
        #         ),
        #     ],dark=True, color='rgb(71, 71, 71)'
        #     ),
        #     dcc.Graph(
        #         id="client",
        #         figure=go.Figure(
        #             data=[
        #                 go.Scatter(x=dates1, y= df_clients0[df_clients0['client']==1000292]['dinamic_saldo'].values, mode='lines', name= "1000134", line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
        #                 # go.Scatter(x=dates, y=points3, mode='lines', name= 'Динамическое сальдо без лимита', line_color='rgb(138,36,50)', line_shape='spline', xaxis='x1'),
        #                 go.Scatter(x=dates, y=df_clients0[df_clients0['client']==1000292]['lim_sum'].values, mode='lines', name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
        #                 go.Scatter(x=dates, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
        #             ],
        #             layout=go.Layout(
        #                 plot_bgcolor='white',
        #                 paper_bgcolor='white',
        #                 xaxis=dict(
        #                     showticklabels=False,
        #                     overlaying='x2',
        #                     showdividers=False),
        #                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
        #                 legend={'x': 0, 'y': 1},
        #                 showlegend=True
        #             )
        #         ), style={'width': '80%'},
        #         config={'displayModeBar': False}
        #     ),
        #     html.Div([
        #         html.H6('Рейтинг клиентов:'),
        #         dbc.Col(dash_table.DataTable(
        #             id='datatable',
        #             columns=[{"name": col_name_rus[i][0], "id": i,
        #              "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
        #             {"name": col_name_rus[i][0], "id": i,
        #              "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
        #              for i in    df_clients.columns],
        #             data=df_clients.to_dict('records'),
        #             # editable=True,
        #             filter_action="native",
        #             sort_action="native",
        #             sort_mode="multi",
        #             # column_selectable="single",
        #             # row_selectable="multi",
        #             # row_deletable=True,
        #             style_table={#'height': 530, 
        #                     # 'width':800,
        #                     'overflowY': 'auto',
        #                     'lineHeight': '30px'},
        #                 style_data={
        #                     'whiteSpace': 'normal',
        #                     'height': 'auto',
        #                     'font_size': '12px',
        #                     'line-height': 0.9
        #                     # 'width': '100px',
        #                     # 'maxWidth': '100px',
        #                     # 'minWidth': '100px',
        #                 },
        #             #     style_header={
        #             #             'backgroundColor': 'rgb(138,36,50)',
        #             #             'color': 'white',
        #             #             'whiteSpace':'normal',
        #             #             'fontWeight': 'bold',
        #             #             'font_size': '16px'
        #             # },
        #                 style_cell={
        #                     'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'right'
        #                 },
        #             selected_columns=[],
        #             selected_rows=[],
        #             page_action="native",
        #             page_current= 0,
        #             page_size= 10, 
        #             # style_cell = {'textAlign': 'left'},
        #             style_as_list_view=True, 
        #             # style_data_conditional=[
        #             #     {'if': {'column_id': 'Лимит в SAP'},
        #             #     'width': '35px'},
        #             # ]
        #         ), width=12)
        #     ], className='eleven columns'
        #     ),
        #     # dbc.Row(
        #     #     html.H5('Детализация по договорам')
        #     # ),
        #     # dbc.Navbar(
        #     # [
        #     #     html.Div('Выберите договор:',
        #     #         style={'width': '15%', 'margin-left': 15,'display': 'inline-block', 'color': 'white'}
        #     #     ),
        #     #     html.Div(
        #     #         dcc.Dropdown(
        #     #             id='dogovor', 
        #     #             options=[
        #     #                         {
        #     #                             'label':':'.join(str(x) for x in k) , 
        #     #                             'value': k[1]} for k in contracts.values]
        #     #         ), 
        #     #         style={'width': '25%', 'display': 'inline-block'}
        #     #     )
        #     # # ], dark=True, sticky="top", color='rgb(71, 71, 71)'),
        #     # ], dark=True, color='rgb(71, 71, 71)'
        #     # ),
        # #     dcc.Graph(
        # #         id="client",
        # #         figure=go.Figure(
        # #             data=[
        # #                 go.Scatter(x=dates1, y= df[df['id_rcm']==1132]['dinamic_saldo'].values, mode='lines', name= "1132", line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
        # #                 # go.Scatter(x=dates, y=points3, mode='lines', name= 'Динамическое сальдо без лимита', line_color='rgb(138,36,50)', line_shape='spline', xaxis='x1'),
        # #                 go.Scatter(x=dates, y=df[df['id_rcm']==1132]['lim_sum'].values, mode='lines', name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
        # #                 go.Scatter(x=dates, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
        # #             ],
        # #             layout=go.Layout(
        # #                 plot_bgcolor='white',
        # #                 paper_bgcolor='white',
        # #                 xaxis=dict(
        # #                     showticklabels=False,
        # #                     overlaying='x2',
        # #                     showdividers=False),
        # #                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
        # #                 legend={'x': 0, 'y': 1},
        # #                 showlegend=True
        # #             )
        # #         ), style={'width': '80%'},
        # #         config={'displayModeBar': False}
        # #     ),
        # #     html.Div([
        # #         html.H6('Рейтинг клиентов:'),
        # #         dbc.Col(dash_table.DataTable(
        # #             id='datatable',
        # #             columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in df_dog.columns],
        # #             data=df_dog.to_dict('records'),
        # #             # editable=True,
        # #             filter_action="native",
        # #             sort_action="native",
        # #             sort_mode="multi",
        # #             # column_selectable="single",
        # #             # row_selectable="multi",
        # #             # row_deletable=True,
        # #             selected_columns=[],
        # #             selected_rows=[],
        # #             page_action="native",
        # #             page_current= 0,
        # #             page_size= 10, 
        # #             style_cell = {'textAlign': 'left'},
        # #             style_as_list_view=True, 
        # #             # style_data_conditional=[
        # #             #     {'if': {'column_id': 'Лимит в SAP'},
        # #             #     'width': '35px'},
        # #             # ]
        # #         ), width=12)
        # #     ], className='eleven columns'
        # #     ),

           
            
                        
        # # #    ,


# @app.callback(
#         [Output('dogovor', 'options'),
#         Output('dogovor', 'value')],
#     # Output(component_id='dogovor', component_property='options'),
#     [
#         Input(component_id='klient', component_property='value')
#     ]
# )
# def dogovor(klient):
#     # query3="""
#     # SELECT DISTINCT(SAPABAP1.BSEG.ZUONR) as ZUONR FROM SAPABAP1.BSEG
#     # where SAPABAP1.BSEG.KUNNR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
#     # """ % klient
#     # con = get_connection()
#     # df6=pd.read_sql(query3, con)
#     df = get_limit_oper_zuonr_data(klient)
#     if df.empty:
#         return None
#     else:
#         return [{'label': i, 'value': i} for i in df['zuonr']], df['zuonr'][0]


# @app.callback(
#     Output(component_id='graph', component_property='children'),
#     [
#         Input(component_id='klient', component_property='value'),
#         Input(component_id='dogovor', component_property='value')
#     ]
# )
# def content(klient, dogovor):
#     # query2="""
#     # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM, 
#     #     TO_TIMESTAMP(CONCAT(SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM), 'YYYYMMDDHHMISS') as timestamp, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
#     # LEFT JOIN SAPABAP1.BKPF
#     # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
#     # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
#     # """ % (klient, dogovor)
    
#     # con = get_connection()
#     cols = ['ind','zuonr','shkzg','hkont','kunnr','h_blart','dmbtr','cpudt','cputm','timestamp', 'stblg']
#     df = get_limit_oper_client_zuonr_data(klient, dogovor)[cols]
#     if df.empty:
#         return None
#     else: 
#         # df=pd.read_sql(query2, con)
#         # con.close()

#         # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
#         # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
#         # xl = pd.ExcelFile(file)
#         # dflim = xl.parse('BSEG')
#         dflim = get_limit1()

#         df4=df.sort_values(['timestamp'], ascending=True)
#         lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
#         df4.insert(11, 'limit', 99999999)
#         for i, item in enumerate (df4['ind']):
#             try:
#                 df4.iloc[i,11]=int(lim)
#             except:
#                 df4.iloc[i,11]=0
#         df5=df4
#         df5.insert(12, 'summ2', 999999999)
#         for i, item in enumerate (df5['ind']):
#             if df5.iloc[0,2]=='S':
#                 df5.iloc[0,12]=df5.iloc[0,6]
#             else:
#                 df5.iloc[0,12]=df5.iloc[0,6]*(-1)
#             try:
#                 if df5.iloc[i+1,2]=='S':
#                     df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])
#                 else:
#                     df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])*(-1)
#             except:
#                 if df5.iloc[i,2]=='S':
#                     df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])
#                 else:
#                     df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])*(-1)
#         df5.insert(13, 'zero', 9)
#         for i, item in enumerate (df5['ind']):
#             try:
#                 df5.iloc[i,13]=int('0')
#             except:
#                 df5.iloc[i,13]=0
#         dates=df5['cpudt']
#         dates1=df5['cputm']
#         points=df5['summ2']
#         points1=df5['limit']
#         dates2=df5['timestamp']
#         points2=df5['zero']

#         # print('Excel')
#         # with pd.ExcelWriter('/home/turganovai@domain.local/git/uva001_front/test.xlsx') as wr:
#         #     df.to_excel(wr, sheet_name = 'df', encoding = 'utf-8', index = False)
#         #     df5.to_excel(wr, sheet_name = 'df5', encoding = 'utf-8', index = False) 


#         return dcc.Graph(figure=go.Figure(
#             data=[go.Scatter(x=[dates2, dates, dates1], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
#                 go.Scatter(x=[dates2, dates, dates1], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
#                 go.Scatter(x=dates2, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
#             layout=go.Layout(
#                 plot_bgcolor='white',
#                 paper_bgcolor='white',
#                 xaxis=dict(
#                     showticklabels=False,
#                     overlaying='x2',
#                     showdividers=False),
#                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
#                 legend={'x': 0, 'y': 1},
#                 showlegend=True
#             )
#         ), config={'displayModeBar': False})

# @app.callback(
#     Output(component_id='graph2', component_property='children'),
#     [
#         Input(component_id='klient', component_property='value'),
#         Input(component_id='dogovor', component_property='value')
#     ]
# )
# def content2(klient, dogovor):
#     # query4="""
#     # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM, TO_TIMESTAMP(CONCAT(SAPABAP1.BKPF.CPUDT, SAPABAP1.BKPF.CPUTM), 'YYYYMMDDHHMISS') as timestamp, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
#     # LEFT JOIN SAPABAP1.BKPF
#     # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
#     # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
#     # """ % (klient, dogovor)

#     # con = get_connection()
#     print('graph2')
#     cols = ['ind','zuonr','shkzg','hkont','kunnr','h_blart','dmbtr','cpudt','cputm','timestamp', 'stblg']
#     df = get_limit_oper_client_zuonr_data(klient, dogovor)[cols]

#     if df.empty:
#         return None
#     else: 
#         # df=pd.read_sql(query4, con)
#         # con.close()

#         # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
#         # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
#         # xl = pd.ExcelFile(file)
#         # dflim = xl.parse('BSEG')
#         dflim = get_limit1()

#         df4=df.sort_values(['cpudt', 'cputm'], ascending=[True, True])
#         df4.insert(11, 'limit', 99999999)
#         lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
#         for i, item in enumerate (df4['ind']):
#             try:
#                 df4.iloc[i,11]=int(lim)
#             except:
#                 df4.iloc[i,11]=0
#         df5=df4
#         df5.insert(12, 'summ2', 999999999)
#         for i, item in enumerate (df5['ind']):
#             if df5.iloc[0,2]=='S':
#                 df5.iloc[0,12]=df5.iloc[0,6]
#             else:
#                 df5.iloc[0,12]=df5.iloc[0,6]*(-1)
#             try:
#                 if df5.iloc[i+1,2]=='S':
#                     df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])
#                 else:
#                     df5.iloc[i+1,12]=int(df5.iloc[i,12])+int(df5.iloc[i+1,6])*(-1)
#             except:
#                 if df5.iloc[i,2]=='S':
#                     df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])
#                 else:
#                     df5.iloc[i,12]=df5.iloc[i-1,12]+int(df5.iloc[i,6])*(-1)
#         df5.insert(13, 'zero', 9)
#         for i, item in enumerate (df5['ind']):
#             try:
#                 df5.iloc[i,13]=int('0')
#             except:
#                 df5.iloc[i,13]=0
#         dates=df5['cpudt']
#         dates2=df5['cputm']
#         points=df5['summ2']
#         points1=df5['limit']
#         dates4=df5['timestamp']
#         points2=df5['zero']
#         return dcc.Graph(figure=go.Figure(
#             data=[go.Scatter(x=[dates4, dates, dates2], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_shape='spline', line_color='grey', xaxis='x1'),
#                 go.Scatter(x=[dates4, dates, dates2], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
#                 go.Scatter(x=dates4, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
#             layout=go.Layout(
#                 plot_bgcolor='white',
#                 paper_bgcolor='white',
#                 xaxis=dict(
#                     showticklabels=False,
#                     overlaying='x2',
#                     showdividers=False
#                 ),
#                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
#                 legend={'x': 0, 'y': 1},
#                 showlegend=True
#             )
#         ), config={'displayModeBar': False})

# @app.callback(
#     Output(component_id='graph3', component_property='children'),
#     [
#         Input(component_id='klient', component_property='value'),
#         Input(component_id='dogovor', component_property='value')
#     ]
# )
# def content3(klient, dogovor):
#     # query5="""
#     # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BUDAT, 'YYYYMMDD') as BUDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
#     # LEFT JOIN SAPABAP1.BKPF
#     # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
#     # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
#     # """ % (klient, dogovor)

#     # con = get_connection()
#     print('graph3')
#     cols = ['ind','zuonr','shkzg','hkont','kunnr','h_blart','dmbtr','budat','belnr', 'stblg']
#     df = get_limit_oper_client_zuonr_data(klient, dogovor)[cols]
#     if df.empty:
#         return None
#     else: 
#         # df=pd.read_sql(query5, con)
#         # con.close()

#         # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
#         # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
#         # xl = pd.ExcelFile(file)
#         # dflim = xl.parse('BSEG')
#         dflim = get_limit1()

#         df4=df.sort_values(['budat', 'belnr'], ascending=[True, True])
#         lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
#         df4.insert(10, 'limit', 99999999)
#         for i, item in enumerate (df4['ind']):
#             try:
#                 df4.iloc[i,10]=int(lim)
#             except:
#                 df4.iloc[i,10]=0
#         df5=df4
#         df5.insert(11, 'summ2', 999999999)
#         for i, item in enumerate (df5['ind']):
#             if df5.iloc[0,2]=='S':
#                 df5.iloc[0,11]=df5.iloc[0,6]
#             else:
#                 df5.iloc[0,11]=df5.iloc[0,6]*(-1)
#             try:
#                 if df5.iloc[i+1,2]=='S':
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
#                 else:
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
#             except:
#                 if df5.iloc[i,2]=='S':
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
#                 else:
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
#         df5.insert(12, 'zero', 9)
#         for i, item in enumerate (df5['ind']):
#             try:
#                 df5.iloc[i,12]=int('0')
#             except:
#                 df5.iloc[i,12]=0
#         dates=df5['belnr']
#         points=df5['summ2']
#         points1=df5['limit']
#         dates2=df5['budat']
#         points2=df5['zero']
#         return dcc.Graph(figure=go.Figure(
#             data=[go.Scatter(x=[dates2, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
#                 go.Scatter(x=[dates2, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
#                 go.Scatter(x=dates2, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
#             layout=go.Layout(
#                 plot_bgcolor='white',
#                 paper_bgcolor='white',
#                 xaxis=dict(
#                     showticklabels=False,
#                     overlaying='x2',
#                     showdividers=False),
#                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
#                 legend={'x': 0, 'y': 1},
#                 showlegend=True
#             )
#         ), config={'displayModeBar': False})

# @app.callback(
#     Output(component_id='graph4', component_property='children'),
#     [
#         Input(component_id='klient', component_property='value'),
#         Input(component_id='dogovor', component_property='value')
#     ]
# )
# def content4(klient, dogovor):
#     # query6="""
#     # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BUDAT, 'YYYYMMDD') as BUDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
#     # LEFT JOIN SAPABAP1.BKPF
#     # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
#     # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
#     # """ % (klient, dogovor)

#     # con = get_connection()
#     cols = ['ind','zuonr','shkzg','hkont','kunnr','h_blart','dmbtr','budat','belnr', 'stblg']
#     df = get_limit_oper_client_zuonr_data(klient, dogovor)[cols]
#     # df=pd.read_sql(query6, con)
#     # con.close()

#     # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
#     # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
#     # xl = pd.ExcelFile(file)
#     # dflim = xl.parse('BSEG')
#     if df.empty:
#         return None
#     else: 
#         dflim = get_limit1()
#         print('graph4')
#         df4=df.sort_values(['budat', 'belnr'], ascending=[True, True])
#         df4.insert(10, 'limit', 99999999)
#         lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
#         for i, item in enumerate (df4['ind']):
#             try:
#                 df4.iloc[i,10]=int(lim)
#             except:
#                 df4.iloc[i,10]=0
#         df5=df4
#         df5.insert(11, 'summ2', 999999999)
#         for i, item in enumerate (df5['ind']):
#             if df5.iloc[0,2]=='S':
#                 df5.iloc[0,11]=df5.iloc[0,6]
#             else:
#                 df5.iloc[0,11]=df5.iloc[0,6]*(-1)
#             try:
#                 if df5.iloc[i+1,2]=='S':
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
#                 else:
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
#             except:
#                 if df5.iloc[i,2]=='S':
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
#                 else:
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
#         df5.insert(12, 'zero', 9)
#         for i, item in enumerate (df5['ind']):
#             try:
#                 df5.iloc[i,12]=int('0')
#             except:
#                 df5.iloc[i,12]=0
#         dates=df5['belnr']
#         points=df5['summ2']
#         points1=df5['limit']
#         dates4=df5['budat']
#         points2=df5['zero']
#         return dcc.Graph(figure=go.Figure(
#             data=[go.Scatter(x=[dates4, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_shape='spline', line_color='grey', xaxis='x1'),
#                 go.Scatter(x=[dates4, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
#                 go.Scatter(x=dates4, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
#             layout=go.Layout(
#                 plot_bgcolor='white',
#                 paper_bgcolor='white',
#                 xaxis=dict(
#                     showticklabels=False,
#                     overlaying='x2',
#                     showdividers=False
#                 ),
#                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
#                 legend={'x': 0, 'y': 1},
#                 showlegend=True
#             )
#         ), config={'displayModeBar': False})

# @app.callback(
#     Output(component_id='graph5', component_property='children'),
#     [
#         Input(component_id='klient', component_property='value'),
#         Input(component_id='dogovor', component_property='value')
#     ]
# )
# def content5(klient, dogovor):
#     # query7="""
#     # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BLDAT, 'YYYYMMDD') as BLDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
#     # LEFT JOIN SAPABAP1.BKPF
#     # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
#     # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and STBLG<'1' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
#     # """ % (klient, dogovor)
#     print('graph5')
#     # con =get_connection()
#     cols = ['ind','zuonr','shkzg','hkont','kunnr','h_blart','dmbtr','bldat','belnr', 'stblg']
#     df=get_limit_oper_client_zuonr_data(klient, dogovor)[cols]
#     # print(df.head(3))
#     # df=pd.read_sql(query7, con)
#     # con.close()

#     # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
#     # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
#     # xl = pd.ExcelFile(file)
#     # dflim = xl.parse('BSEG')
#     # print(dflim.head(3))
#     dflim = get_limit1()
#     if df.empty:
#         return None
#     else:     
#         df4=df.sort_values(['bldat', 'belnr'], ascending=[True, True])
#         lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
#         df4.insert(10, 'limit', 99999999)
#         for i, item in enumerate (df4['ind']):
#             try:
#                 df4.iloc[i,10]=int(lim)
#             except:
#                 df4.iloc[i,10]=0
#         df5=df4
#         df5.insert(11, 'summ2', 999999999)
#         for i, item in enumerate (df5['ind']):
#             if df5.iloc[0,2]=='S':
#                 df5.iloc[0,11]=df5.iloc[0,6]
#             else:
#                 df5.iloc[0,11]=df5.iloc[0,6]*(-1)
#             try:
#                 if df5.iloc[i+1,2]=='S':
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
#                 else:
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
#             except:
#                 if df5.iloc[i,2]=='S':
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
#                 else:
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
#         df5.insert(12, 'zero', 9)
#         for i, item in enumerate (df5['ind']):
#             try:
#                 df5.iloc[i,12]=int('0')
#             except:
#                 df5.iloc[i,12]=0
#         dates=df5['belnr']
#         points=df5['summ2']
#         points1=df5['limit']
#         dates2=df5['bldat']
#         points2=df5['zero']
#         return dcc.Graph(figure=go.Figure(
#             data=[go.Scatter(x=[dates2, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_color='rgb(40,80,0)', line_shape='spline', xaxis='x1'),
#                 go.Scatter(x=[dates2, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
#                 go.Scatter(x=dates2, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
#             layout=go.Layout(
#                 plot_bgcolor='white',
#                 paper_bgcolor='white',
#                 xaxis=dict(
#                     showticklabels=False,
#                     overlaying='x2',
#                     showdividers=False),
#                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
#                 legend={'x': 0, 'y': 1},
#                 showlegend=True,
#                 font=dict(
#                     size=12
#                 )
#             )
#         ), config={'displayModeBar': False})
    

# @app.callback(
#     Output(component_id='graph6', component_property='children'),
#     [
#         Input(component_id='klient', component_property='value'),
#         Input(component_id='dogovor', component_property='value')
#     ]
# )
# def content6(klient, dogovor):
#     # query8="""
#     # SELECT CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR) as IND, ZUONR, SHKZG, HKONT, KUNNR, H_BLART, DMBTR, TO_TIMESTAMP(SAPABAP1.BKPF.BLDAT, 'YYYYMMDD') as BLDAT, SAPABAP1.BSEG.BELNR, SAPABAP1.BKPF.STBLG FROM SAPABAP1.BSEG
#     # LEFT JOIN SAPABAP1.BKPF
#     # ON CONCAT(SAPABAP1.BSEG.BELNR, SAPABAP1.BSEG.GJAHR)=CONCAT(SAPABAP1.BKPF.BELNR, SAPABAP1.BKPF.GJAHR)
#     # where SAPABAP1.BSEG.KUNNR='%s' and ZUONR='%s' and H_BLART not in ('DC', 'DN') and HKONT in ('6201010100', '6202010100')
#     # """ % (klient, dogovor)

#     # con = get_connection()
#     print('graph6')
#     cols = ['ind','zuonr','shkzg','hkont','kunnr','h_blart','dmbtr','bldat','belnr', 'stblg']
#     df = get_limit_oper_client_zuonr_data(klient, dogovor)[cols]
#     # df=pd.read_sql(query8, con)
#     # con.close()
#     if df.empty:
#         return None
#     else: 
#         df4=df.sort_values(['bldat', 'belnr'], ascending=[True, True])
#         df4.insert(10, 'limit', 99999999)

#         # # file = os.getcwd()+'/uva001_front/Limit1.xlsx'
#         # file = '/home/turganovai@domain.local/git/uva001_front/Limit1.xlsx'
#         # xl = pd.ExcelFile(file)
#         # dflim = xl.parse('BSEG')
#         dflim = get_limit1()

#         lim=dflim[dflim['ZUONR']==dogovor]['LIMIT'].max()
#         for i, item in enumerate (df4['ind']):
#             try:
#                 df4.iloc[i,10]=int(lim)
#             except:
#                 df4.iloc[i,10]=0
#         df5=df4
#         df5.insert(11, 'summ2', 999999999)
#         for i, item in enumerate (df5['ind']):
#             if df5.iloc[0,2]=='S':
#                 df5.iloc[0,11]=df5.iloc[0,6]
#             else:
#                 df5.iloc[0,11]=df5.iloc[0,6]*(-1)
#             try:
#                 if df5.iloc[i+1,2]=='S':
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])
#                 else:
#                     df5.iloc[i+1,11]=int(df5.iloc[i,11])+int(df5.iloc[i+1,6])*(-1)
#             except:
#                 if df5.iloc[i,2]=='S':
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])
#                 else:
#                     df5.iloc[i,11]=df5.iloc[i-1,11]+int(df5.iloc[i,6])*(-1)
#         df5.insert(12, 'zero', 9)
#         for i, item in enumerate (df5['ind']):
#             try:
#                 df5.iloc[i,12]=int('0')
#             except:
#                 df5.iloc[i,12]=0
#         dates=df5['belnr']
#         points=df5['summ2']
#         points1=df5['limit']
#         dates4=df5['bldat']
#         points2=df5['zero']
#         return dcc.Graph(figure=go.Figure(
#             data=[go.Scatter(x=[dates4, dates], y=points, mode='lines+markers', name= 'Дебиторская задолженность', line_shape='spline', line_color='grey', xaxis='x1'),
#                 go.Scatter(x=[dates4, dates], y=points1, mode='lines', name= 'Кредитный лимит', line_color='rgb(207,0,15)', xaxis='x1'),
#                 go.Scatter(x=dates4, y=points2, mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')],
#             layout=go.Layout(
#                 plot_bgcolor='white',
#                 paper_bgcolor='white',
#                 xaxis=dict(
#                     showticklabels=False,
#                     overlaying='x2',
#                     showdividers=False
#                 ),
#                 margin={'l': 30, 'b': 30, 't': 20, 'r': 0},
#                 legend={'x': 0, 'y': 1},
#                 showlegend=True
#             )
#         ), config={'displayModeBar': False})
# agg0={
    #     'dinamic_saldo_min': 'min',
    #     'dinamic_saldo_mean': 'mean', 
    #     'dinamic_saldo_std':'mean',
    #     'dinamic_saldo_mean_below_zero':'mean',
    #     'dept_over_lim_min_x':'min',
    #     'dept_over_lim_mean_x':'mean',
    #     'dept_over_lim_std_x':'mean',
    #     'days_over_limit_max_x':'max',
    #     'days_over_limit_mean_x':'mean',
    #     'days_over_limit_std_x':'std',
    #     'days_over_limit_count_days_over_x':'sum',
    #     'dinamic_saldo':'sum',
    #     'lim_sum':sum_nonlimit,
    #     'dept_over_lim':'sum',
    #     # 'days_over_limit',
    #     'debitor_min':'min',
    #     'debitor_mean':'mean',
    #     'debitor_std':'mean',
    #     'debitor_mean_below_zero':'mean',
    #     'dept_over_lim_min_y':'min',
    #     'dept_over_lim_mean_y':'mean',
    #     'dept_over_lim_std_y':'std',
    #     'days_over_limit_max_y':'max',
    #     'days_over_limit_mean_y':'mean',
    #     'days_over_limit_std_y':'mean',
    #     'days_over_limit_count_days_over_y':'sum'

    # }