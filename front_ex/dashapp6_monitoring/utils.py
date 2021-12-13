"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
import front_ex.config as config
from sqlalchemy import create_engine


# Значения списка филиалов
def get_branch_names(start_date, end_date, gruz, rod):
    """Выгрузка списка филиалов"""
    sql = '''
        SELECT DISTINCT "Наименование филиала"
        FROM dashboard.resellers_cube
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
        FROM dashboard.resellers_cube
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
        FROM dashboard.resellers_cube
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
        FROM dashboard.resellers_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        ORDER BY "Название груза ЕТСНГ" ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения списка РПС
def get_rps(start_date, end_date, branches, gruz):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT "Род подвижного состава"
        FROM dashboard.resellers_cube
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
        FROM dashboard.resellers_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        ORDER BY "Род подвижного состава" ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Максимальная дата в выгрузке
def get_max_date():
    """Максимальная дата в выгрузке"""
    sql = '''
    SELECT MAX(TO_DATE("Дата раскредитования", 'YYYYMMDD'))
    FROM dashboard.resellers_cube
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
        FROM dashboard.resellers_cube a

            LEFT JOIN (
                SELECT f."Заказчик",
                    f."Результат анализа",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_cube f
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


# Количество посреднических рейсов в разрезе филиалов
def get_resellers_by_branches(start_date, end_date, branches, gruz, rod, sorting):
    """Выгрузка количества посреднических рейсов в разрезе филиалов"""
    # sql = """
    #     SELECT a."Наименование филиала",
    #         sum(a."Количество рейсов")::int AS "Количество рейсов",
    #         b."Количество посреднических рейсов"::int AS "Количество посреднических рейсов",
    #         round(b."Количество посреднических рейсов"::numeric/sum(a."Количество рейсов")::numeric,4)*100 AS "Доля посреднических рейсов",
    #         sum(a."Стоимость")::bigint AS "Стоимость рейсов",
    #         b."Стоимость"::bigint AS "Стоимость посреднических рейсов",
    #         round(b."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
            
    #     FROM(
    #         (SELECT "Наименование филиала",
    #             sum("Количество рейсов") AS "Количество рейсов",
    #             sum("Стоимость") AS ""
    #         FROM dashboard.resellers_cube
    #         WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
    #             AND "Наименование филиала" IN %s
    #             AND "Название груза ЕТСНГ" IN %s
    #             AND "Род подвижного состава" IN %s
    #         GROUP BY "Наименование филиала") a
    #     LEFT JOIN (
    #         SELECT "Наименование филиала",
    #             sum("Количество рейсов") AS "Количество посреднических рейсов"
    #         FROM dashboard.resellers_cube
    #         WHERE "Результат анализа" = 'Посредник'
    #             AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
    #             AND "Наименование филиала" IN %s
    #             AND "Название груза ЕТСНГ" IN %s
    #             AND "Род подвижного состава" IN %s
    #         GROUP BY "Наименование филиала") b
    #             ON a."Наименование филиала" = b."Наименование филиала"
    #     )
    #     GROUP BY a."Наименование филиала",
    #         b."Количество посреднических рейсов"
    #     ORDER BY (CASE '%s' WHEN 'Количество' THEN b."Количество посреднических рейсов"::int
    #                 WHEN 'Доля по количеству' THEN round(b."Количество посреднических рейсов"::numeric/sum(a."Количество рейсов")::numeric,4)*100
    #             END) ASC
    # """ % (start_date, end_date, branches, gruz, rod, start_date, end_date, branches, gruz, rod, sorting)
    sql = """
        SELECT a."Сбытовая организация",
            a."Наименование филиала",
            sum(a."Количество рейсов")::bigint AS "Количество рейсов",
            c."Количество"::int AS "Количество посреднических рейсов",
            round(c."Количество"::numeric/sum(a."Количество рейсов")::numeric*100, 2) AS "Доля посреднических рейсов",
            sum(a."Стоимость")::bigint AS "Стоимость рейсов",
            c."Стоимость"::bigint AS "Стоимость посреднических рейсов",
            round(c."Стоимость"::numeric/sum(a."Стоимость")::numeric*100, 2) AS "Доля ст посреднических рейсов"
        FROM dashboard.resellers_cube a

            LEFT JOIN (
                SELECT f."Сбытовая организация",
                    f."Наименование филиала",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_cube f
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
        FROM dashboard.resellers_cube a

            LEFT JOIN (
                SELECT f."Род подвижного состава",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_cube f
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
        FROM dashboard.resellers_cube a

            LEFT JOIN (
                SELECT f."Код груза ЕТСНГ",
                    f."Название груза ЕТСНГ",
                    sum("Количество рейсов") AS "Количество",
                    sum("Стоимость") AS "Стоимость"
                FROM dashboard.resellers_cube f
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


def get_resellers_count(start_date, end_date, branches, gruz, rod):
    """Выгрузка количества посреднических рейсов"""
    sql = '''
        SELECT sum("Количество рейсов") AS "Количество"
        FROM dashboard.resellers_cube
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
        FROM dashboard.resellers_cube
        WHERE "Результат анализа" = 'Посредник'
            AND TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
            ''' % (start_date, end_date, branches, gruz, rod)
    sql2 = '''
        SELECT sum("Количество рейсов")::int AS "Количество рейсов"
        FROM dashboard.resellers_cube
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
    


def get_resellers_table(start_date, end_date, branches, gruz, rod):
    """Выгрузка таблицы по посредникам"""
    # Сделать, чтобы количество пересчитывалось в зависимости от даты
    sql = '''
        SELECT *
        FROM dashboard.resellers_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            AND "Результат анализа" = 'Посредник'
            AND "Наименование филиала" IN %s
            AND "Название груза ЕТСНГ" IN %s
            AND "Род подвижного состава" IN %s
    ''' % (start_date, end_date, branches, gruz, rod)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


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

#     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_get_open_ap_by_groups_182():
    """Открытые планы мероприятий по группам 0-182 дня"""

    sql = '''
        SELECT z.issue_group AS issue_group,
            z.issue_risk_level AS issue_risk_level,
            count(*)
        FROM (

            SELECT a.*,
                        c."Language3" AS issue_group, 
                        e."Language3" AS issue_type,
                        g."Language3" AS issue_risk_level,
                        h."IDFld",
                        i.open_actplans,
                        DATE(j."AP_date") AS "AP_date",
                        DATE('2021-11-30') AS "Reporting_date",
                        DATE('2021-11-30') - DATE(j."AP_date") AS "duration"
                    FROM dashboard.issues a
                    LEFT JOIN dashboard.udfvalue b
                        ON a."FindGroup" = b."UDFValueID"
                    LEFT JOIN dashboard.languageaa c
                        ON b."LanguageID"::text = c."IDFld"::text
                            AND c."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.udfvalue d
                        ON a."FindType" = d."UDFValueID"
                    LEFT JOIN dashboard.languageaa e
                        ON d."LanguageID"::text = e."IDFld"::text
                            AND e."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.udfvalue f
                        ON a."FindRisk" = f."UDFValueID"
                    LEFT JOIN dashboard.languageaa g
                        ON f."LanguageID"::text = g."IDFld"::text
                            AND g."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.activities h
                        ON a."AuditID" = h."GuiIDFld"

                    LEFT JOIN (
                        SELECT "OrigID", count(*) AS open_actplans
                        FROM dashboard.actplans
                        WHERE "APADate" IS NULL
                            AND "APStatus" <> '61'
                            AND "Deleted" = '-1'
                        GROUP BY "OrigID"
                        ) i
                        ON a."IDFld" = i."OrigID"
                        
                    LEFT JOIN (
                        SELECT "Iss", min("AP_date") AS "AP_date"
                            FROM dashboard.ap_dates
                            GROUP BY "Iss"
                    ) j
                        ON a."Subject" = j."Iss"
                        
                    WHERE i.open_actplans IS NOT NULL
                        AND h."IDFld" <> '2021 Тест'
                        AND h."IDFld" <> '2021 Тест 2 - 1'
                        AND "Subject" IS NOT NULL
                        AND a."Deleted" = '-1'
                        AND a."Dispos" = '52'
                        AND DATE('2021-11-30') - DATE(j."AP_date") BETWEEN 0 AND 182
                
            ) z
                    GROUP BY z.issue_group,
                        z.issue_risk_level
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


def get_get_open_ap_by_groups_365():
    """Открытые планы мероприятий по группам 183-365 дней"""

    sql = '''
        SELECT z.issue_group AS issue_group,
            z.issue_risk_level AS issue_risk_level,
            count(*)
        FROM (

            SELECT a.*,
                        c."Language3" AS issue_group, 
                        e."Language3" AS issue_type,
                        g."Language3" AS issue_risk_level,
                        h."IDFld",
                        i.open_actplans,
                        DATE(j."AP_date") AS "AP_date",
                        DATE('2021-11-30') AS "Reporting_date",
                        DATE('2021-11-30') - DATE(j."AP_date") AS "duration"
                    FROM dashboard.issues a
                    LEFT JOIN dashboard.udfvalue b
                        ON a."FindGroup" = b."UDFValueID"
                    LEFT JOIN dashboard.languageaa c
                        ON b."LanguageID"::text = c."IDFld"::text
                            AND c."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.udfvalue d
                        ON a."FindType" = d."UDFValueID"
                    LEFT JOIN dashboard.languageaa e
                        ON d."LanguageID"::text = e."IDFld"::text
                            AND e."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.udfvalue f
                        ON a."FindRisk" = f."UDFValueID"
                    LEFT JOIN dashboard.languageaa g
                        ON f."LanguageID"::text = g."IDFld"::text
                            AND g."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.activities h
                        ON a."AuditID" = h."GuiIDFld"

                    LEFT JOIN (
                        SELECT "OrigID", count(*) AS open_actplans
                        FROM dashboard.actplans
                        WHERE "APADate" IS NULL
                            AND "APStatus" <> '61'
                            AND "Deleted" = '-1'
                        GROUP BY "OrigID"
                        ) i
                        ON a."IDFld" = i."OrigID"
                        
                    LEFT JOIN (
                        SELECT "Iss", min("AP_date") AS "AP_date"
                            FROM dashboard.ap_dates
                            GROUP BY "Iss"
                    ) j
                        ON a."Subject" = j."Iss"
                        
                    WHERE i.open_actplans IS NOT NULL
                        AND h."IDFld" <> '2021 Тест'
                        AND h."IDFld" <> '2021 Тест 2 - 1'
                        AND "Subject" IS NOT NULL
                        AND a."Deleted" = '-1'
                        AND a."Dispos" = '52'
                        AND DATE('2021-11-30') - DATE(j."AP_date") BETWEEN 183 AND 365
                
            ) z
                    GROUP BY z.issue_group,
                        z.issue_risk_level
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


def get_get_open_ap_by_groups_366():
    """Открытые планы мероприятий по группам более года"""

    sql = '''
        SELECT z.issue_group AS issue_group,
            z.issue_risk_level AS issue_risk_level,
            count(*)
        FROM (

            SELECT a.*,
                        c."Language3" AS issue_group, 
                        e."Language3" AS issue_type,
                        g."Language3" AS issue_risk_level,
                        h."IDFld",
                        i.open_actplans,
                        DATE(j."AP_date") AS "AP_date",
                        DATE('2021-11-30') AS "Reporting_date",
                        DATE('2021-11-30') - DATE(j."AP_date") AS "duration"
                    FROM dashboard.issues a
                    LEFT JOIN dashboard.udfvalue b
                        ON a."FindGroup" = b."UDFValueID"
                    LEFT JOIN dashboard.languageaa c
                        ON b."LanguageID"::text = c."IDFld"::text
                            AND c."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.udfvalue d
                        ON a."FindType" = d."UDFValueID"
                    LEFT JOIN dashboard.languageaa e
                        ON d."LanguageID"::text = e."IDFld"::text
                            AND e."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.udfvalue f
                        ON a."FindRisk" = f."UDFValueID"
                    LEFT JOIN dashboard.languageaa g
                        ON f."LanguageID"::text = g."IDFld"::text
                            AND g."Description" = 'UDF'
                            
                    LEFT JOIN dashboard.activities h
                        ON a."AuditID" = h."GuiIDFld"

                    LEFT JOIN (
                        SELECT "OrigID", count(*) AS open_actplans
                        FROM dashboard.actplans
                        WHERE "APADate" IS NULL
                            AND "APStatus" <> '61'
                            AND "Deleted" = '-1'
                        GROUP BY "OrigID"
                        ) i
                        ON a."IDFld" = i."OrigID"
                        
                    LEFT JOIN (
                        SELECT "Iss", min("AP_date") AS "AP_date"
                            FROM dashboard.ap_dates
                            GROUP BY "Iss"
                    ) j
                        ON a."Subject" = j."Iss"
                        
                    WHERE i.open_actplans IS NOT NULL
                        AND h."IDFld" <> '2021 Тест'
                        AND h."IDFld" <> '2021 Тест 2 - 1'
                        AND "Subject" IS NOT NULL
                        AND a."Deleted" = '-1'
                        AND a."Dispos" = '52'
                        AND DATE('2021-11-30') - DATE(j."AP_date") > 365
                
            ) z
                    GROUP BY z.issue_group,
                        z.issue_risk_level
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


def get_incoming_ap():
    """Входящие остатки по недостаткам"""

    sql = '''
        SELECT z.issue_risk_level,
            count(*)
        FROM (
        SELECT a.*,
            c."Language3" AS issue_group, 
            e."Language3" AS issue_type,
            g."Language3" AS issue_risk_level,
            h."IDFld",
            i.open_actplans
        FROM dashboard.issues a
        LEFT JOIN dashboard.udfvalue b
            ON a."FindGroup" = b."UDFValueID"
        LEFT JOIN dashboard.languageaa c
            ON b."LanguageID"::text = c."IDFld"::text
                AND c."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue d
            ON a."FindType" = d."UDFValueID"
        LEFT JOIN dashboard.languageaa e
            ON d."LanguageID"::text = e."IDFld"::text
                AND e."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue f
            ON a."FindRisk" = f."UDFValueID"
        LEFT JOIN dashboard.languageaa g
            ON f."LanguageID"::text = g."IDFld"::text
                AND g."Description" = 'UDF'
                
        LEFT JOIN dashboard.activities h
            ON a."AuditID" = h."GuiIDFld"

        LEFT JOIN (
            SELECT "OrigID", count(*) AS open_actplans
            FROM dashboard.actplans
            WHERE "APADate" IS NULL
                AND "APStatus" <> '61'
                AND "Deleted" = '-1'
            GROUP BY "OrigID"
            ) i
            ON a."IDFld" = i."OrigID"
            
        WHERE h."IDFld" <> '2021 Тест'
			AND h."IDFld" <> '2021 Тест 2 - 1'
			AND "Subject" IS NOT NULL
			AND h."IDFld" = '2021 Недостатки прошлых периодов (ранее 2021 года)'
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
        ) z
        GROUP BY z.issue_risk_level
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


def get_increase_ap():
    """Добавленные за период недостатки"""

    sql = '''
        SELECT z.issue_risk_level,
            count(*)
        FROM (
        SELECT a.*,
            c."Language3" AS issue_group, 
            e."Language3" AS issue_type,
            g."Language3" AS issue_risk_level,
            h."IDFld",
            i.open_actplans
        FROM dashboard.issues a
        LEFT JOIN dashboard.udfvalue b
            ON a."FindGroup" = b."UDFValueID"
        LEFT JOIN dashboard.languageaa c
            ON b."LanguageID"::text = c."IDFld"::text
                AND c."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue d
            ON a."FindType" = d."UDFValueID"
        LEFT JOIN dashboard.languageaa e
            ON d."LanguageID"::text = e."IDFld"::text
                AND e."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue f
            ON a."FindRisk" = f."UDFValueID"
        LEFT JOIN dashboard.languageaa g
            ON f."LanguageID"::text = g."IDFld"::text
                AND g."Description" = 'UDF'
                
        LEFT JOIN dashboard.activities h
            ON a."AuditID" = h."GuiIDFld"

        LEFT JOIN (
            SELECT "OrigID", count(*) AS open_actplans
            FROM dashboard.actplans
            WHERE "APADate" IS NULL
                AND "APStatus" <> '61'
                AND "Deleted" = '-1'
            GROUP BY "OrigID"
            ) i
            ON a."IDFld" = i."OrigID"
            
        WHERE h."IDFld" <> '2021 Тест'
			AND h."IDFld" <> '2021 Тест 2 - 1'
			AND "Subject" IS NOT NULL
			AND h."IDFld" <> '2021 Недостатки прошлых периодов (ранее 2021 года)'
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
        ) z
        GROUP BY z.issue_risk_level
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


def get_decrease_ap():
    """Закрытые за период недостатки"""

    sql = '''
        SELECT z.issue_risk_level,
            count(*)
        FROM (
        SELECT a.*,
            c."Language3" AS issue_group, 
            e."Language3" AS issue_type,
            g."Language3" AS issue_risk_level,
            h."IDFld",
            i.open_actplans
        FROM dashboard.issues a
        LEFT JOIN dashboard.udfvalue b
            ON a."FindGroup" = b."UDFValueID"
        LEFT JOIN dashboard.languageaa c
            ON b."LanguageID"::text = c."IDFld"::text
                AND c."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue d
            ON a."FindType" = d."UDFValueID"
        LEFT JOIN dashboard.languageaa e
            ON d."LanguageID"::text = e."IDFld"::text
                AND e."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue f
            ON a."FindRisk" = f."UDFValueID"
        LEFT JOIN dashboard.languageaa g
            ON f."LanguageID"::text = g."IDFld"::text
                AND g."Description" = 'UDF'
                
        LEFT JOIN dashboard.activities h
            ON a."AuditID" = h."GuiIDFld"

        LEFT JOIN (
            SELECT "OrigID", count(*) AS open_actplans
            FROM dashboard.actplans
            WHERE "APADate" IS NULL
                AND "APStatus" <> '61'
                AND "Deleted" = '-1'
            GROUP BY "OrigID"
            ) i
            ON a."IDFld" = i."OrigID"
            
        WHERE h."IDFld" <> '2021 Тест'
			AND h."IDFld" <> '2021 Тест 2 - 1'
			AND "Subject" IS NOT NULL
            AND i.open_actplans IS NULL
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
        ) z
        GROUP BY z.issue_risk_level
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


def get_outcoming_ap():
    """Исходящие остатки недостатков за период"""

    sql = '''
        SELECT z.issue_risk_level,
            count(*)
        FROM (
        SELECT a.*,
            c."Language3" AS issue_group, 
            e."Language3" AS issue_type,
            g."Language3" AS issue_risk_level,
            h."IDFld",
            i.open_actplans
        FROM dashboard.issues a
        LEFT JOIN dashboard.udfvalue b
            ON a."FindGroup" = b."UDFValueID"
        LEFT JOIN dashboard.languageaa c
            ON b."LanguageID"::text = c."IDFld"::text
                AND c."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue d
            ON a."FindType" = d."UDFValueID"
        LEFT JOIN dashboard.languageaa e
            ON d."LanguageID"::text = e."IDFld"::text
                AND e."Description" = 'UDF'
                
        LEFT JOIN dashboard.udfvalue f
            ON a."FindRisk" = f."UDFValueID"
        LEFT JOIN dashboard.languageaa g
            ON f."LanguageID"::text = g."IDFld"::text
                AND g."Description" = 'UDF'
                
        LEFT JOIN dashboard.activities h
            ON a."AuditID" = h."GuiIDFld"

        LEFT JOIN (
            SELECT "OrigID", count(*) AS open_actplans
            FROM dashboard.actplans
            WHERE "APADate" IS NULL
                AND "APStatus" <> '61'
                AND "Deleted" = '-1'
            GROUP BY "OrigID"
            ) i
            ON a."IDFld" = i."OrigID"
            
        WHERE h."IDFld" <> '2021 Тест'
			AND h."IDFld" <> '2021 Тест 2 - 1'
			AND "Subject" IS NOT NULL
            AND i.open_actplans IS NOT NULL
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
        ) z
        GROUP BY z.issue_risk_level
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


def get_high_ap_issues():
    """Недостатки и планы мероприятий с высоким уровнем риска"""

    sql = '''
        SELECT c."Language3" AS "Область риска",
            b."Subject" AS "Название недостатка",
            b."Finding" AS "Краткое описание недостатка",
            -- b."Recom" AS "Рекомендация",
            h."IDFld" AS "Аудит",
            a."open_actplans" AS "Количество открытых ПМ"
                    FROM dashboard.issues b
                        LEFT JOIN dashboard.activities h
                            ON b."AuditID" = h."GuiIDFld"
                        LEFT JOIN dashboard.udfvalue d
                            ON b."FindGroup" = d."UDFValueID"
                        LEFT JOIN dashboard.languageaa c
                            ON d."LanguageID"::text = c."IDFld"::text
                                AND c."Description" = 'UDF'
                        LEFT JOIN dashboard.udfvalue e
                            ON b."FindType" = e."UDFValueID"
                        LEFT JOIN dashboard.languageaa f
                            ON e."LanguageID"::text = f."IDFld"::text
                                AND f."Description" = 'UDF'
                        LEFT JOIN dashboard.udfvalue g
                            ON b."FindRisk" = g."UDFValueID"
                        LEFT JOIN dashboard.languageaa i
                            ON g."LanguageID"::text = i."IDFld"::text
                                AND i."Description" = 'UDF'
                        LEFT JOIN (
                            SELECT "OrigID", count(*) AS open_actplans
                            FROM dashboard.actplans
                            WHERE "APADate" IS NULL
                                AND "APStatus" <> '61'
                                AND "Deleted" = '-1'
                            GROUP BY "OrigID"
                            ) a
                            ON b."IDFld" = a."OrigID"
                    WHERE h."IDFld" <> '2021 Тест'
                        AND h."IDFld" <> '2021 Тест 2 - 1'
                        AND b."Subject" IS NOT NULL
                        AND b."Deleted" = '-1'
                        AND b."Dispos" = '52'
                        AND i."Language3" = 'Высокий'
                        AND a."open_actplans" IS NOT NULL
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    df1 = pd.read_sql(sql, con)

    return df1


# def get_ap_issues():
#     """Недостатки и планы мероприятий"""

#     sql = '''
#         SELECT b."Subject" AS "Issue_Subject",
#             b."Creator" AS "Issue_Creator",
#             b."CreateDate" AS "Issue_CreateDate",
#             b."Finding" AS "Issue_Finding",
#             b."Background" AS "Issue_Background",
#             b."FindGroup" AS "Issue_FindGroup",
#             b."FindType" AS "Issue_FindType",
#             b."Recom" AS "Issue_Recom",
#             a."Subject" AS "Ap_Subject",
#             a."Creator" AS "Ap_Creator",
#             a."APEDate" AS "Ap_APEDate",
#             a."APEDate_W" AS "Ap_APEDate_W",
#             a."APADate" AS "Ap_APADate",
#             a."APDate" AS "Ap_APDate",
#             a."APStatus" AS "Ap_APStatus",
#             a."Mresp" AS "Ap_Mresp"
#         FROM dashboard.actplans a 
#             LEFT JOIN dashboard.issues b
#                 ON a."OrigID" = b."IDFld"
#             LEFT JOIN dashboard.activities h
#             	ON b."AuditID" = h."GuiIDFld"
#         WHERE h."IDFld" <> '2021 Тест'
# 			AND h."IDFld" <> '2021 Тест 2 - 1'
# 			AND b."Subject" IS NOT NULL
#             AND b."Deleted" = '-1'
# 			AND b."Dispos" = '52'
#     '''

#     con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
#     df1 = pd.read_sql(sql, con)

#     return df1