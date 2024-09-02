""" Интерактивные элементы для отчетов по запчастям."""
import datetime as dt
import numpy as np
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import plotly.graph_objects as go
import pandas as pd
# import dash_table
from dash import dash_table
import dash
from ..pages import dash_app
from ..utils import get_open_ap_by_groups_182, get_open_ap_by_groups_365, get_open_ap_by_groups_366
from ..utils import get_incoming_ap, get_increase_ap, get_decrease_ap, get_outcoming_ap, get_high_ap_issues
from ..utils import get_manual_table1, get_manual_table2, get_manual_table3, get_actplans


# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
	[Input('dashboard2-date-picker-range', 'start_date'),
	Input('dashboard2-date-picker-range', 'end_date'),
	])

def render_content(start_date, end_date):
	"""Построение содержимого дашборда"""

	df1 = get_open_ap_by_groups_182(start_date, end_date)
	# df1 = get_monitoring().sort_values(by=s, ascending=True)
	kol = 0

	x1_data = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str).tolist()
	x1_text = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str)
	y1_data = df1['actname'][df1['issue_risk_level']=='Низкий'].apply(lambda x: x[:20]).tolist()
	
	x1_text_bold = []
	for item in x1_text:
		x1_text_bold.append('<b>' + item + '</b>')

	x2_data = df1['count'][df1['issue_risk_level']=='Средний'].astype(str).tolist()
	x2_text = df1['count'][df1['issue_risk_level']=='Средний'].astype(str)
	y2_data = df1['actname'][df1['issue_risk_level']=='Средний'].apply(lambda x: x[:20]).tolist()
	x2_text_bold = []
	for item in x2_text:
		x2_text_bold.append('<b>' + item + '</b>')

	x3_data = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str).tolist()
	x3_text = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str)
	y3_data = df1['actname'][df1['issue_risk_level']=='Высокий'].apply(lambda x: x[:20]).tolist()
	x3_text_bold = []
	for item in x3_text:
		x3_text_bold.append('<b>' + item + '</b>')

	sum1 = sum(map(int, x1_data)) + sum(map(int, x2_data)) + sum(map(int, x3_data))

	df1 = get_open_ap_by_groups_365(start_date, end_date)

	x4_data = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str).tolist()
	x4_text = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str)
	y4_data = df1['actname'][df1['issue_risk_level']=='Низкий'].apply(lambda x: x[:20]).tolist()
	x4_text_bold = []
	for item in x4_text:
		x4_text_bold.append('<b>' + item + '</b>')

	x5_data = df1['count'][df1['issue_risk_level']=='Средний'].astype(str).tolist()
	x5_text = df1['count'][df1['issue_risk_level']=='Средний'].astype(str)
	y5_data = df1['actname'][df1['issue_risk_level']=='Средний'].apply(lambda x: x[:20]).tolist()
	x5_text_bold = []
	for item in x5_text:
		x5_text_bold.append('<b>' + item + '</b>')

	x6_data = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str).tolist()
	x6_text = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str)
	y6_data = df1['actname'][df1['issue_risk_level']=='Высокий'].apply(lambda x: x[:20]).tolist()
	x6_text_bold = []
	for item in x6_text:
		x6_text_bold.append('<b>' + item + '</b>')

	sum2 = sum(map(int, x4_data)) + sum(map(int, x5_data)) + sum(map(int, x6_data))


	df1 = get_open_ap_by_groups_366(start_date, end_date)

	x7_data = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str).tolist()
	x7_text = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str)
	y7_data = df1['actname'][df1['issue_risk_level']=='Низкий'].apply(lambda x: x[:20]).tolist()
	x7_text_bold = []
	for item in x7_text:
		x7_text_bold.append('<b>' + item + '</b>')

	x8_data = df1['count'][df1['issue_risk_level']=='Средний'].astype(str).tolist()
	x8_text = df1['count'][df1['issue_risk_level']=='Средний'].astype(str)
	y8_data = df1['actname'][df1['issue_risk_level']=='Средний'].apply(lambda x: x[:20]).tolist()
	x8_text_bold = []
	for item in x8_text:
		x8_text_bold.append('<b>' + item + '</b>')

	x9_data = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str).tolist()
	x9_text = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str)
	y9_data = df1['actname'][df1['issue_risk_level']=='Высокий'].apply(lambda x: x[:20]).tolist()
	x9_text_bold = []
	for item in x9_text:
		x9_text_bold.append('<b>' + item + '</b>')

	sum3 = sum(map(int, x7_data)) + sum(map(int, x8_data)) + sum(map(int, x9_data))

	incoming_ap = get_incoming_ap(start_date)
	increase_ap = get_increase_ap(start_date, end_date)
	decrease_ap = get_decrease_ap(start_date, end_date)
	outcoming_ap = get_outcoming_ap(end_date)

	if not incoming_ap[incoming_ap['issue_risk_level'] == 'Высокий'].empty:
		y11 = incoming_ap[incoming_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]
		y11_bold = '<b>' + str(incoming_ap[incoming_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]) + '</b>'
	else:
		y11 = 0
		y11_bold = 0
	if not increase_ap[increase_ap['issue_risk_level'] == 'Высокий'].empty:
		y12 = increase_ap[increase_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]
		y12_bold = '<b>' + str(increase_ap[increase_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]) + '</b>'
	else:
		y12 = 0
		y12_bold = 0
	if not decrease_ap.empty:
		y13 = (-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]
		y13_bold = '<b>' + str((-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]) + '</b>'
	else:
		y13 = 0
		y13_bold = 0
	y14 = (-1)*outcoming_ap[outcoming_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]
	y14_bold = '<b>' + str(outcoming_ap[outcoming_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]) + '</b>'

	if not incoming_ap[incoming_ap['issue_risk_level'] == 'Средний'].empty:
		y21 = incoming_ap[incoming_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]
		y21_bold = '<b>' + str(incoming_ap[incoming_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]) + '</b>'
	else:
		y21 = 0
		y21_bold = 0
	if not increase_ap[increase_ap['issue_risk_level'] == 'Средний'].empty:
		y22 = increase_ap[increase_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]
		y22_bold = '<b>' + str(increase_ap[increase_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]) + '</b>'
	else:
		y22 = 0
		y22_bold = 0
	if not decrease_ap.empty:
		y23 = (-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]
		y23_bold = '<b>' + str((-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]) + '</b>'
	else:
		y23 = 0
		y23_bold = 0
	y24 = (-1)*outcoming_ap[outcoming_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]
	y24_bold = '<b>' + str(outcoming_ap[outcoming_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]) + '</b>'

	if not incoming_ap[incoming_ap['issue_risk_level'] == 'Низкий'].empty:
		y31 = incoming_ap[incoming_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]
		y31_bold = '<b>' + str(incoming_ap[incoming_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]) + '</b>'
	else:
		y31 = 0
		y31_bold = 0
	if not increase_ap[increase_ap['issue_risk_level'] == 'Низкий'].empty:
		y32 = increase_ap[increase_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]
		y32_bold = '<b>' + str(increase_ap[increase_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]) + '</b>'
	else:
		y32 = 0
		y32_bold = 0
	if not decrease_ap.empty:
		y33 = (-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]
		y33_bold = '<b>' + str((-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]) + '</b>'
	else:
		y33 = 0
		y33_bold = 0
	y34 = (-1)*outcoming_ap[outcoming_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]
	y34_bold = '<b>' + str(outcoming_ap[outcoming_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]) + '</b>'

	high_ap = get_high_ap_issues()

	df_actplans = get_actplans()
	print(df_actplans.columns)
	manual_table2 = get_manual_table2()
	manual_table3 = get_manual_table3()

	content = html.Div([
		html.Div([
			html.Div([
				html.Div([
					html.Br([]),
					html.H6('''Количество недостатков по аудитам и длительностям устранения, шт.''',
							style={'text-align':'center',
								'font-size': '16pt',
								'font-weight': 'bold'}),
					html.Br([]),
				], className="six columns"),

				html.Div([
					html.Br([]),
					html.H6('''Динамика выявленных недостатков по уровню значимости''',
							style={'text-align':'center',
								'font-size': '16pt',
								'font-weight': 'bold'}),
					html.Br([]),
				], className="six columns"),
			], className="row"),

			html.Div([
				html.Div([

					dcc.Graph(
						id="dashboard6-graph1",
						figure={
							"data": [
								go.Bar(
									x=x1_data,
									y=y1_data,
									text=x1_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Низкий <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(112,149,51)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
								go.Bar(
									x=x2_data,
									y=y2_data,
									text=x2_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Средний <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(250,216,89)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
								go.Bar(
									x=x3_data,
									y=y3_data,
									text=x3_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Высокий <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(138,36,50)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
							],
							"layout": go.Layout(
								barmode='stack',
								height=200,
								title_text=f'''До 6 месяцев – {sum1} недостатков ({round(sum1/(sum1+sum2+sum3)*100)}%)''',
								xaxis={'categoryorder':'total descending'},
								margin={
													"r": 50,
													"t": 50,
													"b": 20,
													"l": 150,
								},
								showlegend=False,
							),

						},
						config={"displayModeBar": False},
					),
					html.Br([]),
	
					dcc.Graph(
						id="dashboard6-graph2",
						figure={
							"data": [
								go.Bar(
									x=x4_data,
									y=y4_data,
									text=x4_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Низкий <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(112,149,51)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
								go.Bar(
									x=x5_data,
									y=y5_data,
									text=x5_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Средний <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(250,216,89)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
								go.Bar(
									x=x6_data,
									y=y6_data,
									text=x6_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Высокий <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(138,36,50)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
							],
							"layout": go.Layout(
								# autosize=True,
								height=200,
								barmode='stack',
								title_text=f'''от 6 месяцев до 1 года – {sum2} недостатков ({round(sum2/(sum1+sum2+sum3)*100)}%)''',
								xaxis={'categoryorder':'total descending'},
								margin={
													"r": 50,
													"t": 50,
													"b": 20,
													"l": 150,
								},
								showlegend=False,

							),

						},
						config={"displayModeBar": False},
					),
					html.Br([]),
	
					dcc.Graph(
						id="dashboard6-graph3",
						figure={
							"data": [
								go.Bar(
									x=x7_data,
									y=y7_data,
									text=x7_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Низкий <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(112,149,51)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
								go.Bar(
									x=x8_data,
									y=y8_data,
									text=x8_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Средний <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(250,216,89)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
								go.Bar(
									x=x9_data,
									y=y9_data,
									text=x9_text_bold,
									textangle=0,
									hoverinfo='skip',
									hovertemplate=
										"""Риск: Высокий <br>Количество недостатков: %{text}""",
									name='',
									orientation='h',
									textposition='auto',
									marker={
										"color": 'rgb(138,36,50)',
										"line": {
											"color": "rgb(255, 255, 255)",
											"width": 2,
										},
									},
								),
							],
							"layout": go.Layout(
								height=200,
								barmode='stack',
								title_text=f'''более 1 года – {sum3} недостатков ({round(sum3/(sum1+sum2+sum3)*100)}%)''',
								margin={
													"r": 50,
													"t": 50,
													"b": 20,
													"l": 250,
								},
								showlegend=False,
							),

						},
						config={"displayModeBar": False},
					),
					html.Br([]),
				], className="six columns"),

				html.Div([

					dcc.Graph(
						id="dashboard6-graph4",
						figure={
							"data": [
								go.Waterfall(
									measure = ['relative', 'relative', 'relative', 'relative'],
									x=["Мониторинг <br>на начало периода", "Выявлено <br>за период", "Сняты с контроля <br>за период", "Мониторинг <br>на конец периода"],
									y=[y11, y12, y13, y14],
									# y=[49, 43, -23, -69],
									increasing = {"marker":{"color":"rgb(138,36,50)"}},
									decreasing = {"marker":{"color":"rgb(197, 116, 137)"}},
									# textposition = "inside",
									textposition = "auto",
									cliponaxis = False,
									connector={'visible': False},
									text=[y11_bold, y12_bold, y13_bold, y14_bold],
									hoverinfo='skip',
									hovertemplate=
										"""Количество недостатков: %{text}""",
									name='Недостатки',
									orientation='v',
								),
								
							],
							"layout": go.Layout(
								# autosize=True,
								height=200,
								barmode='stack',
								xaxis = {'tickangle': 0},
								title_text='Высокий уровень',
								margin={
													"r": 10,
													"t": 50,
													"b": 40,
													"l": 20,
								},

							),

						},
						config={"displayModeBar": False},
					),
					html.Br([]),

					dcc.Graph(
						id="dashboard6-graph5",
						figure={
							"data": [
								go.Waterfall(
									measure = ['relative', 'relative', 'relative', 'relative'],
									x=["Мониторинг <br>на начало периода", "Выявлено <br>за период", "Сняты с контроля <br>за период", "Мониторинг <br>на конец периода"],
									y=[y21, y22, y23, y24],
									# y=[49, 43, -23, -69],
									increasing = {"marker":{"color":"rgb(250,216,89)"}},
									decreasing = {"marker":{"color":"rgb(251, 231, 152)"}},
									# textposition = "inside",
									textposition = "auto",
									connector={'visible': False},
									text=[y21_bold, y22_bold, y23_bold, y24_bold],
									hoverinfo='skip',
									hovertemplate=
										"""Количество недостатков: %{text}""",
									name='Недостатки',
									orientation='v',
								),
								
							],
							"layout": go.Layout(
								# autosize=True,
								height=200,
								barmode='stack',
								title_text='Средний уровень',
								margin={
													"r": 10,
													"t": 50,
													"b": 40,
													"l": 20,
								},

							),

						},
						config={"displayModeBar": False},
					),
					html.Br([]),

					dcc.Graph(
						id="dashboard6-graph6",
						figure={
							"data": [
								go.Waterfall(
									measure = ['relative', 'relative', 'relative', 'relative'],
									x=["Мониторинг <br>на начало периода", "Выявлено <br>за период", "Сняты с контроля <br>за период", "Мониторинг <br>на конец периода"],
									y=[y31, y32, y33, y34],
									# y=[49, 43, -23, -69],
									increasing = {"marker":{"color":"rgb(112,149,51)"}},
									decreasing = {"marker":{"color":"rgb(169, 191, 133)"}},
									# textposition = "inside",
									textposition = "auto",
									connector={'visible': False},
									text=[y31_bold, y32_bold, y33_bold, y34_bold],
									hoverinfo='skip',
									hovertemplate=
										"""Количество недостатков: %{text}""",
									name='Недостатки',
									orientation='v',
								),
								
							],
							"layout": go.Layout(
								# autosize=True,
								height=300,
								barmode='stack',
								title_text='Низкий уровень',
								margin={
													"r": 10,
													"t": 50,
													"b": 40,
													"l": 20,
								},

							),

						},
						config={"displayModeBar": False},
					),
				], className="six columns"),
			], className="row"),

			html.Div([
				html.Div([
					html.H6(f'''Итого: {sum1+sum2+sum3} открытых недостатка''',
					style={'text-align':'center',
							'font-size': '16pt',
							'font-weight': 'bold'}),
				], className="five columns"),
				html.Div([
					html.H6('''Итого:''',
					style={'text-align':'center',
							'font-size': '16pt',
							'font-weight': 'bold'}),
				], className="one column"),
				html.Div([
					html.H6(y11+y21+y31,
					style={'text-align':'center',
							'font-size': '16pt',
							'font-weight': 'bold'}),
				], className="two columns"),
				html.Div([
					html.H6(y12+y22+y32,
					style={'text-align':'center',
							'font-size': '16pt',
							'font-weight': 'bold'}),
				], className="one column"),
				html.Div([
					html.H6(y13+y23+y33,
					style={'text-align':'center',
							'font-size': '16pt',
							'font-weight': 'bold'}),
				], className="two columns"),
				html.Div([
					html.H6(-y14-y24-y34,
					style={'text-align':'center',
							'font-size': '16pt',
							'font-weight': 'bold'}),
				], className="one column"),
			], className="row"),

			html.Div([
				html.Br([]),
				dbc.Row(),
			]),

			html.Div([
				# html.Br(),
				# html.H6('''Недостатки высокого уровня значимости''',
				#     style={'text-align':'center',
				#             'font-size': '16pt',
				#             'font-weight': 'bold'}),
				# html.Br([]),

				# Доработать эту таблицу, не удалять, она хорошая
				# dash_table.DataTable(
				#     # https://dash.plotly.com/datatable/width
				#     id='high_ap_issues_table',
				#     columns=[{"name": i, "id": i} for i in high_ap.columns],
				#     data=high_ap.to_dict('records'),
				#     page_size=20,
				#     style_table={'overflowX': 'auto'},
				#     style_cell={
				#         # all three widths are needed
				#         'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
				#         'overflow': 'hidden',
				#         'textOverflow': 'ellipsis',
				#         'textAlign': 'left',
				#     },
				#     export_format='xlsx',
				#     export_headers='display',
				#     merge_duplicate_headers=True,
				#     style_header={
				#         'backgroundColor': 'rgb(200, 200, 200)',
				#         'fontWeight': 'bold'
				#     },
				#     style_data_conditional=[
				#         {
				#             'if': {'row_index': 'odd'},
				#             'backgroundColor': 'rgb(230, 230, 230)',
				#         }
				#     ],
				#     style_data={
				#         'whiteSpace': 'normal',
				#         'height': 'auto',
				#     },
				# ),

				# Ручные таблицы
				html.Br(),
				dbc.Row(),
				html.H6('''Список недостатков''',
					style={'text-align':'center',
							'font-size': '16pt',
							'font-weight': 'bold'}),

				dash_table.DataTable(
					# https://dash.plotly.com/datatable/width
					id='manual_table1',
					columns=[{"name": i, "id": i} for i in df_actplans.columns],
					data=df_actplans.to_dict('records'),
					page_size=20,
					style_table={'overflowX': 'auto'},
					style_cell={
						# all three widths are needed
						'minWidth': '180px', 
						# 'width': '180px', 
						'maxWidth': '18000px',
						'overflow': 'hidden',
						'textOverflow': 'ellipsis',
						'textAlign': 'left',
					},
					style_cell_conditional=[
						{'if': {'column_id': 'Название аудита'},
						'width': '35%'},
						{'if': {'column_id': 'Мероприятие'},
						'width': '85%'},
						{'if': {'column_id': 'Описание недостатка (кратк)'},
						'width': '5%'},
						{'if': {'column_id': 'Описание недостатка (детальн)'},
						'width': '1580'},
						{'if': {'column_id': "Уровень критичности недостатка"},
						'width': '5%'},
						{'if': {'column_id': "Рекомендации"},
						'width': '40%'},
						{'if': {'column_id': "Комментарии"},
						'width': '10%'},
						{'if': {'column_id': "Отв аудитор"},
						'width': '5%'},
						{'if': {'column_id': "Координатор от бизнес-подразделения"},
						'width': '5%'},
						{'if': {'column_id': "Ожидаемая дата выполнения"},
						'width': '10%'},
						{'if': {'column_id': "Пересмотренная дата выполнения"},
						'width': '10%'},
						{'if': {'column_id': "ЗГД"},
						'width': '10%'},
						{'if': {'column_id': "История комментариев"},
						'width': '10%'},
					],
					export_format='xlsx',
					export_headers='display',
					merge_duplicate_headers=True,
					style_header={
						'backgroundColor': 'rgb(138,36,50)',
						'color': 'white',
						'whiteSpace':'normal',
						'fontWeight': 'bold'
					},
					style_data_conditional=[
						{
							'if': {'row_index': 'odd'},
							'backgroundColor': 'rgb(230, 230, 230)',
						}
					],
					style_data={
						'whiteSpace': 'normal',
						'height': 'auto',
					},
				),

				# html.Br(),
				# html.H6('''Недостатки со сроками завершения мероприятий, перенесенными на 2021 год''',
				#     style={'text-align':'center',
				#             'font-size': '16pt',
				#             'font-weight': 'bold'}),

				# dash_table.DataTable(
				#     # https://dash.plotly.com/datatable/width
				#     id='manual_table2',
				#     columns=[{"name": i, "id": i} for i in manual_table2.columns],
				#     data=manual_table2.to_dict('records'),
				#     page_size=20,
				#     style_table={'overflowX': 'auto'},
				#     style_cell={
				#         # all three widths are needed
				#         'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
				#         'overflow': 'hidden',
				#         'textOverflow': 'ellipsis',
				#         'textAlign': 'left',
				#     },
				#     style_cell_conditional=[
				#         {'if': {'column_id': "Область риска"},
				#         'width': '10%'},
				#         {'if': {'column_id': "Описание недостатка"},
				#         'width': '50%'},
				#         {'if': {'column_id': "Уровень значимости"},
				#         'width': '10%'},
				#         {'if': {'column_id': "Длительность устранения план/факт"},
				#         'width': '20%'},
				#     ],
				#     export_format='xlsx',
				#     export_headers='display',
				#     merge_duplicate_headers=True,
				#     style_header={
				#         'backgroundColor': 'rgb(138,36,50)',
				#         'color': 'white',
				#         'whiteSpace':'normal',
				#         'fontWeight': 'bold'
				#     },
				#     style_data_conditional=[
				#         {
				#             'if': {'row_index': 'odd'},
				#             'backgroundColor': 'rgb(230, 230, 230)',
				#         }
				#     ],
				#     style_data={
				#         'whiteSpace': 'normal',
				#         'height': 'auto',
				#     },
				# ),

				# html.Br(),
				# html.H6('''Недостатки с длительным плановым сроком завершения мероприятий''',
				#     style={'text-align':'center',
				#             'font-size': '16pt',
				#             'font-weight': 'bold'}),

				# dash_table.DataTable(
				#     # https://dash.plotly.com/datatable/width
				#     id='manual_table3',
				#     columns=[{"name": i, "id": i} for i in manual_table3.columns],
				#     data=manual_table3.to_dict('records'),
				#     page_size=20,
				#     style_table={'overflowX': 'auto'},
				#     style_cell={
				#         # all three widths are needed
				#         'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
				#         'overflow': 'hidden',
				#         'textOverflow': 'ellipsis',
				#         'textAlign': 'left',
				#     },
				#     export_format='xlsx',
				#     export_headers='display',
				#     merge_duplicate_headers=True,
				#     style_header={
				#         'backgroundColor': 'rgb(138,36,50)',
				#         'color': 'white',
				#         'whiteSpace':'normal',
				#         'fontWeight': 'bold'
				#     },
				#     style_data_conditional=[
				#         {
				#             'if': {'row_index': 'odd'},
				#             'backgroundColor': 'rgb(230, 230, 230)',
				#         }
				#     ],
				#     style_cell_conditional=[
				#         {'if': {'column_id': "Область риска"},
				#         'width': '10%'},
				#         {'if': {'column_id': "Описание недостатка"},
				#         'width': '30%'},
				#         {'if': {'column_id': "Уровень значимости"},
				#         'width': '10%'},
				#         {'if': {'column_id': "Длительность устранения план/факт"},
				#         'width': '10%'},
				#         {'if': {'column_id': "Статус"},
				#         'width': '40%'},
				#     ],
				#     style_data={
				#         'whiteSpace': 'normal',
				#         'height': 'auto',
				#     },
				# ),

			], className="row"),
		], className="row"),
	])

	return content