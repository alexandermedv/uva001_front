"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
import front_ex.config as config
from sqlalchemy import create_engine


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
                        TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY') AS "Sent_to_Itrack",
                        DATE(j."AP_date") AS "AP_date",
                        DATE('2022-05-01') AS "Reporting_date",
                        CASE WHEN i."Sent_to_Itrack" IS NULL
						THEN DATE('2022-05-01') - DATE(j."AP_date")
						ELSE DATE('2022-05-01') - TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY')
						END AS "duration"
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
                        SELECT "OrigID", count(*) AS open_actplans, min("Sent_to_Itrack") AS "Sent_to_Itrack"
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
                        AND h."IDFld" <> '2022 Test'
                        AND "Subject" IS NOT NULL
                        AND a."Deleted" = '-1'
                        AND a."Dispos" = '52'
                        AND CASE WHEN i."Sent_to_Itrack" IS NULL
                            THEN DATE('2022-05-01') - DATE(j."AP_date")
                            ELSE DATE('2022-05-01') - TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY')
                            END < 182
                
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
                        TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY') AS "Sent_to_Itrack",
                        DATE(j."AP_date") AS "AP_date",
                        DATE('2022-05-01') AS "Reporting_date",
                        CASE WHEN i."Sent_to_Itrack" IS NULL
						THEN DATE('2022-05-01') - DATE(j."AP_date")
						ELSE DATE('2022-05-01') - TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY')
						END AS "duration"
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
                        SELECT "OrigID", count(*) AS open_actplans, min("Sent_to_Itrack") AS "Sent_to_Itrack"
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
                        AND h."IDFld" <> '2022 Test'
                        AND "Subject" IS NOT NULL
                        AND a."Deleted" = '-1'
                        AND a."Dispos" = '52'
                        AND CASE WHEN i."Sent_to_Itrack" IS NULL
						THEN DATE('2022-05-01') - DATE(j."AP_date")
						ELSE DATE('2022-05-01') - TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY')
						END BETWEEN 183 AND 365
                
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
                        TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY') AS "Sent_to_Itrack",
                        i."Close_date",
                        DATE(j."AP_date") AS "AP_date",
                        DATE('2022-05-01') AS "Reporting_date",
                        CASE WHEN i."Sent_to_Itrack" IS NULL
						THEN DATE('2022-05-01') - DATE(j."AP_date")
						ELSE DATE('2022-05-01') - TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY')
						END AS "duration"
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
                        SELECT "OrigID", 
                            count(*) AS open_actplans, 
                            min("Sent_to_Itrack") AS "Sent_to_Itrack",
                            max(TO_DATE(LEFT("APADate", 10), 'DD/MM/YYYY')) AS "Close_date"
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
                        AND h."IDFld" <> '2022 Test'
                        AND "Subject" IS NOT NULL
                        AND a."Deleted" = '-1'
                        AND a."Dispos" = '52'
                        AND (CASE WHEN i."Sent_to_Itrack" IS NULL
						THEN DATE('2022-05-01') - DATE(j."AP_date")
						ELSE DATE('2022-05-01') - TO_DATE(left(i."Sent_to_Itrack", 10), 'MM/DD/YYYY')
						END) > 365
                
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
            i.open_actplans,
            (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) AS "Sent_to_Itrack",
            k."Close_date"
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
            SELECT "OrigID", 
                count(*) AS open_actplans, 
                min("Sent_to_Itrack") AS "Sent_to_Itrack",
                max(TO_DATE(LEFT("APADate", 10), 'DD/MM/YYYY')) AS "Close_date"
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

        LEFT JOIN (
			SELECT "OrigID",
            min("Sent_to_Itrack") AS "Sent_to_Itrack",
			max(TO_DATE(LEFT("APADate", 10), 'MM/DD/YYYY')) AS "Close_date"
			FROM dashboard.actplans
            WHERE "Deleted" = '-1'
            GROUP BY "OrigID"
            ) k
			ON a."IDFld" = k."OrigID"
            
        WHERE h."IDFld" <> '2022 Test'
			AND "Subject" IS NOT NULL
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
            AND (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) < TO_DATE('20220401', 'YYYYMMDD')
            AND (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) IS NOT NULL
            AND NOT (k."Close_date" < TO_DATE('20220401', 'YYYYMMDD') AND i.open_actplans IS NULL)
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
            i.open_actplans,
			(CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) AS "Sent_to_Itrack",
            k."Close_date"
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
            SELECT "OrigID", count(*) AS open_actplans, min("Sent_to_Itrack") AS "Sent_to_Itrack"
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
							
		LEFT JOIN (
			SELECT "OrigID",
            min("Sent_to_Itrack") AS "Sent_to_Itrack",
			max(TO_DATE(LEFT("APADate", 10), 'MM/DD/YYYY')) AS "Close_date"
			FROM dashboard.actplans
            WHERE "Deleted" = '-1'
            GROUP BY "OrigID"
            ) k
			ON a."IDFld" = k."OrigID"
            
        WHERE h."IDFld" <> '2022 Test'
			AND "Subject" IS NOT NULL
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
            AND (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) IS NOT NULL
			AND (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) >= TO_DATE('20220401', 'YYYYMMDD')
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
            i.open_actplans,
			(CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) AS "Sent_to_Itrack",
            k."Close_date"
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
            SELECT "OrigID", count(*) AS open_actplans, min("Sent_to_Itrack") AS "Sent_to_Itrack"
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
							
		LEFT JOIN (
			SELECT "OrigID",
            min("Sent_to_Itrack") AS "Sent_to_Itrack",
			max(TO_DATE(LEFT("APADate", 10), 'MM/DD/YYYY')) AS "Close_date"
			FROM dashboard.actplans
            WHERE "Deleted" = '-1'
            GROUP BY "OrigID"
            ) k
			ON a."IDFld" = k."OrigID"
            
        WHERE h."IDFld" <> '2022 Test'
			AND "Subject" IS NOT NULL
            AND i.open_actplans IS NULL
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
            AND (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) IS NOT NULL
			AND k."Close_date" >= TO_DATE('20220401', 'YYYYMMDD')
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
            i.open_actplans,
            (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) AS "Sent_to_Itrack",
            k."Close_date"
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
            SELECT "OrigID", 
                count(*) AS open_actplans, 
                min("Sent_to_Itrack") AS "Sent_to_Itrack",
                max(TO_DATE(LEFT("APADate", 10), 'DD/MM/YYYY')) AS "Close_date"
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

        LEFT JOIN (
			SELECT "OrigID",
            min("Sent_to_Itrack") AS "Sent_to_Itrack",
			max(TO_DATE(LEFT("APADate", 10), 'MM/DD/YYYY')) AS "Close_date"
			FROM dashboard.actplans
            WHERE "Deleted" = '-1'
            GROUP BY "OrigID"
            ) k
			ON a."IDFld" = k."OrigID"
            
        WHERE h."IDFld" <> '2022 Test'
			AND "Subject" IS NOT NULL
            AND a."Deleted" = '-1'
			AND a."Dispos" = '52'
            AND i.open_actplans IS NOT NULL
            AND (CASE WHEN j."AP_date" IS NOT NULL
							THEN j."AP_date"
							ELSE TO_DATE(left(k."Sent_to_Itrack", 10), 'MM/DD/YYYY')
							END) IS NOT NULL
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
                    WHERE h."IDFld" <> '2022 Test'
                        AND b."Subject" IS NOT NULL
                        AND b."Deleted" = '-1'
                        AND b."Dispos" = '52'
                        AND i."Language3" = 'Высокий'
                        AND a."open_actplans" IS NOT NULL
    '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
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
            AND j."APCmt" IS NOT NULL -- Убрать эту строчку
            '''

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
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

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
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

    con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
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