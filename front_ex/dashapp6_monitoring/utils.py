"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
# import front_ex.config as config
from sqlalchemy import create_engine, text

def get_issues_large_sql(start_date, end_date):
    
    issues_large = f'''
        SELECT 
            a."IDFld",
            a."CreateDate",
            a."Creator",
            a."Subject" AS "Тема наблюдения",
            a."Finding" AS "Краткий текст наблюдения",
            a."Background" AS "Подробный текст наблюдения",
            a."Dispos" AS "Диспозиция наблюдения",
            a."Recom" AS "Рекомендация",
            a."FindType" AS "Тип наблюдения",
            e."Language3" AS "Текст типа наблюдения",
            a."FindGroup" AS "Группа наблюдения",
            c."Language3" AS "Текст группы наблюдения",
            a."FindRisk" AS "Уровень риска",
            g."Language3" AS "issue_risk_level",
            a."Deleted" AS "Статус удаления наблюдения",
            a."History" AS "История наблюдения",
            a."Status" AS "Статус наблюдения",
            a."AprvLevel" AS "Одобрение наблюдения",
            a."AuditID" AS "ID аудита",
            h."IDFld" AS "ActName",
            h."FiscalYear" AS "Год аудита",
            i.open_actplans "Количество открытых ПМ на начало",
            ii.open_actplans "Количество открытых ПМ на конец",
            TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') AS "Дата согласования ГД",
            CASE WHEN ii.open_actplans IS NULL THEN k."Close_date"
                    ELSE NULL
                    END AS "Дата закрытия недостатка",
            CASE WHEN EXTRACT(YEAR FROM TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY')) = h."FiscalYear"
                THEN TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY')
                ELSE TO_DATE(h."FiscalYear"::text||'1231', 'YYYYMMDD')
                END AS "Дата недостатка", -- С подменой даты
            TO_DATE('{end_date}', 'YYYY-MM-DD') - TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') AS "Длительность"
                -- Наблюдения
                FROM dashboard.issues a
                -- Присоединяем группу наблюдения
                LEFT JOIN dashboard.udfvalue b
                    ON a."FindGroup" = b."UDFValueID"
                -- Присоединяем название группы наблюдения
                LEFT JOIN dashboard.languageaa c
                    ON b."LanguageID"::text = c."IDFld"::text
                        AND c."Description" = 'UDF'
                -- Присоединяем тип наблюдения
                LEFT JOIN dashboard.udfvalue d
                    ON a."FindType" = d."UDFValueID"
                -- Присоединяем название типа наблюдения
                LEFT JOIN dashboard.languageaa e
                    ON d."LanguageID"::text = e."IDFld"::text
                        AND e."Description" = 'UDF'
                -- Присоединяем уровень риска
                LEFT JOIN dashboard.udfvalue f
                    ON a."FindRisk" = f."UDFValueID"
                -- Присоединяем текст уровня риска
                LEFT JOIN dashboard.languageaa g
                    ON f."LanguageID"::text = g."IDFld"::text
                        AND g."Description" = 'UDF'
                -- Присоединяем аудиты
                LEFT JOIN dashboard.activities h
                    ON a."AuditID" = h."GuiIDFld"
                -- Количество открытых ПМ на start_date, дата согласования ГД
                LEFT JOIN (
                    SELECT "OrigID", count(*) AS open_actplans, 
                        min(bb."ActlDate6") AS "ActlDate6"
                    FROM dashboard.actplans aa
                    LEFT JOIN dashboard.overview bb
                        ON aa."AuditID" = bb."IDFld"
                    WHERE 1=1
                        AND ("APADate" IS NULL OR TO_DATE(LEFT("APADate", 10), 'MM/DD/YYYY') > TO_DATE('{start_date}', 'YYYY-MM-DD'))
                        --AND "APStatus" <> '61'
                        AND aa."Deleted" = '-1'
                        AND ("ActlDate6" IS NOT NULL AND TO_DATE(left("ActlDate6", 10), 'MM/DD/YYYY') <= TO_DATE('{start_date}', 'YYYY-MM-DD'))
                    GROUP BY "OrigID"
                    ) i
                    ON a."IDFld" = i."OrigID"
                -- Количество открытых ПМ на end_date, дата согласования ГД
                LEFT JOIN (
                    SELECT "OrigID", count(*) AS open_actplans, 
                        min(bb."ActlDate6") AS "ActlDate6"
                    FROM dashboard.actplans aa
                    LEFT JOIN dashboard.overview bb
                        ON aa."AuditID" = bb."IDFld"
                    WHERE 1=1
                        AND ("APADate" IS NULL OR TO_DATE(LEFT("APADate", 10), 'MM/DD/YYYY') > TO_DATE('{end_date}', 'YYYY-MM-DD'))
                        --AND "APStatus" <> '61'
                        AND aa."Deleted" = '-1'
                        AND ("ActlDate6" IS NOT NULL AND TO_DATE(left("ActlDate6", 10), 'MM/DD/YYYY') <= TO_DATE('{end_date}', 'YYYY-MM-DD'))
                    GROUP BY "OrigID"
                    ) ii
                    ON a."IDFld" = ii."OrigID"
                -- Дата появления и дата закрытия недостатка          
                LEFT JOIN (
                    SELECT "OrigID",
                    min(bb."ActlDate6") AS "ActlDate6",
                    max(TO_DATE(LEFT("APADate", 10), 'MM/DD/YYYY')) AS "Close_date"
                    FROM dashboard.actplans aa
                    LEFT JOIN dashboard.overview bb
                        ON aa."AuditID" = bb."IDFld"
                    WHERE aa."Deleted" = '-1'
                    GROUP BY "OrigID"
                    ) k
                    ON a."IDFld" = k."OrigID"
    '''
	
    return issues_large

def get_open_ap_by_groups_182(start_date, end_date):
	"""Открытые планы мероприятий по группам 0-182 дня"""

	sql = f'''
			SELECT z."ActName" AS actname,
			z.issue_risk_level AS issue_risk_level,
			count(*)
		FROM (
                {get_issues_large_sql(start_date, end_date)}                
                WHERE h."IDFld" <> '2023 Проверка доступности сервиса IssueTrack'
                    AND "Subject" IS NOT NULL
                    AND a."Deleted" = '-1'
                    AND a."Dispos" = '52'
                    AND k."ActlDate6" IS NOT NULL
                    AND TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') IS NOT NULL
                    AND ii.open_actplans IS NOT NULL
					AND TO_DATE('{end_date}', 'YYYY-MM-DD') - TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') <= 182
			) z
					GROUP BY z."ActName",
						z.issue_risk_level
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_open_ap_by_groups_365(start_date, end_date):
	"""Открытые планы мероприятий по группам 183-365 дней"""

	sql = f'''
			SELECT z."ActName" AS actname,
			z.issue_risk_level AS issue_risk_level,
			count(*)
		FROM (
                {get_issues_large_sql(start_date, end_date)}                
                WHERE h."IDFld" <> '2023 Проверка доступности сервиса IssueTrack'
                    AND "Subject" IS NOT NULL
                    AND a."Deleted" = '-1'
                    AND a."Dispos" = '52'
                    AND k."ActlDate6" IS NOT NULL
                    AND TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') IS NOT NULL
                    AND ii.open_actplans IS NOT NULL
					AND TO_DATE('{end_date}', 'YYYY-MM-DD') - TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') BETWEEN 183 AND 365
			) z
					GROUP BY z."ActName",
						z.issue_risk_level
	    '''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_open_ap_by_groups_366(start_date, end_date):
	"""Открытые планы мероприятий по группам более года"""

	sql = f'''
			SELECT z."ActName" AS actname,
			z.issue_risk_level AS issue_risk_level,
			count(*)
		FROM (
                {get_issues_large_sql(start_date, end_date)}                
                WHERE h."IDFld" <> '2023 Проверка доступности сервиса IssueTrack'
                    AND "Subject" IS NOT NULL
                    AND a."Deleted" = '-1'
                    AND a."Dispos" = '52'
                    AND k."ActlDate6" IS NOT NULL
                    AND TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') IS NOT NULL
                    AND ii.open_actplans IS NOT NULL
					AND TO_DATE('{end_date}', 'YYYY-MM-DD') - TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') > 365
			) z
					GROUP BY z."ActName",
						z.issue_risk_level
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_incoming_ap(start_date, end_date):
	"""Входящие остатки по недостаткам"""

	sql = f'''
		SELECT z.issue_risk_level,
			count(*)
		FROM (
			{get_issues_large_sql(start_date, end_date)}                
            WHERE h."IDFld" <> '2023 Проверка доступности сервиса IssueTrack'
                AND "Subject" IS NOT NULL
                AND a."Deleted" = '-1'
                AND a."Dispos" = '52'
                AND k."ActlDate6" IS NOT NULL
                --AND TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') IS NOT NULL
                AND i.open_actplans IS NOT NULL
			) z
		GROUP BY z.issue_risk_level
	'''
	print('incoming =', sql)

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_increase_ap(start_date, end_date):
	"""Добавленные за период недостатки"""

	sql = f'''
		SELECT z.issue_risk_level,
			count(*)
		FROM (
			{get_issues_large_sql(start_date, end_date)} 
				
			WHERE h."IDFld" <> '2023 Проверка доступности сервиса IssueTrack'
				AND "Subject" IS NOT NULL
				AND a."Deleted" = '-1'
				AND a."Dispos" = '52'
				AND TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') IS NOT NULL
				AND TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
			) z
		GROUP BY z.issue_risk_level
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_decrease_ap(start_date, end_date):
	"""Закрытые за период недостатки"""

	sql = f'''
		SELECT z.issue_risk_level,
			count(*)
		FROM (
			{get_issues_large_sql(start_date, end_date)} 
				
			WHERE h."IDFld" <> '2023 Проверка доступности сервиса IssueTrack'
				AND "Subject" IS NOT NULL
				AND a."Deleted" = '-1'
				AND a."Dispos" = '52'
				AND CASE WHEN ii.open_actplans IS NULL THEN k."Close_date"
                    ELSE NULL
                    END IS NOT NULL
				AND CASE WHEN ii.open_actplans IS NULL THEN GREATEST(k."Close_date", TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY'))
                    ELSE NULL
                    END BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
				AND k."ActlDate6" IS NOT NULL
				
			) z
		GROUP BY z.issue_risk_level
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_outcoming_ap(start_date, end_date):
	"""Исходящие остатки недостатков за период"""

	sql = f'''
		SELECT z.issue_risk_level,
			count(*)
		FROM (
			{get_issues_large_sql(start_date, end_date)}                
            WHERE h."IDFld" <> '2023 Проверка доступности сервиса IssueTrack'
                AND "Subject" IS NOT NULL
                AND a."Deleted" = '-1'
                AND a."Dispos" = '52'
                AND k."ActlDate6" IS NOT NULL
                AND TO_DATE(left(k."ActlDate6", 10), 'MM/DD/YYYY') IS NOT NULL
                AND ii.open_actplans IS NOT NULL
			) z
		GROUP BY z.issue_risk_level
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
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
					WHERE h."IDFld" <> '2022 Test'
						AND b."Subject" IS NOT NULL
						AND b."Deleted" = '-1'
						AND b."Dispos" = '52'
						AND i."Language3" = 'Высокий'
						AND a."open_actplans" IS NOT NULL
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_actplans():
	"""Планы мероприятий для таблицы"""

	sql = '''
		SELECT 
			"ActName" AS "Название аудита",
			"Subject" AS "Мероприятие",
			"Finding" AS "Описание недостатка (кратк)",
			"Background" AS "Описание недостатка (детальн)",
			"issue_risk_level" AS "Уровень критичности недостатка",
			"Recom" AS "Рекомендации",
			"Mresp" AS "Комментарии",
			"Creator" AS "Отв аудитор",
			"employee" AS "Координатор от бизнес-подразделения", 
			"APEDate" AS "Ожидаемая дата выполнения",
			"APREDate" AS "Пересмотренная дата выполнения",
			"reviewer" AS "ЗГД",
			"APCmtHst" AS "История комментариев"
		FROM dashboard.issues_actplans
		WHERE 
			"APADate" IS NULL
			AND "APStatus" <> '61'
			AND "Deleted" = '-1'
			'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_delayed_actplans():
	"""Отложенные планы мероприятий"""

	sql = '''
		SELECT a."Finding" AS "Описание недостатка",
			j."Subject" AS "Мероприятие",
			j."APEDate" AS "Первоначальная дата окончания",
			j."APREDate" AS "Пересмотренная дата окончания",
			j."APCmt" AS "Комментарий"
			
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
							LEFT JOIN dashboard.actplans j
								ON j."OrigID" = a."IDFld"
		WHERE g."Language3" = 'Высокий'
			AND i.open_actplans IS NOT NULL
			AND j."APREDate" IS NOT NULL
			AND j."APADate" IS NULL
			AND j."APCmt" IS NOT NULL -- Убрать эту строчку
			'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_manual_table1():
	"""Ручная таблица 1"""

	sql = '''
		SELECT "Область риска",
			"Описание недостатка",
			"Длительность устранения план/факт, мес.",
			"Срок завершения мероприятий",
			"Статус",
			"Причины длительного устранения"
		FROM dashboard.aa_manual_table1
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_manual_table2():
	"""Ручная таблица 2"""

	sql = '''
		SELECT "Область риска",
			"Описание недостатка",
			"Уровень значимости",
			"Длительность устранения план/факт"
		FROM dashboard.aa_manual_table2
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


def get_manual_table3():
	"""Ручная таблица 3"""

	sql = '''
		SELECT "Область риска",
			"Описание недостатка",
			"Уровень значимости",
			"Длительность устранения план/факт",
			"Статус"
		FROM dashboard.aa_manual_table3
	'''

	con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	df1 = pd.read_sql(sql, con)

	return df1


# Максимальная дата в выгрузке
def get_max_date():
	"""Максимальная дата в выгрузке"""
	sql = '''
	SELECT MAX(TO_DATE("Дата ввода", 'YYYYMMDD'))
	FROM dashboard.osv_94
	'''
	# return engine_cons.execute(sql).fetchone()[0]
	engine = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
	with engine.connect() as con:
		result = con.execute(text(sql)).fetchone()[0]

	return result


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

#     con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
#     df1 = pd.read_sql(sql, con)

#     return df1