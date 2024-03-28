"""Выгрузка данных и вспомогательные функции"""
import os
from sqlalchemy import create_engine
import pandas as pd
from datetime import date
from dash import html, dcc

# Переменные
min_date = date(2020,1,1)
max_date = date.today()
flag_posr = 0.8
flag_gruz = 0.8
flag_profit = 0.8

# Таблица по клиентам
def get_clients_df(client=None):
    """Таблица по клиентам"""
    if client is None:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Холдинг клиента",
                    "ИНН клиента",
                    "ОГРН клиента",
                    "Дата регистрации клиента",
                    "ОКВЭД",
                    "Кол-во рейсов ТМ",
                    "Доля посредничества",
                    "Изменение доли основного груза",
                    "Разных грузов у клиента",
                    "Последний фин период", 
                    CASE WHEN "Выручка посл фин период" = 'Нет данных' THEN null
			            ELSE "Выручка посл фин период"::bigint END AS "Выручка посл фин период",
                    "ДО: Доходность",
                    "СХ: Доходность",
                    "Кол-во рейсов" AS "ДО: Кол-во рейсов",
                    "Кол-во груженых рейсов" AS "ДО: Кол-во груженых рейсов",
                    "ДО миним",
                    "ДО критичн",
                    "ДО норматив",
                    "ДО целев",
                    "Доля низкодоходности",
                    "Доля критичнодоходности"
            FROM dashboard.credibility_uru
        '''
        # print(os.environ['POSTGRE_URL_DASH'], flush = True)
        df_clients = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH']))
        
        df_clients['Флаги'] = ''
        df_clients.loc[df_clients['Доля посредничества']>=flag_posr, 'Флаги'] += '⭐'
        df_clients.loc[df_clients['Изменение доли основного груза']>=flag_gruz, 'Флаги'] += '🚚'
        df_clients.loc[df_clients['Доля критичнодоходности']>=flag_profit, 'Флаги'] += '💰'
        df_clients = df_clients.sort_values(by=['Флаги', 'Кол-во рейсов ТМ'], ascending=False).reset_index(drop=True)
        #df_clients = df_clients.sort_values(by=['Доля посредничества', 'Холдинг клиента'], ascending=False).reset_index(drop=True)
        # Это индексирование нужно для того чтобы в dash можно было выбирать строку
        df_clients['id'] = df_clients.index
        return df_clients
    else:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Холдинг клиента",
                    "ИНН клиента",
                    "ОГРН клиента",
                    "Дата регистрации клиента",
                    "ОКВЭД",
                    "Кол-во рейсов ТМ",
                    "Доля посредничества",
                    "Изменение доли основного груза",
                    "Разных грузов у клиента",
                    "Последний фин период", 
			        "Выручка посл фин период",
                    "ДО: Доходность",
                    "СХ: Доходность",
                    "Кол-во рейсов" AS "ДО: Кол-во рейсов",
                    "Кол-во груженых рейсов" AS "ДО: Кол-во груженых рейсов",
                    "ДО миним",
                    "ДО критичн",
                    "ДО норматив",
                    "ДО целев",
                    "Доля низкодоходности",
                    "Доля критичнодоходности"
            FROM dashboard.credibility_uru
            WHERE "Клиент" = '%s'
        ''' % (client)
        df_client = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
        return df_client

# Таблица по грузам
def get_gruzes_df(client=None):
    if client is None:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Код груза",
                    "Наименование груза",
                    "Рейсов 2020",
                    "Рейсов 2021",
                    "Рейсов 2022",
                    "Рейсов 2023",
                    "Рейсов 2024"
            FROM dashboard.credibility_gruz_changes_uru
        '''
        return "Выберите клиента"
    else:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Код груза",
                    "Наименование груза",
                    "Рейсов 2020",
                    "Рейсов 2021",
                    "Рейсов 2022",
                    "Рейсов 2023",
                    "Рейсов 2024"
            FROM dashboard.credibility_gruz_changes_uru
            WHERE "Клиент" = '%s'
        ''' % (client)
        return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))

def get_go_rating(client):
    sql2 = '''
        SELECT "Грузоотправитель",
                "Грузоотправитель имя",
                "Договор",
                "Сумма продаж ГО у клиента",
                "Доля ГО у клиента",
                "Результат анализа",
                "Метрика посредничества"
        FROM dashboard.credibility_posrednics_go_rating_uru е
        WHERE "Клиент" = '%s'
        ORDER BY "Доля ГО у клиента" DESC
    ''' % (client)
    return pd.read_sql(sql2, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))

# # Фильтры
# date_filter = dbc.FormGroup([
#     dbc.Label("Период", html_for="date_filter"),
#     dcc.DatePickerRange(
#         id="date_filter",
#         start_date=date(2020,1,1),
#         end_date=date.today(),
#         display_format='D MMM YYYY'
#     )
# ])