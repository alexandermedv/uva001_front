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
        FROM dashboard.resellers_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
                    AND "Название груза ЕТСНГ" IN %s
                    AND "Род подвижного состава" IN %s
                    AND "Результат анализа" = 'Посредник'
        ORDER BY "Наименование филиала" ASC
    ''' % (start_date, end_date, gruz, rod)

    # return pd.read_sql(sql, con=engine_cons)
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


# Значения полного списка групп грузов
def get_all_cargo_names(start_date, end_date):
    """Выгрузка групп грузов"""
    sql = '''
        SELECT DISTINCT "Название груза ЕТСНГ"
        FROM dashboard.resellers_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        ORDER BY "Название груза ЕТСНГ" ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


# Значения полного списка РПС
def get_all_rps(start_date, end_date):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT "Род подвижного состава"
        FROM dashboard.resellers_cube
        WHERE TO_DATE("Дата раскредитования", 'YYYYMMDD') BETWEEN '%s' AND '%s'
        ORDER BY "Род подвижного состава" ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


# Максимальная дата в выгрузке
def get_max_date():
    """Максимальная дата в выгрузке"""
    sql = '''
    SELECT MAX(TO_DATE("Дата раскредитования", 'YYYYMMDD'))
    FROM dashboard.resellers_cube
    '''
    # return engine_cons.execute(sql).fetchone()[0]
    con = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
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

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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
    df1 = pd.read_sql(sql1, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
    df2 = pd.read_sql(sql2, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))

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

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))


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
        FROM dashboard.resellers_cube
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
                FROM dashboard.resellers_cube
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

    # sql2 = '''
    #     SELECT a."Дата",
        #     a."Начало недели",
        #     a."Начало месяца",
        #     a."Количество рейсов" AS "Количество посред рейсов",
        #     a."Стоимость" AS "Стоимость посред рейсов",
        #     b."Количество рейсов" AS "Количество рейсов",
        #     b."Стоимость" AS "Стоимость рейсов",
        #     round(a."Количество рейсов"/b."Количество рейсов"*100, 2) AS "Доля посред рейсов в шт",
        #     round(a."Стоимость"::numeric/b."Стоимость"::numeric*100, 2) AS "Доля посред рейсов в руб" 
        # FROM (
        # (SELECT TO_DATE("Дата раскредитования",'YYYYMMDD') AS "Дата",
        #     (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube) + 
        #     (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7 AS "Начало недели",
        #     date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
        #     sum("Количество рейсов") AS "Количество рейсов",
        #     round(sum("Стоимость")) AS "Стоимость"
        # FROM dashboard.resellers_cube
        # WHERE "Результат анализа" = 'Посредник'
        # GROUP BY TO_DATE("Дата раскредитования",'YYYYMMDD'),
        #     (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7,
        #     date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
        # ORDER BY TO_DATE("Дата раскредитования",'YYYYMMDD') DESC) a
        #     LEFT JOIN (
        #         SELECT TO_DATE("Дата раскредитования",'YYYYMMDD') AS "Дата",
        #             (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube) + 
        #             (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7 AS "Начало недели",
        #             date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD'))) AS "Начало месяца",
        #             sum("Количество рейсов") AS "Количество рейсов",
        #             round(sum("Стоимость")) AS "Стоимость"
        #         FROM dashboard.resellers_cube
        #         GROUP BY TO_DATE("Дата раскредитования",'YYYYMMDD'),
        #             (TO_DATE("Дата раскредитования",'YYYYMMDD') - (SELECT min(TO_DATE("Дата раскредитования",'YYYYMMDD')) FROM dashboard.resellers_cube))/7*7,
        #             date(date_trunc('month', TO_DATE("Дата раскредитования",'YYYYMMDD')))
        #         ORDER BY TO_DATE("Дата раскредитования",'YYYYMMDD') DESC
        #     ) b
        #     ON a."Дата" = b."Дата"
        # )
    # '''

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
