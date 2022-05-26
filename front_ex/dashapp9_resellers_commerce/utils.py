"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
# import front_ex.config as config
from sqlalchemy import create_engine


# Значения списка филиалов
def get_branch_names(start_date, end_date, gruz, rod):
    """Выгрузка списка филиалов"""
    sql = '''
        SELECT DISTINCT "Наименование филиала"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                    AND "Результат анализа" = 'Посредник'
        ORDER BY "Наименование филиала" ASC
    ''' % (start_date, end_date, gruz, rod)

    # return pd.read_sql(sql, con=engine_cons)
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения полного списка филиалов
def get_all_branch_names(start_date, end_date):
    """Выгрузка списка филиалов"""
    sql = '''
        SELECT DISTINCT "Наименование филиала"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        ORDER BY "Наименование филиала" ASC
    ''' % (start_date, end_date)

    # return pd.read_sql(sql, con=engine_cons)
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения списка групп грузов
def get_cargo_names(start_date, end_date, branches, rod):
    """Выгрузка групп грузов"""
    sql = '''
        SELECT DISTINCT "Название груза ЕТСНГ"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Род подвижного состава" IN %s
                    AND "Результат анализа" = 'Посредник'
        ORDER BY "Название груза ЕТСНГ" ASC
    ''' % (start_date, end_date, branches, rod)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения полного списка групп грузов
def get_all_cargo_names(start_date, end_date):
    """Выгрузка групп грузов"""
    sql = '''
        SELECT DISTINCT "Название груза ЕТСНГ"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        ORDER BY "Название груза ЕТСНГ" ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения списка РПС
def get_rps(start_date, end_date, branches, gruz):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT "Род подвижного состава"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Результат анализа" = 'Посредник'
        ORDER BY "Род подвижного состава" ASC
    ''' % (start_date, end_date, branches, gruz)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения полного списка РПС
def get_all_rps(start_date, end_date):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT "Род подвижного состава"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        ORDER BY "Род подвижного состава" ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Максимальная дата в выгрузке
def get_max_date():
    """Максимальная дата в выгрузке"""
    sql = '''
    SELECT MAX(TO_DATE("Дата раскредитования", 'YYYYMMDD'))
    FROM dashboard.resellers_commerce_cube
    '''
    # return engine_cons.execute(sql).fetchone()[0]
    con = create_engine(config.POSTGRE_DB, max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]


def get_top_resellers(start_date, end_date, branches, gruz, rod, sorting):
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
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Заказчик",
                    f."Результат анализа",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
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


def get_top_resellers_detailed(start_date, end_date, branches, gruz, rod, sorting):
    """Топ посредников по количеству рейсов - развернутые данные"""
    sql = """
        SELECT *
        FROM dashboard.resellers_commerce_results
        WHERE "Заказчик" IN (
            SELECT "Заказчик" FROM (
        
        SELECT a."Заказчик",
            a."Название заказчика",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Заказчик",
                    f."Результат анализа",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
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
        ) z
        )
    """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Количество посреднических рейсов в разрезе филиалов
def get_resellers_by_branches(start_date, end_date, branches, gruz, rod, sorting):
    """Выгрузка количества посреднических рейсов в разрезе филиалов"""
    sql = """
        SELECT a."Сбытовая организация",
            a."Наименование филиала",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Сбытовая организация",
                    f."Наименование филиала",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
                WHERE "Результат анализа" = 'Посредник'
                    AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY f."Сбытовая организация",
                    f."Наименование филиала",
                    f."Результат анализа") c
            ON a."Сбытовая организация" = c."Сбытовая организация"
        WHERE a."Сбытовая организация" IS NOT NULL
            AND c."Количество" > 30
            AND c."Стоимость" IS NOT NULL
            AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND a."Наименование филиала" IN %s
            AND a."Название груза ЕТСНГ" IN %s
            AND a."Род подвижного состава" IN %s
        GROUP BY a."Сбытовая организация",
            a."Наименование филиала",
            c."Количество",
            c."Стоимость"
        ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
                    WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
                    WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
                    WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
                    WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
                    WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
                END) ASC
    """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Количество посреднических рейсов в разрезе филиалов
def get_resellers_by_branches_detailed(start_date, end_date, branches, gruz, rod, sorting):
    """Выгрузка количества посреднических рейсов в разрезе филиалов - детальные данные для таблицы"""
    sql = """
        SELECT *
        FROM dashboard.resellers_commerce_results
        WHERE "Сбытовая организация" IN (
            SELECT "Сбытовая организация" FROM (

        SELECT a."Сбытовая организация",
            a."Наименование филиала",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Сбытовая организация",
                    f."Наименование филиала",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
                WHERE "Результат анализа" = 'Посредник'
                    AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY f."Сбытовая организация",
                    f."Наименование филиала",
                    f."Результат анализа") c
            ON a."Сбытовая организация" = c."Сбытовая организация"
        WHERE a."Сбытовая организация" IS NOT NULL
            AND c."Количество" > 30
            AND c."Стоимость" IS NOT NULL
            AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND a."Наименование филиала" IN %s
            AND a."Название груза ЕТСНГ" IN %s
            AND a."Род подвижного состава" IN %s
        GROUP BY a."Сбытовая организация",
            a."Наименование филиала",
            c."Количество",
            c."Стоимость"
        ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
                    WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
                    WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
                    WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
                    WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
                    WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
                END) ASC
        ) z
        )
    """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_resellers_by_rps(start_date, end_date, branches, gruz, rod, sorting):
    """Выгрузка количества посреднических рейсов в разрезе РПС"""
    sql = '''
        SELECT a."Род подвижного состава",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Род подвижного состава",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
                WHERE "Результат анализа" = 'Посредник'
                    AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY f."Род подвижного состава",
                    f."Результат анализа") c
            ON a."Род подвижного состава" = c."Род подвижного состава"
        WHERE a."Сбытовая организация" IS NOT NULL
            AND c."Количество" > 30
            AND c."Стоимость" IS NOT NULL
            AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND a."Наименование филиала" IN %s
            AND a."Название груза ЕТСНГ" IN %s
            AND a."Род подвижного состава" IN %s
        GROUP BY a."Род подвижного состава",
            c."Количество",
            c."Стоимость"
        ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
                    WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
                    WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
                    WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
                    WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
                    WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
                END) ASC
    ''' % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_resellers_by_rps_detailed(start_date, end_date, branches, gruz, rod, sorting):
    """Выгрузка количества посреднических рейсов в разрезе РПС - детальные данные для таблицы"""
    sql = '''
        SELECT *
        FROM dashboard.resellers_commerce_results
        WHERE "Род подвижного состава" IN (
            SELECT "Род подвижного состава" FROM (

        SELECT a."Род подвижного состава",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Род подвижного состава",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
                WHERE "Результат анализа" = 'Посредник'
                    AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY f."Род подвижного состава",
                    f."Результат анализа") c
            ON a."Род подвижного состава" = c."Род подвижного состава"
        WHERE a."Сбытовая организация" IS NOT NULL
            AND c."Количество" > 30
            AND c."Стоимость" IS NOT NULL
            AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND a."Наименование филиала" IN %s
            AND a."Название груза ЕТСНГ" IN %s
            AND a."Род подвижного состава" IN %s
        GROUP BY a."Род подвижного состава",
            c."Количество",
            c."Стоимость"
        ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
                    WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
                    WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
                    WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
                    WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
                    WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
                END) ASC
        ) z
        )
    ''' % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_resellers_cargo(start_date, end_date, branches, gruz, rod, sorting):
    """Посреднические рейсы по грузам"""
    sql = """
        SELECT a."Код груза ЕТСНГ",
            a."Название груза ЕТСНГ",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Код груза ЕТСНГ",
                    f."Название груза ЕТСНГ",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
                WHERE "Результат анализа" = 'Посредник'
                    AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY f."Код груза ЕТСНГ",
                    f."Название груза ЕТСНГ",
                    f."Результат анализа") c
            ON a."Код груза ЕТСНГ" = c."Код груза ЕТСНГ"
        WHERE a."Сбытовая организация" IS NOT NULL
            AND c."Количество" > 30
            AND c."Стоимость" IS NOT NULL
            AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND a."Наименование филиала" IN %s
            AND a."Название груза ЕТСНГ" IN %s
            AND a."Род подвижного состава" IN %s
        GROUP BY a."Код груза ЕТСНГ",
            a."Название груза ЕТСНГ",
            c."Количество",
            c."Стоимость"
        ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
                    WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
                    WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
                    WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
                    WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
                    WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
                END) DESC
        LIMIT 10
    """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_resellers_cargo_detailed(start_date, end_date, branches, gruz, rod, sorting):
    """Посреднические рейсы по грузам - детальные данные для таблицы"""
    sql = """
        SELECT *
        FROM dashboard.resellers_commerce_results
        WHERE "Код груза ЕТСНГ" IN (
            SELECT "Код груза ЕТСНГ" FROM (

        SELECT a."Код груза ЕТСНГ",
            a."Название груза ЕТСНГ",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_commerce_cube a

            LEFT JOIN (
                SELECT f."Код груза ЕТСНГ",
                    f."Название груза ЕТСНГ",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_commerce_cube f
                WHERE "Результат анализа" = 'Посредник'
                    AND TO_DATE(f."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY f."Код груза ЕТСНГ",
                    f."Название груза ЕТСНГ",
                    f."Результат анализа") c
            ON a."Код груза ЕТСНГ" = c."Код груза ЕТСНГ"
        WHERE a."Сбытовая организация" IS NOT NULL
            AND c."Количество" > 30
            AND c."Стоимость" IS NOT NULL
            AND TO_DATE(a."Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND a."Наименование филиала" IN %s
            AND a."Название груза ЕТСНГ" IN %s
            AND a."Род подвижного состава" IN %s
        GROUP BY a."Код груза ЕТСНГ",
            a."Название груза ЕТСНГ",
            c."Количество",
            c."Стоимость"
        ORDER BY (CASE '%s' WHEN 'Количество посреднических рейсов' THEN c."Количество"::int
                    WHEN 'Доля по количеству' THEN round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2)
                    WHEN 'Количество рейсов' THEN sum(a."Количество рейсов")
                    WHEN 'Сумма посреднических рейсов, руб.' THEN c."Стоимость"::bigint
                    WHEN 'Доля по сумме' THEN round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2)
                    WHEN 'Сумма, руб.' THEN sum(a."Стоимость")::bigint
                END) DESC
        LIMIT 10
        ) z
        )
    """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_resellers_kol(start_date, end_date, branches, gruz, rod):
    """Выгрузка количества посредников"""
    sql = '''
        SELECT count(DISTINCT a."Заказчик") AS "Количество"
        FROM dashboard.resellers_commerce_results a
            LEFT JOIN dashboard.resellers_commerce_cube b
                ON a."Заказчик" = b."Заказчик"
                AND a."Грузоотправитель" = b."Грузоотправитель"
                AND a."Грузополучатель" = b."Грузополучатель"
        WHERE a."Результат анализа" = 'Посредник'
            AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND b."Наименование филиала" IN %s
            AND b."Название груза ЕТСНГ" IN %s
            AND b."Род подвижного состава" IN %s

    ''' % (start_date, end_date, branches, gruz, rod)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'],
                                              max_identifier_length=128,
                                              encoding='utf-8'))


def get_resellers_count(start_date, end_date, branches, gruz, rod):
    """Выгрузка количества посреднических рейсов"""
    sql = '''
        SELECT sum("Количество рейсов") AS "Количество"
        FROM dashboard.resellers_commerce_cube
        WHERE "Результат анализа" = 'Посредник'
            AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
    ''' % (start_date, end_date, branches, gruz, rod)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'],
                                              max_identifier_length=128,
                                              encoding='utf-8'))


def get_resellers_sum(start_date, end_date, branches, gruz, rod):
    """Выгрузка суммы посреднических рейсов в деньгах"""
    sql = '''
        SELECT sum("Стоимость") AS "Стоимость"
        FROM dashboard.resellers_commerce_cube
        WHERE "Результат анализа" = 'Посредник'
            AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
    ''' % (start_date, end_date, branches, gruz, rod)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'],
                                              max_identifier_length=128,
                                              encoding='utf-8'))


def get_resellers_share(start_date, end_date, branches, gruz, rod):
    """Выгрузка доли посреднических рейсов"""
    sql1 = '''
        SELECT sum("Количество рейсов")::int AS "Количество посреднических рейсов"
        FROM dashboard.resellers_commerce_cube
        WHERE "Результат анализа" = 'Посредник'
            AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
            ''' % (start_date, end_date, branches, gruz, rod)
    sql2 = '''
        SELECT sum("Количество рейсов")::int AS "Количество рейсов"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        AND "Наименование филиала" IN %s
        AND "Название груза ЕТСНГ" IN %s
        AND "Род подвижного состава" IN %s
    ''' % (start_date, end_date, branches, gruz, rod)
    df1 = pd.read_sql(sql1, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
    df2 = pd.read_sql(sql2, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

    if df1['Количество посреднических рейсов'][0] and df2['Количество рейсов'][0]:
        return str(round(float(df1['Количество посреднических рейсов'][0])/float(df2['Количество рейсов'][0])*100, 2)) + '%'
    else:
        return '0 %'


def get_resellers_share_money(start_date, end_date, branches, gruz, rod):
    """Выгрузка доли посреднических рейсов в деньгах"""
    sql1 = '''
        SELECT sum("Стоимость")::bigint AS "Стоимость посреднических рейсов"
        FROM dashboard.resellers_commerce_cube
        WHERE "Результат анализа" = 'Посредник'
            AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
            ''' % (start_date, end_date, branches, gruz, rod)
    sql2 = '''
        SELECT sum("Стоимость")::bigint AS "Стоимость рейсов"
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        AND "Наименование филиала" IN %s
        AND "Название груза ЕТСНГ" IN %s
        AND "Род подвижного состава" IN %s
    ''' % (start_date, end_date, branches, gruz, rod)
    df1 = pd.read_sql(sql1, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
    df2 = pd.read_sql(sql2, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

    if df1['Стоимость посреднических рейсов'][0] and df2['Стоимость рейсов'][0]:
        return str(round(float(df1['Стоимость посреднических рейсов'][0])/float(df2['Стоимость рейсов'][0])*100, 2)) + '%'
    else:
        return '0 %'
    


def get_resellers_table(start_date, end_date, branches, gruz, rod):
    """Выгрузка таблицы по посредникам"""
    # Сделать, чтобы количество пересчитывалось в зависимости от даты
    sql = '''
        SELECT *
        FROM dashboard.resellers_commerce_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND "Результат анализа" = 'Посредник'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
    ''' % (start_date, end_date, branches, gruz, rod)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_resellers_dynamics(start_date, end_date, branches, gruz, rod):
    """Выгрузка динамики по посредникам"""
    sql = '''
        SELECT a."Начало месяца",
            a."Количество рейсов" AS "Количество посред рейсов",
            a."Стоимость" AS "Стоимость посред рейсов",
            b."Количество рейсов" AS "Количество рейсов",
            b."Стоимость" AS "Стоимость рейсов",
            round(a."Количество рейсов"/b."Количество рейсов"*100, 2) AS "Доля посред рейсов в шт",
            round(a."Стоимость"::numeric/b."Стоимость"::numeric*100, 2) AS "Доля посред рейсов в руб" 
        FROM (
        (SELECT date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
            sum("Количество рейсов") AS "Количество рейсов",
            round(sum("Стоимость")) AS "Стоимость"
        FROM dashboard.resellers_commerce_cube
        WHERE "Результат анализа" = 'Посредник'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
        GROUP BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
        ORDER BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) DESC) a
            LEFT JOIN (
                SELECT date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
                    sum("Количество рейсов") AS "Количество рейсов",
                    round(sum("Стоимость")) AS "Стоимость"
                FROM dashboard.resellers_commerce_cube
                WHERE "Наименование филиала" IN %s
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                GROUP BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
                ORDER BY date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) DESC
            ) b
            ON a."Начало месяца" = b."Начало месяца"
        )
        WHERE a."Начало месяца" BETWEEN '%s' AND '%s'
    '''% (branches, gruz, rod, branches, gruz, rod, start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
