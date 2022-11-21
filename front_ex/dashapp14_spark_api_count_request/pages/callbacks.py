""" Интерактивные элементы для отчета"""
import datetime as dt
import numpy as np
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_table
import dash
from ..pages import dash_app
from ..utils import spark_GetStateAccount 
import xml.etree.ElementTree as ET

@dash_app.callback(Output(component_id='period', component_property='children'),
                    Output(component_id="actual_time", component_property='children'),
                    Output(component_id='pie', component_property='figure'),
                    Output(component_id='bar', component_property='figure'),
                   [Input('button', 'n_clicks')])
def count_request_func(n_ckicks):
    xml = spark_GetStateAccount(method='GetStateAccount')
    root = ET.fromstring(xml)
    conn_dt = root.iter('ReportPeriod')
    for i in conn_dt:
        period_to = i.attrib.get("To")
        period_from = i.attrib.get("From")
    content_period = html.H5('Период действия тарифа: с {} по {}'.format(period_from, period_to))
    
    actual_dt = root.iter('ResultInfo')
    for i in actual_dt:
        act_dt = pd.to_datetime(i.attrib.get("DateTime"))
    content_actual = html.H5('Отчет актуален на: {}'.format(act_dt))

    calls = root.iter('Methods')
    df_calls = pd.DataFrame(columns=['limit_call' 'total_call', 'left_call',])
    for i in calls:
        df_calls = df_calls.append({'limit_call': int(i.attrib.get("LimitCall")), 
                                    'total_call': int(i.attrib.get("TotalCall")),
                                    'left_call': int(i.attrib.get("LeftCall"))},
                    ignore_index=True)
    fig = px.pie(names=['Использованные запросы', 'Оставшиеся запросы'],
                values=[df_calls['total_call'][0], df_calls['left_call'][0]],
                title='Лимит запросов',
                color_discrete_sequence=['#FBFF9B', '#A4FF63'], #['#A4FF63', '#FBFF9B'],
                hole=0.85) #, category_orders={"names":['Использованные запросы','Оставшиеся запросы']}
    fig.update_traces(textinfo='value+label', 
                    textposition="outside")
    fig.update_layout(showlegend=False,
                    plot_bgcolor= '#f8f8ff', 
                    paper_bgcolor= '#f8f8ff')
    fig.add_annotation(x=0.5, y=0.5, text='Лимит запросов: {:,}'.format(int(df_calls['limit_call'][0])), showarrow=False)

    methods = root.iter('Method')
    df_methods = pd.DataFrame(columns=['method_name', 'method_description', 'call_count'])
    for i in methods:
        df_methods = df_methods.append({'method_name': i.attrib.get("Name"), 
                                    'method_description': i.attrib.get("Description"), 
                                    'call_count': int(i.attrib.get("CallCount"))},
                        ignore_index=True)
    # fig2 = px.bar(df_methods, 
    #             y='method_name',
    #             x='call_count',
    #             orientation='h',
    #             hover_name='method_description',
    #             title='Использованные запросы')
    # fig2.update_traces(marker=dict(
    #                     color='rgba(50, 171, 96, 0.6)',
    #                     line=dict(
    #                         color='rgba(50, 171, 96, 1.0)',
    #                         width=1)
    #                 )
    #             )
    # fig2.update_xaxes(title="", showgrid=False)
    # fig2.update_yaxes(title="")
    # fig2.update_layout({'plot_bgcolor': '#f8f8ff', 'paper_bgcolor': '#f8f8ff'})
    layout2 = go.Layout(
        shapes=[dict(
            type='line',
            x0=0, y0=i,
            x1=df_methods['call_count'][i], y1=df_methods['method_description'][i],
            line=dict(color='rgba(50, 171, 96, 0.6)', width=1)
        ) for i in range(len(df_methods))],
        title = dict(text ='Количество запросов по методам', x=0.5, font=dict()),
        plot_bgcolor='#f8f8ff', 
        paper_bgcolor= '#f8f8ff',
        xaxis_range=[-1000,df_methods['call_count'].max()+5000]
    )
    data2 = go.Scatter(y=df_methods['method_description'],
                    x=df_methods['call_count'],
                    text=df_methods['call_count'],
                    textposition='middle right',
                    texttemplate='%{text:,}',
                    #textfont=dict(color='#E58606'),
                    mode='markers+text',
                    marker=dict(color='rgba(50, 171, 96, 1.0)'),
                    hovertext=df_methods['method_name'])
    fig2 = go.Figure(data2, layout2)
    fig2.update_xaxes(showgrid=False, visible=False)
    fig2.update_yaxes(showgrid=False)

    return content_period, content_actual, fig, fig2