"""Выгрузка данных и вспомогательные функции"""
import os
import datetime as dt
import pandas as pd
from sqlalchemy import create_engine


# Выгрузка непроведенных операций выбраковки
def get_defect(start_date,  end_date):
    """Выгрузка непроведенных операций выбраковки"""
    sql = '''
        SELECT *
        FROM udv.details_defect a
        LEFT JOIN udv.view_details_reports_defect_details b
        ON a.details_defect_id = b.details_defect_id
        WHERE defect_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Количество непроведенных операций выбраковки
def get_defect_count(start_date,  end_date):
    """Количество непроведенных операций выбраковки"""

    sql = '''
        SELECT count(*)
        FROM udv.details_defect a
        LEFT JOIN udv.view_details_reports_defect_details b
        ON a.details_defect_id = b.details_defect_id
        WHERE defect_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)
    print(sql)
    con = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]

def get_defect_dynamics(start_date,  end_date):
    """Динамика непроведенных операций выбраковки"""

    sql = """

    """ % (start_date,  end_date, end_date)

# Выгрузка непроведенных операций пересылки
def get_transfer(start_date,  end_date):
    """Выгрузка непроведенных операций выбраковки"""
    sql = '''
        SELECT *,
        date_part('day', TO_DATE('20220802', 'YYYYMMDD') - transfer_date),
        date_part('day', accept_date - TO_DATE('20220815', 'YYYYMMDD'))
        FROM udv.details_transfer a
        left join udv.view_details_reports_transfer_details b
        ON a.details_transfer_id = b.details_transfer_id
        WHERE transfer_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Количество непроведенных операций пересылки
def get_transfer_count(start_date,  end_date):
    """Количество непроведенных операций пересылки"""

    sql = '''
        SELECT count(*)
        FROM udv.details_transfer a
        left join udv.view_details_reports_transfer_details b
        ON a.details_transfer_id = b.details_transfer_id
        WHERE transfer_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)
    print(sql)
    con = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]

# Выгрузка непроведенных операций ремонта
def get_repair(start_date,  end_date):
    """Выгрузка непроведенных операций ремонта"""
    sql = '''
        SELECT *,
        date_part('day', TO_DATE('20220802', 'YYYYMMDD') - rem_act_date),
        date_part('day', accept_date - TO_DATE('20220815', 'YYYYMMDD'))
        FROM udv.details_repair a
        left join udv.view_details_reports_repair_details b
        on a.details_rapair_id = b.details_repair_id
        WHERE rem_act_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Количество непроведенных операций ремонта
def get_repair_count(start_date,  end_date):
    """Количество непроведенных операций ремонта"""

    sql = '''
        SELECT count(*)
        FROM udv.details_repair a
        left join udv.view_details_reports_repair_details b
        on a.details_rapair_id = b.details_repair_id
        WHERE rem_act_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)
    print(sql)
    con = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]

# Выгрузка непроведенных операций реализации
def get_sale(start_date,  end_date):
    """Выгрузка непроведенных операций реализации"""
    sql = '''
        SELECT *,
        date_part('day', TO_DATE('20220802', 'YYYYMMDD') - sale_date),
        date_part('day', accept_date - TO_DATE('20220815', 'YYYYMMDD'))
        FROM udv.details_sale a
        LEFT JOIN udv.view_details_reports_sale_details b
        ON a.details_sale_id = b.details_sale_id
        WHERE sale_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Количество непроведенных операций реализации
def get_sale_count(start_date,  end_date):
    """Количество непроведенных операций реализации"""

    sql = '''
        SELECT count(*)
        FROM udv.details_sale a
        LEFT JOIN udv.view_details_reports_sale_details b
        ON a.details_sale_id = b.details_sale_id
        WHERE sale_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
        ''' % (start_date,  end_date, end_date)

    con = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]


# Сводные результаты нагона
def get_nagon_results(start_date, end_date):
    """Сводные результаты нагона"""

    sql = '''
        SELECT 'Выбраковка' AS "operation",
    date_part('year', defect_date)::int AS "year",
    filial_id AS "filial",
    c.filial_short_name AS "filial_name",
    count(*)::bigint AS "oper_accepted_count",
    avg("oper_count")::bigint AS "oper_count",
    round(count(*)/avg("oper_count"), 2) AS "percentage"
FROM udv.details_defect a
        LEFT JOIN udv.view_details_reports_defect_details b
        ON a.details_defect_id = b.details_defect_id
        LEFT JOIN udv.nsi_org_filial c
        ON a.filial_id = c.nsi_org_filial_id
        
        LEFT JOIN (
            SELECT 'Выбраковка' AS "operation",
            date_part('year', defect_date) AS "year",
            filial_id AS "filial",
            c.filial_short_name AS "filial_name",
            count(*) AS "oper_count"
        FROM udv.details_defect a
                LEFT JOIN udv.view_details_reports_defect_details b
                ON a.details_defect_id = b.details_defect_id
                LEFT JOIN udv.nsi_org_filial c
                ON a.filial_id = c.nsi_org_filial_id
                WHERE defect_date between '%s' and '%s'
                    AND filial_id NOT IN ('30', '32', '34')
        GROUP BY date_part('year', defect_date),
                filial_id,
                c.filial_short_name) x
        ON date_part('year', a.defect_date) = x."year"
        AND a.filial_id = x."filial"
        AND c.filial_short_name = x."filial_name" 
        WHERE defect_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
            AND filial_id NOT IN ('30', '32', '34')
        GROUP BY date_part('year', defect_date),
                filial_id,
                c.filial_short_name
            
        UNION 
        SELECT 'Пересылка' AS "operation",
                date_part('year', transfer_date)::int AS "year",
                filial_id AS "filial",
                c.filial_short_name AS "filial_name",
                count(*)::bigint AS "oper_accepted_count",
                avg("oper_count")::bigint AS "oper_count",
                round(count(*)/avg("oper_count"), 2) AS "percentage"
        FROM udv.details_transfer a
                left join udv.view_details_reports_transfer_details b
                ON a.details_transfer_id = b.details_transfer_id
                LEFT JOIN udv.nsi_org_filial c
                ON a.filial_id = c.nsi_org_filial_id
                LEFT JOIN (
                    SELECT 'Пересылка' AS "operation",
                    date_part('year', transfer_date) AS "year",
                    filial_id AS "filial",
                    c.filial_short_name AS "filial_name",
                    count(*) AS "oper_count"
                FROM udv.details_transfer a
                        LEFT JOIN udv.view_details_reports_transfer_details b
                        ON a.details_transfer_id = b.details_transfer_id
                        LEFT JOIN udv.nsi_org_filial c
                        ON a.filial_id = c.nsi_org_filial_id
                        WHERE transfer_date between '%s' and '%s'
                            AND filial_id NOT IN ('30', '32', '34')
                GROUP BY date_part('year', transfer_date),
                        filial_id,
                        c.filial_short_name) x
                ON date_part('year', a.transfer_date) = x."year"
                AND a.filial_id = x."filial"
                AND c.filial_short_name = x."filial_name"
        WHERE transfer_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
            AND filial_id NOT IN ('30', '32', '34')
        GROUP BY date_part('year', transfer_date),
                filial_id,
                c.filial_short_name

        UNION
        SELECT 'Расход в ремонт вагонов' AS "operation",
                date_part('year', rem_act_date)::int AS "year",
                filial_id AS "filial",
                c.filial_short_name AS "filial_name",
                count(*)::bigint AS "oper_accepted_count",
                avg("oper_count")::bigint AS "oper_count",
                round(count(*)/avg("oper_count"), 2) AS "percentage"
        FROM udv.details_repair a
                left join udv.view_details_reports_repair_details b
                ON a.details_rapair_id = b.details_repair_id
                LEFT JOIN udv.nsi_org_filial c
                ON a.filial_id = c.nsi_org_filial_id
                LEFT JOIN (
                    SELECT 'Расход в ремонт вагонов' AS "operation",
                    date_part('year', rem_act_date) AS "year",
                    filial_id AS "filial",
                    c.filial_short_name AS "filial_name",
                    count(*) AS "oper_count"
                FROM udv.details_repair a
                        LEFT JOIN udv.view_details_reports_repair_details b
                        ON a.details_rapair_id = b.details_repair_id
                        LEFT JOIN udv.nsi_org_filial c
                        ON a.filial_id = c.nsi_org_filial_id
                        WHERE rem_act_date between '%s' and '%s'
                            AND filial_id NOT IN ('30', '32', '34')
                GROUP BY date_part('year', rem_act_date),
                        filial_id,
                        c.filial_short_name) x
                ON date_part('year', a.rem_act_date) = x."year"
                AND a.filial_id = x."filial"
                AND c.filial_short_name = x."filial_name"
        WHERE rem_act_date between '%s' and '%s'
            AND (accept_date > '%s' OR accept_date is null)
            AND filial_id NOT IN ('30', '32', '34')
        GROUP BY date_part('year', rem_act_date),
                filial_id,
                c.filial_short_name
        ''' % (start_date,  end_date, start_date, end_date, end_date, start_date,  end_date, start_date, end_date, end_date, start_date,  end_date, start_date, end_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))



# Выгрузка динамики по нагону
def get_nagon_dynamics(start_date, end_date):
    """Выгрузка динамики по нагону"""

    start_date = start_date.replace(day=1)
    end_date = end_date.replace(day=1)

    sql = '''
        SELECT *
        FROM udv.nagon_dynamics_months
        WHERE start_date = '%s'
            AND end_date between '%s' AND '%s'
        ''' % (start_date, start_date,  end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))



# Выгрузка оборота и количества операций по счету 94* за выбранный период
def get_osv_detail_by_dates(start_date, end_date, debug = False):
    """Выгрузка недостач деталей за выбранный период"""
    sql = '''
          SELECT "Название бизнес-сферы",
                dashboard.material."Группа материалов",
                "Наименование склада",
                round(sum("Сумма во внутренней валюте по дебе")) AS "Дебет", 
                round(sum("Сумма во внутренней валюте по кред")) AS "Кредит",
                round(sum("Сумма во внутренней валюте по дебе")) - round(sum("Сумма во внутренней валюте по кред")) AS "Изменение за период",
				count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
					 	ELSE null 
					END) AS "Количество_дебет",
                count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
					 	ELSE null 
					END) AS "Количество_кредит",
                count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
					 	ELSE null 
					END) - 
				count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
					 	ELSE null 
					END) AS "Изменение количества"
            FROM dashboard.osv_94
                LEFT JOIN dashboard.material
                    ON dashboard.osv_94."Материал" = '00000000'||dashboard.material."Код материала"
            WHERE TO_DATE("Дата ввода", 'YYYYMMDD') BETWEEN %s AND %s
            GROUP BY "Название бизнес-сферы",
                     dashboard.material."Группа материалов",
                     "Наименование склада"
    ''' % (start_date, end_date)
    print('1')
    if debug:
        print(sql)
    # return pd.read_sql(sql, con=engine_cons, params={"dstart":start_date,"dfinish":end_date})
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Выгрузка куба данных операций по счету 94* за выбранный период
def get_osv_data(start_date, end_date, debug = False):
    """Выгрузка куба данных операций по счету 94* за выбранный период"""
    sql = '''
          SELECT 			dashboard.osv_94."Дата проводки",
				initial_date,
				dashboard.osv_94."Название бизнес-сферы",
                dashboard.material."Группа материалов",
                dashboard.osv_94."Наименование склада",
                round(sum("Сумма во внутренней валюте по дебе")) AS "Дебет", 
                round(sum("Сумма во внутренней валюте по кред")) AS "Кредит",
                round(sum("Сумма во внутренней валюте по дебе") - sum("Сумма во внутренней валюте по кред")) AS "Изменение за период",
				count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
					 	ELSE null 
					END) AS "Количество_дебет",
                count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
					 	ELSE null 
					END) AS "Количество_кредит",
                count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по кред" < 0 then 1
					 	ELSE null 
					END) - 
				count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
					 	WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
					 	ELSE null 
					END) AS "Изменение количества",
				a.cumsum_filial,
				b.cumsum_det_type,
				c.cumsum_sklad,
				d.cumsum,
				e.cumsum_filial_count,
				f.cumsum_det_type_count,
				g.cumsum_sklad_count,
				h.cumsum_count
            FROM dashboard.osv_94
                LEFT JOIN dashboard.material
                    ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
				LEFT JOIN (
					SELECT  "Дата проводки",
							"Название бизнес-сферы",
							sum(round(sum("Сумма во внутренней валюте по дебе") - 
		   					sum("Сумма во внутренней валюте по кред"))) 
		   					over (partition by "Название бизнес-сферы"
								  order by "Дата проводки" 
								  rows between unbounded preceding and current row) AS cumsum_filial
					FROM dashboard.osv_94
					GROUP BY "Дата проводки",
							 "Название бизнес-сферы"
				) a
					ON a."Дата проводки" = dashboard.osv_94."Дата проводки"
						AND a."Название бизнес-сферы" = dashboard.osv_94."Название бизнес-сферы"
				LEFT JOIN (
					SELECT "Дата проводки",
							dashboard.material."Группа материалов",
							sum(round(sum("Сумма во внутренней валюте по дебе") - 
		   					sum("Сумма во внутренней валюте по кред"))) 
		   					over (partition by "Группа материалов" 
								  order by "Дата проводки" 
								  rows between unbounded preceding and current row) AS cumsum_det_type
					FROM dashboard.osv_94
						LEFT JOIN dashboard.material
							ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
					GROUP BY "Дата проводки",
							 "Группа материалов"
				) b
					ON b."Дата проводки" = dashboard.osv_94."Дата проводки"
						AND b."Группа материалов" = dashboard.material."Группа материалов"
				LEFT JOIN (
					SELECT  "Дата проводки",
							"Наименование склада",
							sum(round(sum("Сумма во внутренней валюте по дебе") - 
		   					sum("Сумма во внутренней валюте по кред"))) 
		   					over (partition by "Наименование склада" 
								  order by "Дата проводки" 
								  rows between unbounded preceding and current row) AS cumsum_sklad
					FROM dashboard.osv_94
					GROUP BY "Дата проводки",
							 "Наименование склада"
				) c
					ON c."Дата проводки" = dashboard.osv_94."Дата проводки"
						AND c."Наименование склада" = dashboard.osv_94."Наименование склада"
				LEFT JOIN (
					SELECT  "Дата проводки",
							sum(round(sum("Сумма во внутренней валюте по дебе") - 
		   					sum("Сумма во внутренней валюте по кред"))) 
		   					over (order by "Дата проводки" rows between unbounded preceding and current row) AS cumsum
					FROM dashboard.osv_94
					GROUP BY "Дата проводки"
				) d
					ON d."Дата проводки" = dashboard.osv_94."Дата проводки"
				LEFT JOIN (
					SELECT  "Дата проводки",
							"Название бизнес-сферы",
							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
									WHEN "Сумма во внутренней валюте по кред" < 0 then 1
									ELSE null 
								END) - 
							count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
									WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
									ELSE null 
								END))
							over (partition by "Название бизнес-сферы" 
			 	 				  order by "Дата проводки" 
			  					  rows between unbounded preceding and current row) AS cumsum_filial_count
						FROM dashboard.osv_94
						GROUP BY "Дата проводки",
							 	 "Название бизнес-сферы"
				) e
					ON e."Дата проводки" = dashboard.osv_94."Дата проводки"
						AND e."Название бизнес-сферы" = dashboard.osv_94."Название бизнес-сферы"
					LEFT JOIN (
					SELECT  "Дата проводки",
							dashboard.material."Группа материалов",
							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
                                    WHEN "Сумма во внутренней валюте по кред" < 0 then 1
                                    ELSE null 
                                END) - 
                            count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
                                    WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
                                    ELSE null 
                                END))
							over (partition by "Группа материалов" 
			 	 				  order by "Дата проводки" 
			  					  rows between unbounded preceding and current row) AS cumsum_det_type_count
						FROM dashboard.osv_94
							LEFT JOIN dashboard.material
								ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
						GROUP BY "Дата проводки",
							 	 "Группа материалов"
				) f
					ON f."Дата проводки" = dashboard.osv_94."Дата проводки"
						AND f."Группа материалов" = dashboard.material."Группа материалов"
				LEFT JOIN (
					SELECT  "Дата проводки",
							"Наименование склада",
							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
									WHEN "Сумма во внутренней валюте по кред" < 0 then 1
									ELSE null 
								END) - 
							count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
									WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
									ELSE null 
								END))
							over (partition by "Наименование склада" 
			 	 				  order by "Дата проводки" 
			  					  rows between unbounded preceding and current row) AS cumsum_sklad_count
						FROM dashboard.osv_94
						GROUP BY "Дата проводки",
							 	 "Наименование склада"
				) g
					ON g."Дата проводки" = dashboard.osv_94."Дата проводки"
						AND g."Наименование склада" = dashboard.osv_94."Наименование склада"
				LEFT JOIN (
					SELECT  "Дата проводки",
							sum(count(CASE WHEN "Сумма во внутренней валюте по дебе" > 0 then 1
									WHEN "Сумма во внутренней валюте по кред" < 0 then 1
									ELSE null 
								END) - 
							count(CASE WHEN "Сумма во внутренней валюте по кред" > 0 then 1
									WHEN "Сумма во внутренней валюте по дебе" < 0 then 1
									ELSE null 
								END))
							over (order by "Дата проводки" 
			  					  rows between unbounded preceding and current row) AS cumsum_count
						FROM dashboard.osv_94
						GROUP BY "Дата проводки"
				) h
					ON h."Дата проводки" = dashboard.osv_94."Дата проводки"
				LEFT JOIN (
					SELECT "Название бизнес-сферы",
							"Группа материалов",
							"Наименование склада",
							max("Дата проводки") AS initial_date
					FROM dashboard.osv_94
						LEFT JOIN dashboard.material
							ON dashboard.osv_94."Материал" = dashboard.material."Код материала"
					WHERE TO_DATE("Дата проводки", 'YYYYMMDD') < '%s' 
					GROUP BY "Название бизнес-сферы",
							"Группа материалов",
							"Наименование склада"
					) i
				ON i."Название бизнес-сферы" = dashboard.osv_94."Название бизнес-сферы"
					AND i."Группа материалов" = dashboard.material."Группа материалов"
					AND i."Наименование склада" = dashboard.osv_94."Наименование склада"
            WHERE TO_DATE(dashboard.osv_94."Дата проводки", 'YYYYMMDD') BETWEEN '%s' AND '%s'
            GROUP BY dashboard.osv_94."Дата проводки",
					 dashboard.osv_94."Название бизнес-сферы",
                     dashboard.material."Группа материалов",
                     dashboard.osv_94."Наименование склада",
					 a.cumsum_filial,
					 b.cumsum_det_type,
					 c.cumsum_sklad,
					 d.cumsum,
					 e.cumsum_filial_count,
					 f.cumsum_det_type_count,
					 g.cumsum_sklad_count,
					 h.cumsum_count,
					 i.initial_date
    ''' % (str(start_date)[:10], str(start_date)[:10], str(end_date)[:10])
    if debug:
        print(sql)
    # return pd.read_sql(sql, con=engine_cons, params={"dstart":start_date,"dfinish":end_date})
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# Выгрузка оборота и количества операций по счету 94* за выбранный период для вкладки 4
def get_osv_detail_by_dates2(start_date, end_date, debug = False):
    """Выгрузка недостач деталей за период для вкладки 4"""
    sql = '''
          select "Дата ввода", sum("Сумма во внутренней валюте по дебе") as "Обороты по дебету", 
                sum("Сумма во внутренней валюте по кред") as "Обороты по кредиту", 
                    material."Группа материалов",
                    "Название бизнес-сферы" as "Филиал", "Наименование склада" as "Склад",  
                    sum(sign("Сумма во внутренней валюте по дебе")) as "Обороты по дебету, шт",
                    sum(sign("Сумма во внутренней валюте по кред")) as "Обороты по кредиту, шт"
                    
                    from dashboard.osv_94 
                    	left join dashboard.material on material."Код материала" = osv_94."Материал"::int::varchar
                           where "Дата ввода" between '{}' and '{}'
                                --and "Дата ввода" > '20180101'
                                    group by "Дата ввода", "Название бизнес-сферы", "Наименование склада"
                                        , material."Группа материалов"
    '''.format(dt.datetime.strftime(start_date, '%Y%m%d'), dt.datetime.strftime(end_date, '%Y%m%d'))
    if debug:
        print(sql)

    # return pd.read_sql(sql, con=engine_cons)
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения списка филиалов
def get_branch_names(debug = False):
    """Выгрузка списка филиалов"""
    sql = '''
        SELECT DISTINCT "Название бизнес-сферы"
        FROM dashboard.osv_94
        ORDER BY "Название бизнес-сферы" ASC
    '''
    if debug:
        print(sql)

    # return pd.read_sql(sql, con=engine_cons)
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# Значения списка типов запчастей
def get_detail_type_names(debug = False):
    """Выгрузка типов деталей"""
    sql = '''
        SELECT DISTINCT "Группа материалов"
        FROM dashboard.material
        ORDER BY "Группа материалов" ASC
    '''
    if debug:
        print(sql)

    # return pd.read_sql(sql, con=engine_cons)
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# Значения списка складов
def get_warehouse_names(debug = False):
    """Выгрузка списка складов"""
    sql = '''
        SELECT DISTINCT "Наименование склада", "Название бизнес-сферы"
        FROM dashboard.osv_94
        ORDER BY "Наименование склада" ASC
    '''
    if debug: print(sql)

    # return pd.read_sql(sql, con=engine_cons)
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# Максимальная дата в выгрузке
def get_max_date():
    """Максимальная дата в выгрузке"""
    sql = '''
    SELECT MAX(TO_DATE("Дата ввода", 'YYYYMMDD'))
    FROM dashboard.osv_94
    '''
    # return engine_cons.execute(sql).fetchone()[0]
    con = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]
