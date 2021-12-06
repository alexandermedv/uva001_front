"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
from pandas.io import sql
import front_ex.config as config
from sqlalchemy import create_engine

# Список железных дорог
def get_raiways():
    sql = '''
        select railway_id, railway_name from dashboard.tm_railways
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'])
    df = pd.read_sql(sql, con=con, max_identifier_length=128, encoding='utf-8')
    con.close()
    
    return df

def get_trans_empty_all():
    sql = '''
        select * from dashboard.dash_transport_empty
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'])
    df = pd.read_sql(sql, con=con, max_identifier_length=128, encoding='utf-8')
    con.close()

    return df

def get_trans_empty_by_railway_delay():
    sql = '''
        select "Дорога назначения", "Дор. назн.", "Кол-во вагонорейсов с просрочкой", "Всего вагонорейсов" from (
            select "Дорога назначения", max(ra.file) as "Дор. назн.",
                sum(case when t."Превышение даты истечение срока д" = 'Не удовлетворяет' then "Кол-во вагонорейсов" else 0 end) 
                    as "Кол-во вагонорейсов с просрочкой",
                sum("Кол-во вагонорейсов") as "Всего вагонорейсов"
		            from dashboard.dash_transport_empty t 
			            left join sap_s4.rails_mapping ra
				            on t."Дорога назначения" = ra."db"
                             where (lower("Плательщик") like '%пгк%' 
						        or lower("Грузоотправитель") like '%пгк' 
						        or lower("Получатель") like '%пгк')
                             group by t."Дорога назначения"
                                order by sum(case when t."Превышение даты истечение срока д" = 'Не удовлетворяет' then "Кол-во вагонорейсов" else 0 end) 
        ) t
    ''' 
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_railway_penalty():
    sql = '''
        select "Дорога назначения", max(ra.file) as "Дор. назн.", sum("Оценка пени") as "Оценка пени"
	        from dashboard.dash_transport_empty t 
            	left join sap_s4.rails_mapping ra
				    on t."Дорога назначения" = ra."db"
                    where t."Превышение даты истечение срока д" = 'Не удовлетворяет'
                        and (lower("Плательщик") like '%пгк%' 
						        or lower("Грузоотправитель") like '%пгк' 
						        or lower("Получатель") like '%пгк')
                            group by t."Дорога назначения"	
                                order by sum("Оценка пени")				
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_railway_mean_delay():
    sql = '''
        select "Дорога назначения", max(ra.file) as "Дор. назн."
            , sum("Дней просрочки, суток")/sum("Кол-во вагонорейсов") --avg("Дней просрочки, суток") / count(*)
                as "Средняя просрочка, сут"
	        from dashboard.dash_transport_empty t 
                left join sap_s4.rails_mapping ra
				    on t."Дорога назначения" = ra."db"
		            where t."Превышение даты истечение срока д" = 'Не удовлетворяет'
                            and (lower("Плательщик") like '%пгк%' 
						        or lower("Грузоотправитель") like '%пгк' 
						        or lower("Получатель") like '%пгк')
			                    group by t."Дорога назначения"
                                    order by avg("Дней просрочки, суток")
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

# Закладка динамика
def get_trans_empty_by_type():
    sql = '''
       select   
            case "Превышение даты истечение срока д" 
                when 'Удовлетворяет' then 'Без просрочки'
                when 'Не удовлетворяет' then 'С просрочкой'
                when 'Нет данных' then 'Нет данных для оценки' 
                else "Превышение даты истечение срока д" end as "Тип"
            , sum("Кол-во вагонорейсов") as "Кол-во вагонорейсов" 
                from dashboard.dash_transport_empty f 
                    where lower("Плательщик") like '%пгк%' 
						or lower("Грузоотправитель") like '%пгк' 
						or lower("Получатель") like '%пгк'
                        group by "Превышение даты истечение срока д"
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_money(): 
    sql = '''
        select "Тип", "Рассчитанная сумма" from (
            select 
                    case "Превышение даты истечение срока д" 
                        when 'Удовлетворяет' then 'Без просрочки'
                        when 'Не удовлетворяет' then 'Сумма тарифа для расчёта пени' 
                        else "Превышение даты истечение срока д" end as "Тип"
                    , sum("Рассчитанная сумма") as "Рассчитанная сумма"  
                    from dashboard.dash_transport_empty f where "Превышение даты истечение срока д" != 'Нет данных'
                            and (lower("Плательщик") like '%пгк%' 
                                or lower("Грузоотправитель") like '%пгк' 
                                or lower("Получатель") like '%пгк')
                            group by "Превышение даты истечение срока д"
                union all	
                select
                'Оценка пени' as "Тип"
                    , sum("Оценка пени") as "Рассчитанная сумма" 
                    from dashboard.dash_transport_empty f where "Превышение даты истечение срока д" = 'Не удовлетворяет'
                            and (lower("Плательщик") like '%пгк%' 
                                or lower("Грузоотправитель") like '%пгк' 
                                or lower("Получатель") like '%пгк')
                            group by "Превышение даты истечение срока д"
                ) t where "Тип" != 'Без просрочки'
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_type_month():
    sql = '''
            select 
                "Месяц"
                ,   case "Превышение даты истечение срока д" 
                        when 'Удовлетворяет' then 'Без просрочки'
                        when 'Не удовлетворяет' then 'С просрочкой' 
                        else "Превышение даты истечение срока д" end as "Тип"
                , sum("Кол-во вагонорейсов") as "Кол-во вагонорейсов" 
	            from dashboard.dash_transport_empty f 
                    where lower("Плательщик") like '%пгк%' 
						or lower("Грузоотправитель") like '%пгк' 
						or lower("Получатель") like '%пгк'
		                group by "Месяц", "Превышение даты истечение срока д"
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_money_month(): 
    sql = '''
        select "Месяц"
            ,   sum("Оценка пени") as "Оценка пени"
	        from dashboard.dash_transport_empty f 
                    where (lower("Плательщик") like '%пгк%' 
						    or lower("Грузоотправитель") like '%пгк' 
						    or lower("Получатель") like '%пгк') 
                        and "Превышение даты истечение срока д" = 'Не удовлетворяет'
		            group by "Месяц", "Превышение даты истечение срока д"
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

external_railway = ['БЕЛОРУССКАЯ', 'КАЗАХСТАНСКИЕ', 'ЛАТВИЙСКАЯ', 'ЛИТОВСКАЯ', 'ЭСТОНСКАЯ']

cols = {
    "tor_id" : "Код фрахтового заказа SAP",
    "tor_cat": "Категория накладной", 
    "tor_type": "Тип накладной",
    "tor_ert" : "Признак порожнего рейса",
    "item_type": "Тип позиции накладной",
    "item_cat" : "Категория позиции накладной",
    "platenumber" : "Вагон",
    "statuserw_text": "Статус вагона ЕРВ",
    "ownership_code_text": "Тип собственности по ЕРВ",
#     "labeltxt" : "Тип документа",
    "wb_id" : "Код накладной",
    "wb_freight_size_class" : "Вид отправки",             
    'created_on' : 'Дата cоздания накладной',
    "waybill_inv_num" : "Номер накладной ЭТРАН", 
    "shipper" : "Код перевозчика",
    "shipper_name" : "Грузоотправитель",                              
    "consignee": "Код грузополучателя",
    "consignee_name" : "Получатель", 
    "payer_s" : "Код плательщика",
    "payer_name" : "Плательщик",       
    "issuance_date_time" : "Дата выдачи документа", 
    "last_oper_date" : "Дата послед. операции",                                                                 
    "zzsource_station" : "Код станции отправления",                    
    "station_source_name" : "Станция отправления",
    "zzdest_station" : "Код станции назначения",
    "station_dest_name" : "Станция назначения", 
    "rw_id_s" : "Код дороги отправления",  
    "railway_name_source" : 'Дорога отправления',               
    "rw_id_d" : "Код дороги назначения",
    "railway_destination" : "Дорога назначения",
    "zzgu12_number" : "ГУ12", 
    "waybill_status" : "Статус накладной",
    "lifecycle" : "Жизненный цикл накладной",
    "creation_type" : "Тип создания накладной",
    "zcdtm_fcode" : "Код тип задания на пересылку",
    "fc_descr" : "Тип задания на пересылку",
    "zcdtm_fscode" : "Код подтипа задания на пересылку", 
    "fsc_descr" : "Подтип задания на пересылку",
    "zcdtm_tscode" : "Код технологического подкода",
    "tsc_descr" : "Технологический подкод",
    "invoicing" : "Статус фактурирования",
    'invoicing_text' : 'Статус фактурирования',
    "creation_date" : "Дата создания накладной SAP",
    "planned_load_date" : "Планируемая дата погрузки",       
    "load_date" : "Дата факт. погрузки",
    "expiry_date" : "Дата истеч. срока доставки",
    "placp_fromfrgnrw_dt" : "Дата принятия приемосдатчиком",
    "ready_for_exec_dt" : "Дата принятия груза к перевозке",
    "respacp_pers_name" : "ФИО приемасдатчика",
    "cons_notif_dt" : "Дата уведомления",   
    "actual_dep_dt" : "Факт. дата отправления",
    "actual_arr_dt" : "Факт. дата прибытия",
    "issuance_dt" : "Дата раскредитования",
    "due_type_id_chain" : "Цепь типов по платежам",
    "due_type_name_chain" : "Цепь названий по платежам", 
    "dist_minway_chain" : "Цепь расстояний по платежам",
    "version_chain" : "Цепь версий по платежам",
    "min_dist_way" : "Расстояние по последовательности", 
    "ttl_amount_chain" : "Цепь платежей",
    "net_amount_lcl" : "Общие затраты по накладной",  
    "sum_ttl_ammount" : "Рассчитанная сумма"             
}

# trans.rename(columns = cols).info()


# # Значения списка филиалов
# def get_branch_names(start_date, end_date, gruz, rod):
#     """Выгрузка списка филиалов"""
#     sql = '''
#         SELECT DISTINCT "Наименование филиала"
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#                     AND "Название груза ЕТСНГ" IN %s
#                     AND "Род подвижного состава" IN %s
#                     AND "Результат анализа" = 'Посредник'
#         ORDER BY "Наименование филиала" ASC
#     ''' % (start_date, end_date, gruz, rod)

#     # return pd.read_sql(sql, con=engine_cons)
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Значения полного списка филиалов
# def get_all_branch_names(start_date, end_date):
#     """Выгрузка списка филиалов"""
#     sql = '''
#         SELECT DISTINCT "Наименование филиала"
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#         ORDER BY "Наименование филиала" ASC
#     ''' % (start_date, end_date)

#     # return pd.read_sql(sql, con=engine_cons)
#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Значения списка групп грузов
# def get_cargo_names(start_date, end_date, branches, rod):
#     """Выгрузка групп грузов"""
#     sql = '''
#         SELECT DISTINCT "Название груза ЕТСНГ"
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#                     AND "Наименование филиала" IN %s
#                     AND "Род подвижного состава" IN %s
#                     AND "Результат анализа" = 'Посредник'
#         ORDER BY "Название груза ЕТСНГ" ASC
#     ''' % (start_date, end_date, branches, rod)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Значения полного списка групп грузов
# def get_all_cargo_names(start_date, end_date):
#     """Выгрузка групп грузов"""
#     sql = '''
#         SELECT DISTINCT "Название груза ЕТСНГ"
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#         ORDER BY "Название груза ЕТСНГ" ASC
#     ''' % (start_date, end_date)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Значения списка РПС
# def get_rps(start_date, end_date, branches, gruz):
#     """Выгрузка списка РПС"""
#     sql = '''
#         SELECT DISTINCT "Род подвижного состава"
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#                     AND "Наименование филиала" IN %s
#                     AND "Название груза ЕТСНГ" IN %s
#                     AND "Результат анализа" = 'Посредник'
#         ORDER BY "Род подвижного состава" ASC
#     ''' % (start_date, end_date, branches, gruz)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Значения полного списка РПС
# def get_all_rps(start_date, end_date):
#     """Выгрузка списка РПС"""
#     sql = '''
#         SELECT DISTINCT "Род подвижного состава"
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#         ORDER BY "Род подвижного состава" ASC
#     ''' % (start_date, end_date)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# # Максимальная дата в выгрузке
# def get_max_date():
#     """Максимальная дата в выгрузке"""
#     sql = '''
#     SELECT MAX(TO_DATE("Дата раскредитования", 'YYYYMMDD'))
#     FROM dashboard.resellers_cube
#     '''
#     # return engine_cons.execute(sql).fetchone()[0]
#     con = create_engine(config.POSTGRE_DB, max_identifier_length=128, encoding='utf-8')
#     return con.execute(sql).fetchone()[0]


# def get_top_resellers(start_date, end_date, branches, gruz, rod, sorting):
#     """Топ посредников по количеству рейсов"""
#     sql = """
#         SELECT a."Заказчик",
#             a."Название заказчика",
#             sum(a."Количество рейсов")::bigint AS "Количество рейсов",
#             c."Количество"::int AS "Количество посреднических рейсов",
#             round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
#             sum(a."Стоимость")::bigint AS "Стоимость рейсов",
#             c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
#             round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
#         FROM dashboard.resellers_cube a

#             LEFT JOIN (
#                 SELECT f."Заказчик",
#                     f."Результат анализа",
#                     sum("Количество рейсов") AS "Количество",
#                     sum("Стоимость") AS "Стоимость"
#                 FROM dashboard.resellers_cube f
#                 WHERE "Результат анализа" = 'Посредник'
#                     AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#                     AND "Наименование филиала" IN %s
#                     AND "Название груза ЕТСНГ" IN %s
#                     AND "Род подвижного состава" IN %s
#                 GROUP BY f."Заказчик",
#                     f."Результат анализа") c
#             ON a."Заказчик" = c."Заказчик"
#         WHERE a."Заказчик" IS NOT NULL
#             AND c."Результат анализа" = 'Посредник'
#             AND c."Количество" > 30
#             AND c."Стоимость" IS NOT NULL
#             AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             AND a."Наименование филиала" IN %s
#             AND a."Название груза ЕТСНГ" IN %s
#             AND a."Род подвижного состава" IN %s
#         GROUP BY a."Заказчик",
#             a."Название заказчика",
#             c."Количество",
#             c."Стоимость"
#         ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
#                     WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
#                     WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
#                     WHEN 'Сумма посреднических рейсов, руб.' THEN sum(a."Стоимость")::bigint
#                     WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
#                     WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
#                 END) DESC
#         LIMIT 10
#     """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

#     con=create_engine(os.environ['POSTGRE_URL_DASH']
#     df = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
#     con.close()

#      return df

# con=create_engine(os.environ['POSTGRE_URL_DASH']
# con.close()


# # Количество посреднических рейсов в разрезе филиалов
# def get_resellers_by_branches(start_date, end_date, branches, gruz, rod, sorting):
#     """Выгрузка количества посреднических рейсов в разрезе филиалов"""
#     # sql = """
#     #     SELECT a."Наименование филиала",
#     #         sum(a."Количество рейсов")::int AS "Количество рейсов",
#     #         b."Количество посреднических рейсов"::int AS "Количество посреднических рейсов",
#     #         round(b."Количество посреднических рейсов"::numeric/sum(a."Количество рейсов")::numeric,4)*100 AS "Доля посреднических рейсов",
#     #         sum(a."Стоимость")::bigint AS "Стоимость рейсов",
#     #         b."Стоимость"::bigint AS "Стоимость посреднических рейсов",
#     #         round(b."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
            
#     #     FROM(
#     #         (SELECT "Наименование филиала",
#     #             sum("Количество рейсов") AS "Количество рейсов",
#     #             sum("Стоимость") AS ""
#     #         FROM dashboard.resellers_cube
#     #         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#     #             AND "Наименование филиала" IN %s
#     #             AND "Название груза ЕТСНГ" IN %s
#     #             AND "Род подвижного состава" IN %s
#     #         GROUP BY "Наименование филиала") a
#     #     LEFT JOIN (
#     #         SELECT "Наименование филиала",
#     #             sum("Количество рейсов") AS "Количество посреднических рейсов"
#     #         FROM dashboard.resellers_cube
#     #         WHERE "Результат анализа" = 'Посредник'
#     #             AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#     #             AND "Наименование филиала" IN %s
#     #             AND "Название груза ЕТСНГ" IN %s
#     #             AND "Род подвижного состава" IN %s
#     #         GROUP BY "Наименование филиала") b
#     #             ON a."Наименование филиала" = b."Наименование филиала"
#     #     )
#     #     GROUP BY a."Наименование филиала",
#     #         b."Количество посреднических рейсов"
#     #     ORDER BY (CASE '%s' WHEN 'Количество' THEN b."Количество посреднических рейсов"::int
#     #                 WHEN 'Доля по количеству' THEN round(b."Количество посреднических рейсов"::numeric/sum(a."Количество рейсов")::numeric,4)*100
#     #             END) ASC
#     # """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)
#     sql = """
#         SELECT a."Сбытовая организация",
#             a."Наименование филиала",
#             sum(a."Количество рейсов")::bigint AS "Количество рейсов",
#             c."Количество"::int AS "Количество посреднических рейсов",
#             round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
#             sum(a."Стоимость")::bigint AS "Стоимость рейсов",
#             c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
#             round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
#         FROM dashboard.resellers_cube a

#             LEFT JOIN (
#                 SELECT f."Сбытовая организация",
#                     f."Наименование филиала",
#                     sum("Количество рейсов") AS "Количество",
#                     sum("Стоимость") AS "Стоимость"
#                 FROM dashboard.resellers_cube f
#                 WHERE "Результат анализа" = 'Посредник'
#                     AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#                     AND "Наименование филиала" IN %s
#                     AND "Название груза ЕТСНГ" IN %s
#                     AND "Род подвижного состава" IN %s
#                 GROUP BY f."Сбытовая организация",
#                     f."Наименование филиала",
#                     f."Результат анализа") c
#             ON a."Сбытовая организация" = c."Сбытовая организация"
#         WHERE a."Сбытовая организация" IS NOT NULL
#             AND c."Количество" > 30
#             AND c."Стоимость" IS NOT NULL
#             AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             AND a."Наименование филиала" IN %s
#             AND a."Название груза ЕТСНГ" IN %s
#             AND a."Род подвижного состава" IN %s
#         GROUP BY a."Сбытовая организация",
#             a."Наименование филиала",
#             c."Количество",
#             c."Стоимость"
#         ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
#                     WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
#                     WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
#                     WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
#                     WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
#                     WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
#                 END) ASC
#     """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# def get_resellers_by_rps(start_date, end_date, branches, gruz, rod, sorting):
#     """Выгрузка количества посреднических рейсов в разрезе РПС"""
#     sql = '''
#         SELECT a."Род подвижного состава",
#             sum(a."Количество рейсов")::bigint AS "Количество рейсов",
#             c."Количество"::int AS "Количество посреднических рейсов",
#             round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
#             sum(a."Стоимость")::bigint AS "Стоимость рейсов",
#             c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
#             round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
#         FROM dashboard.resellers_cube a

#             LEFT JOIN (
#                 SELECT f."Род подвижного состава",
#                     sum("Количество рейсов") AS "Количество",
#                     sum("Стоимость") AS "Стоимость"
#                 FROM dashboard.resellers_cube f
#                 WHERE "Результат анализа" = 'Посредник'
#                     AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#                     AND "Наименование филиала" IN %s
#                     AND "Название груза ЕТСНГ" IN %s
#                     AND "Род подвижного состава" IN %s
#                 GROUP BY f."Род подвижного состава",
#                     f."Результат анализа") c
#             ON a."Род подвижного состава" = c."Род подвижного состава"
#         WHERE a."Сбытовая организация" IS NOT NULL
#             AND c."Количество" > 30
#             AND c."Стоимость" IS NOT NULL
#             AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             AND a."Наименование филиала" IN %s
#             AND a."Название груза ЕТСНГ" IN %s
#             AND a."Род подвижного состава" IN %s
#         GROUP BY a."Род подвижного состава",
#             c."Количество",
#             c."Стоимость"
#         ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
#                     WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
#                     WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
#                     WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
#                     WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
#                     WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
#                 END) ASC
#     ''' % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# def get_resellers_cargo(start_date, end_date, branches, gruz, rod, sorting):
#     """Посреднические рейсы по грузам"""
#     sql = """
#         SELECT a."Код груза ЕТСНГ",
#             a."Название груза ЕТСНГ",
#             sum(a."Количество рейсов")::bigint AS "Количество рейсов",
#             c."Количество"::int AS "Количество посреднических рейсов",
#             round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
#             sum(a."Стоимость")::bigint AS "Стоимость рейсов",
#             c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
#             round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
#         FROM dashboard.resellers_cube a

#             LEFT JOIN (
#                 SELECT f."Код груза ЕТСНГ",
#                     f."Название груза ЕТСНГ",
#                     sum("Количество рейсов") AS "Количество",
#                     sum("Стоимость") AS "Стоимость"
#                 FROM dashboard.resellers_cube f
#                 WHERE "Результат анализа" = 'Посредник'
#                     AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#                     AND "Наименование филиала" IN %s
#                     AND "Название груза ЕТСНГ" IN %s
#                     AND "Род подвижного состава" IN %s
#                 GROUP BY f."Код груза ЕТСНГ",
#                     f."Название груза ЕТСНГ",
#                     f."Результат анализа") c
#             ON a."Код груза ЕТСНГ" = c."Код груза ЕТСНГ"
#         WHERE a."Сбытовая организация" IS NOT NULL
#             AND c."Количество" > 30
#             AND c."Стоимость" IS NOT NULL
#             AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             AND a."Наименование филиала" IN %s
#             AND a."Название груза ЕТСНГ" IN %s
#             AND a."Род подвижного состава" IN %s
#         GROUP BY a."Код груза ЕТСНГ",
#             a."Название груза ЕТСНГ",
#             c."Количество",
#             c."Стоимость"
#         ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
#                     WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
#                     WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
#                     WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
#                     WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
#                     WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
#                 END) DESC
#         LIMIT 10
#     """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# def get_resellers_count(start_date, end_date, branches, gruz, rod):
#     """Выгрузка количества посреднических рейсов"""
#     sql = '''
#         SELECT sum("Количество рейсов") AS "Количество"
#         FROM dashboard.resellers_cube
#         WHERE "Результат анализа" = 'Посредник'
#             AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             AND "Наименование филиала" IN %s
#             AND "Название груза ЕТСНГ" IN %s
#             AND "Род подвижного состава" IN %s
#     ''' % (start_date, end_date, branches, gruz, rod)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'],
#                                               max_identifier_length=128,
#                                               encoding='utf-8'))


# def get_resellers_share(start_date, end_date, branches, gruz, rod):
#     """Выгрузка доли посреднических рейсов"""
#     sql1 = '''
#         SELECT sum("Количество рейсов")::int AS "Количество посреднических рейсов"
#         FROM dashboard.resellers_cube
#         WHERE "Результат анализа" = 'Посредник'
#             AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             AND "Наименование филиала" IN %s
#             AND "Название груза ЕТСНГ" IN %s
#             AND "Род подвижного состава" IN %s
#             ''' % (start_date, end_date, branches, gruz, rod)
#     sql2 = '''
#         SELECT sum("Количество рейсов")::int AS "Количество рейсов"
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#         AND "Наименование филиала" IN %s
#         AND "Название груза ЕТСНГ" IN %s
#         AND "Род подвижного состава" IN %s
#     ''' % (start_date, end_date, branches, gruz, rod)
#     df1 = pd.read_sql(sql1, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
#     df2 = pd.read_sql(sql2, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

#     if df1['Количество посреднических рейсов'][0] and df2['Количество рейсов'][0]:
#         return str(round(float(df1['Количество посреднических рейсов'][0])/float(df2['Количество рейсов'][0])*100, 2)) + '%'
#     else:
#         return '0 %'
    


# def get_resellers_table(start_date, end_date, branches, gruz, rod):
#     """Выгрузка таблицы по посредникам"""
#     # Сделать, чтобы количество пересчитывалось в зависимости от даты
#     sql = '''
#         SELECT *
#         FROM dashboard.resellers_cube
#         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
#             AND "Результат анализа" = 'Посредник'
#             AND "Наименование филиала" IN %s
#             AND "Название груза ЕТСНГ" IN %s
#             AND "Род подвижного состава" IN %s
#     ''' % (start_date, end_date, branches, gruz, rod)

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# def get_resellers_dynamics(start_date, end_date, branches, gruz, rod):
#     """Выгрузка динамики по посредникам"""
#     sql = '''
#         SELECT a."Начало месяца",
#             a."Количество рейсов" AS "Количество посред рейсов",
#             a."Стоимость" AS "Стоимость посред рейсов",
#             b."Количество рейсов" AS "Количество рейсов",
#             b."Стоимость" AS "Стоимость рейсов",
#             round(a."Количество рейсов"/b."Количество рейсов"*100, 2) AS "Доля посред рейсов в шт",
#             round(a."Стоимость"::numeric/b."Стоимость"::numeric*100, 2) AS "Доля посред рейсов в руб" 
#         FROM (
#         (SELECT date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
#             sum("Количество рейсов") AS "Количество рейсов",
#             round(sum("Стоимость")) AS "Стоимость"
#         FROM dashboard.resellers_cube
#         WHERE "Результат анализа" = 'Посредник'
#             AND "Наименование филиала" IN %s
#             AND "Название груза ЕТСНГ" IN %s
#             AND "Род подвижного состава" IN %s
#         GROUP BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
#         ORDER BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) DESC) a
#             LEFT JOIN (
#                 SELECT date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
#                     sum("Количество рейсов") AS "Количество рейсов",
#                     round(sum("Стоимость")) AS "Стоимость"
#                 FROM dashboard.resellers_cube
#                 WHERE "Наименование филиала" IN %s
#                     AND "Название груза ЕТСНГ" IN %s
#                     AND "Род подвижного состава" IN %s
#                 GROUP BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
#                 ORDER BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) DESC
#             ) b
#             ON a."Начало месяца" = b."Начало месяца"
#         )
#         WHERE a."Начало месяца" BETWEEN '%s' AND '%s'
#     '''% (branches, gruz, rod, branches, gruz, rod, start_date, end_date)

#     # sql2 = '''
#     #     SELECT a."Дата",
#         #     a."Начало недели",
#         #     a."Начало месяца",
#         #     a."Количество рейсов" AS "Количество посред рейсов",
#         #     a."Стоимость" AS "Стоимость посред рейсов",
#         #     b."Количество рейсов" AS "Количество рейсов",
#         #     b."Стоимость" AS "Стоимость рейсов",
#         #     round(a."Количество рейсов"/b."Количество рейсов"*100, 2) AS "Доля посред рейсов в шт",
#         #     round(a."Стоимость"::numeric/b."Стоимость"::numeric*100, 2) AS "Доля посред рейсов в руб" 
#         # FROM (
#         # (SELECT TO_DATE("Дата раскредитования",'YYYYMMDD') AS "Дата",
#         #     (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube) + 
#         #     (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7 AS "Начало недели",
#         #     date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
#         #     sum("Количество рейсов") AS "Количество рейсов",
#         #     round(sum("Стоимость")) AS "Стоимость"
#         # FROM dashboard.resellers_cube
#         # WHERE "Результат анализа" = 'Посредник'
#         # GROUP BY TO_DATE("Дата раскредитования",'YYYYMMDD'),
#         #     (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7,
#         #     date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
#         # ORDER BY TO_DATE("Дата раскредитования",'YYYYMMDD') DESC) a
#         #     LEFT JOIN (
#         #         SELECT TO_DATE("Дата раскредитования",'YYYYMMDD') AS "Дата",
#         #             (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube) + 
#         #             (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7 AS "Начало недели",
#         #             date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
#         #             sum("Количество рейсов") AS "Количество рейсов",
#         #             round(sum("Стоимость")) AS "Стоимость"
#         #         FROM dashboard.resellers_cube
#         #         GROUP BY TO_DATE("Дата раскредитования",'YYYYMMDD'),
#         #             (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7,
#         #             date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
#         #         ORDER BY TO_DATE("Дата раскредитования",'YYYYMMDD') DESC
#         #     ) b
#         #     ON a."Дата" = b."Дата"
#         # )
#     # '''

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
