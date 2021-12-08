"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
import front_ex.config as config
from sqlalchemy import create_engine


# Значения списка РПС
def get_rps(start_date, end_date):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT rod_id_text
        FROM dashboard.tor_ik
        WHERE DATNRP BETWEEN '%s' AND '%s'
        ORDER BY rod_id_text ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения полного списка РПС
def get_all_rps(start_date, end_date):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT rod_id_text
        FROM dashboard.tor_ik
        WHERE DATNRP BETWEEN '%s' AND '%s'
        ORDER BY rod_id_text ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Максимальная дата в выгрузке
def get_max_date():
    """Максимальная дата в выгрузке"""
    sql = '''
    SELECT MAX(DATNRP)
    FROM dashboard.tor_ik
    '''
    # return engine_cons.execute(sql).fetchone()[0]
    con = create_engine(config.POSTGRE_DB, max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]

    
def get_tors_count(start_date, end_date):
    """Выгрузка количества"""
    sql = '''
        SELECT 
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a.DATNRP BETWEEN '%s' AND '%s'
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

def get_tors_by_rps(start_date, end_date):
    """Выгрузка ремонтов в разрезе РПС"""
    sql = '''
        SELECT 
        a.ROD_ID_TEXT AS "РПС", 
        a.ILATX AS "Вид ремонта",
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a."DATNRP" BETWEEN '%s' AND '%s'
        GROUP BY a.ROD_ID_TEXT, a.ILATX
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_tors_by_type(start_date, end_date):
    """Выгрузка ремонтов в разрезе видов ТОР"""
    sql = '''
        SELECT 
        a.ILATX AS "Вид ремонта",
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a.DATNRP BETWEEN '%s' AND '%s'
        GROUP BY a.ILATX
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

"""Выгрузка топ кодов неисправности в разрезе РПС"""

"""Выгрузка топ кодов неисправности в разрезе видов ТОР"""

"""Выгрузка средняя длительность ремонтов"""


def get_top_tors(start_date, end_date, branches, gruz, rod, sorting):
    """Топ посредников по количеству рейсов"""
    sql = """
        SELECT a."Заказчик",
            a."Название заказчика",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.tors_cube a

            LEFT JOIN (
                SELECT f."Заказчик",
                    f."Результат анализа",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.tors_cube f
                WHERE "Результат анализа" = 'Посредник'
                    AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY f."Заказчик",
                    f."Результат анализа") c
            ON a."Заказчик" = c."Заказчик"
        WHERE a."Заказчик" IS NOT NULL
            AND c."Результат анализа" = 'Посредник'
            AND c."Количество" > 30
            AND c."Стоимость" IS NOT NULL
            AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND a."Наименование филиала" IN %s
            AND a."Название груза ЕТСНГ" IN %s
            AND a."Род подвижного состава" IN %s
        GROUP BY a."Заказчик",
            a."Название заказчика",
            c."Количество",
            c."Стоимость"
        ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
                    WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
                    WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
                    WHEN 'Сумма посреднических рейсов, руб.' THEN sum(a."Стоимость")::bigint
                    WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
                    WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
                END) DESC
        LIMIT 10
    """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

