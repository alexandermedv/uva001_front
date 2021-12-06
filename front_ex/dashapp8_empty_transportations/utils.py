"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
from pandas.io import sql
import front_ex.config as config
from sqlalchemy import create_engine
import datetime as dt

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

def get_trans_empty_by_railway_delay(railway='', start_date=None, end_date=None):
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
    ''' 
    if railway:
        str = sql + 'and "Дорога назначения" = {railway}'.format(railway = railway)
    sql = sql + '''
        group by t."Дорога назначения"
            order by sum(case when t."Превышение даты истечение срока д" = 'Не удовлетворяет' then "Кол-во вагонорейсов" else 0 end) 
        ) t
    ''' 
    # print(sql)
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
def get_trans_empty_by_type(railway='', start_date=None, end_date=None):
    sql = '''
       select   
            case "Превышение даты истечение срока д" 
                when 'Удовлетворяет' then 'Без просрочки'
                when 'Не удовлетворяет' then 'С просрочкой'
                when 'Нет данных' then 'Нет данных для оценки' 
                else "Превышение даты истечение срока д" end as "Тип"
                , sum("Кол-во вагонорейсов") as "Кол-во вагонорейсов" 
                    from dashboard.dash_transport_empty f 
                        where (lower("Плательщик") like '%пгк%' 
                            or lower("Грузоотправитель") like '%пгк' 
                            or lower("Получатель") like '%пгк')
    '''
    if railway:
        sql = sql + '''
            and "Дорога назначения" = '{railway}'
        '''.format(railway = railway)
    if start_date and end_date:
        sql = sql + '''
            and "Месяц" >= '{start_date}'
            and "Месяц" <= '{end_date}'
        '''.format(start_date = start_date, end_date = end_date)
    sql = sql + '''
        group by "Превышение даты истечение срока д"
            order by "Превышение даты истечение срока д" desc
    '''
    # print(sql)
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_money(railway, start_date=None, end_date=None): 
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
    '''
    if railway:
        sql = sql + '''
            and "Дорога назначения" = '{railway}'
        '''.format(railway = railway) 
    if start_date and end_date:
        sql = sql + '''
            and "Месяц" >= '{start_date}'
            and "Месяц" <= '{end_date}'
        '''.format(start_date = start_date, end_date = end_date)
    sql = sql + '''      
                            group by "Превышение даты истечение срока д"
                union all	
                select
                'Оценка пени' as "Тип"
                    , sum("Оценка пени") as "Рассчитанная сумма" 
                    from dashboard.dash_transport_empty f where "Превышение даты истечение срока д" = 'Не удовлетворяет'
                            and (lower("Плательщик") like '%пгк%' 
                                or lower("Грузоотправитель") like '%пгк' 
                                or lower("Получатель") like '%пгк')
    '''
    if railway:
        sql = sql + '''
            and "Дорога назначения" = '{railway}'
        '''.format(railway = railway) 
    if start_date and end_date:
        sql = sql + '''
            and "Месяц" >= '{start_date}'
            and "Месяц" <= '{end_date}'
        '''.format(start_date = start_date, end_date = end_date)
    sql = sql + '''    
                    group by "Превышение даты истечение срока д"
                ) t where "Тип" != 'Без просрочки'
    '''
    # print(sql)
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_type_month(railway, start_date=None, end_date=None):
    sql = '''
            select 
                "Месяц"
                ,   case "Превышение даты истечение срока д" 
                        when 'Удовлетворяет' then 'Без просрочки'
                        when 'Не удовлетворяет' then 'С просрочкой' 
                        else "Превышение даты истечение срока д" end as "Тип"
                , sum("Кол-во вагонорейсов") as "Кол-во вагонорейсов" 
	            from dashboard.dash_transport_empty f 
                    where (lower("Плательщик") like '%пгк%' 
						or lower("Грузоотправитель") like '%пгк' 
						or lower("Получатель") like '%пгк')
    '''
    if railway:
        sql = sql + '''
            and "Дорога назначения" = '{railway}'
        '''.format(railway = railway) 
    if start_date and end_date:
        sql = sql + '''
            and "Месяц" >= '{start_date}'
            and "Месяц" <= '{end_date}'
        '''.format(start_date = start_date, end_date = end_date)
    sql = sql + '''
    	                    group by "Месяц", "Превышение даты истечение срока д"   
                               -- order by "Месяц", "Превышение даты истечение срока д" desc       
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df

def get_trans_empty_by_money_month(railway, start_date=None, end_date=None): 
    sql = '''
        select "Месяц"
            ,   sum("Оценка пени") as "Оценка пени"
	        from dashboard.dash_transport_empty f 
                    where (lower("Плательщик") like '%пгк%' 
						    or lower("Грузоотправитель") like '%пгк' 
						    or lower("Получатель") like '%пгк') 
                        and "Превышение даты истечение срока д" = 'Не удовлетворяет'
    '''
    if railway:
        sql = sql + '''
            and "Дорога назначения" = '{railway}'
        '''.format(railway = railway) 	
    if start_date and end_date:
        sql = sql + '''
            and "Месяц" >= '{start_date}'
            and "Месяц" <= '{end_date}'
        '''.format(start_date = start_date, end_date = end_date)  
    sql = sql + '''         
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
