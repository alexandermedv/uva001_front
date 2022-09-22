"""Выгрузка данных и вспомогательные функции"""
import os
import datetime as dt
import pandas as pd
from sqlalchemy import create_engine
#from app import engine_analysis, engine_cons

# from . import engine_cons

# engine_cons = create_engine("""postgresql://locadm:Temp001@msc199-
# sdb04.domain.local:8031/uva_cons""", max_identifier_length=128, encoding='utf-8')

# Выгрузка таблицы по рискам
def get_risk_table():
	schema='analysis'
	Name_table='risk_radar_base'
	login='svc_fs_uva'
	passwors='Temp001'
	ip_server='172.17.0.136:5432'
	chunksize=100000
	sql = '''
		SELECT *
		FROM '''+schema+'''.'''+Name_table
	con = create_engine('postgresql://'+login+':'+passwors+'@'+ip_server+'/uva_cons' , max_identifier_length=128, encoding='utf-8')
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2


# Выгрузка оборота и количества операций по счету 94* за выбранный период

# print(os.getcwd(), flush=True)

# def get_risk_csv():
# 	print(os.getcwd())


# def get_osv_detail_by_dates(start_date, end_date, debug = False):
#     """Выгрузка недостач деталей за выбранный период"""
#     sql = '''
#           SELECT "Название бизнес-сферы",
#                 dashboard.material."Группа материалов",
#                 "Наименование склада",
#                 round(sum("Сумма во внутренней валюте по дебе")) AS "Дебет", 
#                 round(sum("Сумма во внутренней валюте по кред")) AS "Кредит",
#                 round(sum("Сумма во внутренней валюте по дебе")) - round(sum("Сумма во внутренней валюте по кред")) AS "Изменение за период",
# 				count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
# 					 	ELSE null 
# 					END) AS "Количество_дебет",
#                 count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
# 					 	ELSE null 
# 					END) AS "Количество_кредит",
#                 count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
# 					 	ELSE null 
# 					END) - 
# 				count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
# 					 	ELSE null 
# 					END) AS "Изменение количества"
#             FROM dashboard.osv_94
#                 LEFT JOIN dashboard.material
#                     ON dashboard.osv_94."Материал" = '00000000'||dashboard.material."Код материала"
#             WHERE TO_DATE("Дата ввода", 'YYYYMMDD') BETWEEN %s AND %s
#             GROUP BY "Название бизнес-сферы",
#                      dashboard.material."Группа материалов",
#                      "Наименование склада"
#     ''' % (start_date, end_date)
#     print('1')
#     if debug:
#         print(sql)
#     # return pd.read_sql(sql, con=engine_cons, params={"dstart":start_date,"dfinish":end_date})
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Выгрузка куба данных операций по счету 94* за выбранный период
# def get_osv_data(start_date, end_date, debug = False):
#     """Выгрузка куба данных операций по счету 94* за выбранный период"""
#     sql = '''
#           SELECT 			dashboard.osv_94."Дата проводки",
# 				initial_date,
# 				dashboard.osv_94."Название бизнес-сферы",
#                 dashboard.material."Группа материалов",
#                 dashboard.osv_94."Наименование склада",
#                 round(sum("Сумма во внутренней валюте по дебе")) AS "Дебет", 
#                 round(sum("Сумма во внутренней валюте по кред")) AS "Кредит",
#                 round(sum("Сумма во внутренней валюте по дебе") - sum("Сумма во внутренней валюте по кред")) AS "Изменение за период",
# 				count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
# 					 	ELSE null 
# 					END) AS "Количество_дебет",
#                 count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
# 					 	ELSE null 
# 					END) AS "Количество_кредит",
#                 count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
# 					 	ELSE null 
# 					END) - 
# 				count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
# 					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
# 					 	ELSE null 
# 					END) AS "Изменение количества",
# 				a.cumsum_filial,
# 				b.cumsum_det_type,
# 				c.cumsum_sklad,
# 				d.cumsum,
# 				e.cumsum_filial_count,
# 				f.cumsum_det_type_count,
# 				g.cumsum_sklad_count,
# 				h.cumsum_count
#             FROM dashboard.osv_94
#                 LEFT JOIN dashboard.material
#                     ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
# 				LEFT JOIN (
# 					SELECT  "Дата проводки",
# 							"Название бизнес-сферы",
# 							sum(round(sum("Сумма во внутренней валюте по дебе") - 
# 		   					sum("Сумма во внутренней валюте по кред"))) 
# 		   					over (partition by "Название бизнес-сферы"
# 								  order by "Дата проводки" 
# 								  rows between unbounded preceding and current row) AS cumsum_filial
# 					FROM dashboard.osv_94
# 					GROUP BY "Дата проводки",
# 							 "Название бизнес-сферы"
# 				) a
# 					ON a."Дата проводки" = dashboard.osv_94."Дата проводки"
# 						AND a."Название бизнес-сферы" = dashboard.osv_94."Название бизнес-сферы"
# 				LEFT JOIN (
# 					SELECT "Дата проводки",
# 							dashboard.material."Группа материалов",
# 							sum(round(sum("Сумма во внутренней валюте по дебе") - 
# 		   					sum("Сумма во внутренней валюте по кред"))) 
# 		   					over (partition by "Группа материалов" 
# 								  order by "Дата проводки" 
# 								  rows between unbounded preceding and current row) AS cumsum_det_type
# 					FROM dashboard.osv_94
# 						LEFT JOIN dashboard.material
# 							ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
# 					GROUP BY "Дата проводки",
# 							 "Группа материалов"
# 				) b
# 					ON b."Дата проводки" = dashboard.osv_94."Дата проводки"
# 						AND b."Группа материалов" = dashboard.material."Группа материалов"
# 				LEFT JOIN (
# 					SELECT  "Дата проводки",
# 							"Наименование склада",
# 							sum(round(sum("Сумма во внутренней валюте по дебе") - 
# 		   					sum("Сумма во внутренней валюте по кред"))) 
# 		   					over (partition by "Наименование склада" 
# 								  order by "Дата проводки" 
# 								  rows between unbounded preceding and current row) AS cumsum_sklad
# 					FROM dashboard.osv_94
# 					GROUP BY "Дата проводки",
# 							 "Наименование склада"
# 				) c
# 					ON c."Дата проводки" = dashboard.osv_94."Дата проводки"
# 						AND c."Наименование склада" = dashboard.osv_94."Наименование склада"
# 				LEFT JOIN (
# 					SELECT  "Дата проводки",
# 							sum(round(sum("Сумма во внутренней валюте по дебе") - 
# 		   					sum("Сумма во внутренней валюте по кред"))) 
# 		   					over (order by "Дата проводки" rows between unbounded preceding and current row) AS cumsum
# 					FROM dashboard.osv_94
# 					GROUP BY "Дата проводки"
# 				) d
# 					ON d."Дата проводки" = dashboard.osv_94."Дата проводки"
# 				LEFT JOIN (
# 					SELECT  "Дата проводки",
# 							"Название бизнес-сферы",
# 							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
# 									WHEN "Сумма во внутренней валюте по кред" < 0 then 1
# 									ELSE null 
# 								END) - 
# 							count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
# 									WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
# 									ELSE null 
# 								END))
# 							over (partition by "Название бизнес-сферы" 
# 			 	 				  order by "Дата проводки" 
# 			  					  rows between unbounded preceding and current row) AS cumsum_filial_count
# 						FROM dashboard.osv_94
# 						GROUP BY "Дата проводки",
# 							 	 "Название бизнес-сферы"
# 				) e
# 					ON e."Дата проводки" = dashboard.osv_94."Дата проводки"
# 						AND e."Название бизнес-сферы" = dashboard.osv_94."Название бизнес-сферы"
# 					LEFT JOIN (
# 					SELECT  "Дата проводки",
# 							dashboard.material."Группа материалов",
# 							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
#                                     WHEN "Сумма во внутренней валюте по кред" < 0 then 1
#                                     ELSE null 
#                                 END) - 
#                             count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
#                                     WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
#                                     ELSE null 
#                                 END))
# 							over (partition by "Группа материалов" 
# 			 	 				  order by "Дата проводки" 
# 			  					  rows between unbounded preceding and current row) AS cumsum_det_type_count
# 						FROM dashboard.osv_94
# 							LEFT JOIN dashboard.material
# 								ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
# 						GROUP BY "Дата проводки",
# 							 	 "Группа материалов"
# 				) f
# 					ON f."Дата проводки" = dashboard.osv_94."Дата проводки"
# 						AND f."Группа материалов" = dashboard.material."Группа материалов"
# 				LEFT JOIN (
# 					SELECT  "Дата проводки",
# 							"Наименование склада",
# 							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
# 									WHEN "Сумма во внутренней валюте по кред" < 0 then 1
# 									ELSE null 
# 								END) - 
# 							count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
# 									WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
# 									ELSE null 
# 								END))
# 							over (partition by "Наименование склада" 
# 			 	 				  order by "Дата проводки" 
# 			  					  rows between unbounded preceding and current row) AS cumsum_sklad_count
# 						FROM dashboard.osv_94
# 						GROUP BY "Дата проводки",
# 							 	 "Наименование склада"
# 				) g
# 					ON g."Дата проводки" = dashboard.osv_94."Дата проводки"
# 						AND g."Наименование склада" = dashboard.osv_94."Наименование склада"
# 				LEFT JOIN (
# 					SELECT  "Дата проводки",
# 							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
# 									WHEN "Сумма во внутренней валюте по кред" < 0 then 1
# 									ELSE null 
# 								END) - 
# 							count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
# 									WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
# 									ELSE null 
# 								END))
# 							over (order by "Дата проводки" 
# 			  					  rows between unbounded preceding and current row) AS cumsum_count
# 						FROM dashboard.osv_94
# 						GROUP BY "Дата проводки"
# 				) h
# 					ON h."Дата проводки" = dashboard.osv_94."Дата проводки"
# 				LEFT JOIN (
# 					SELECT "Название бизнес-сферы",
# 							"Группа материалов",
# 							"Наименование склада",
# 							max("Дата проводки") AS initial_date
# 					FROM dashboard.osv_94
# 						LEFT JOIN dashboard.material
# 							ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
# 					WHERE TO_DATE("Дата проводки", 'YYYYMMDD') < '%s' 
# 					GROUP BY "Название бизнес-сферы",
# 							"Группа материалов",
# 							"Наименование склада"
# 					) i
# 				ON i."Название бизнес-сферы" = dashboard.osv_94."Название бизнес-сферы"
# 					AND i."Группа материалов" = dashboard.material."Группа материалов"
# 					AND i."Наименование склада" = dashboard.osv_94."Наименование склада"
#             WHERE TO_DATE(dashboard.osv_94."Дата проводки", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             GROUP BY dashboard.osv_94."Дата проводки",
# 					 dashboard.osv_94."Название бизнес-сферы",
#                      dashboard.material."Группа материалов",
#                      dashboard.osv_94."Наименование склада",
# 					 a.cumsum_filial,
# 					 b.cumsum_det_type,
# 					 c.cumsum_sklad,
# 					 d.cumsum,
# 					 e.cumsum_filial_count,
# 					 f.cumsum_det_type_count,
# 					 g.cumsum_sklad_count,
# 					 h.cumsum_count,
# 					 i.initial_date
#     ''' % (str(start_date)[:10], str(start_date)[:10], str(end_date)[:10])
#     if debug:
#         print(sql)
#     # return pd.read_sql(sql, con=engine_cons, params={"dstart":start_date,"dfinish":end_date})
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# # Выгрузка оборота и количества операций по счету 94* за выбранный период для вкладки 4
# def get_osv_detail_by_dates2(start_date, end_date, debug = False):
#     """Выгрузка недостач деталей за период для вкладки 4"""
#     sql = '''
#           select "Дата ввода", sum("Сумма во внутренней валюте по дебе") as "Обороты по дебету", 
#                 sum("Сумма во внутренней валюте по кред") as "Обороты по кредиту", 
#                     material."Группа материалов",
#                     "Название бизнес-сферы" as "Филиал", "Наименование склада" as "Склад",  
#                     sum(sign("Сумма во внутренней валюте по дебе")) as "Обороты по дебету, шт",
#                     sum(sign("Сумма во внутренней валюте по кред")) as "Обороты по кредиту, шт"
                    
#                     from dashboard.osv_94 
#                     	left join dashboard.material on material."Код материала" = osv_94."Материал"::int::varchar
#                            where "Дата ввода" between '{}' and '{}'
#                                 --and "Дата ввода" > '20180101'
#                                     group by "Дата ввода", "Название бизнес-сферы", "Наименование склада"
#                                         , material."Группа материалов"
#     '''.format(dt.datetime.strftime(start_date, '%Y%m%d'), dt.datetime.strftime(end_date, '%Y%m%d'))
#     if debug:
#         print(sql)

#     # return pd.read_sql(sql, con=engine_cons)
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Значения списка филиалов
# def get_branch_names(debug = False):
#     """Выгрузка списка филиалов"""
#     sql = '''
#         SELECT DISTINCT "Название бизнес-сферы"
#         FROM dashboard.osv_94
#         ORDER BY "Название бизнес-сферы" ASC
#     '''
#     if debug:
#         print(sql)

#     # return pd.read_sql(sql, con=engine_cons)
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# # Значения списка типов запчастей
# def get_detail_type_names(debug = False):
#     """Выгрузка типов деталей"""
#     sql = '''
#         SELECT DISTINCT "Группа материалов"
#         FROM dashboard.material
#         ORDER BY "Группа материалов" ASC
#     '''
#     if debug:
#         print(sql)

#     # return pd.read_sql(sql, con=engine_cons)
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# # Значения списка складов
# def get_warehouse_names(debug = False):
#     """Выгрузка списка складов"""
#     sql = '''
#         SELECT DISTINCT "Наименование склада", "Название бизнес-сферы"
#         FROM dashboard.osv_94
#         ORDER BY "Наименование склада" ASC
#     '''
#     if debug: print(sql)

#     # return pd.read_sql(sql, con=engine_cons)
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# # Максимальная дата в выгрузке
# def get_max_date():
#     """Максимальная дата в выгрузке"""
#     sql = '''
#     SELECT MAX(TO_DATE("Дата ввода", 'YYYYMMDD'))
#     FROM dashboard.osv_94
#     '''
#     # return engine_cons.execute(sql).fetchone()[0]
#     con = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
#     return con.execute(sql).fetchone()[0]
