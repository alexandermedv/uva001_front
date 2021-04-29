SELECT 
	a.bname AS "Логин",
	a.erdat AS "Дата создания",
	a.GLTGV AS "Действ. с", 
	a.GLTGB AS "Действ. по", 
	a.USTYP AS "Тип пользователя",
	a.CLASS AS "Группа",
	h.NAME_TEXT AS "ФИО",
	h.NAME_FIRST AS "Имя",
	h.NAME_LAST AS "Фамилия",
	h.DEPARTMENT AS "Отдел",
	h.FUNCTION AS "Функция",
	to_date(b.logon_date, 'YYYYMMDD') AS "Дата последнего входа",
	(CASE WHEN b.logon_date IS NOT NULL 
	 	THEN
	(SELECT max(to_date(logon_date, 'YYYYMMDD')) FROM sap_s4.usr41) -
	to_date(b.logon_date, 'YYYYMMDD') 
		ELSE
		(SELECT max(to_date(logon_date, 'YYYYMMDD')) FROM sap_s4.usr41) -
			to_date(a.erdat, 'YYYYMMDD')
		END) AS "Количество дней неактивности"

FROM sap_s4.usr02 a
	LEFT JOIN sap_s4.usr41 b
		ON a.bname = b.bname
	LEFT JOIN sap_s4.USR21 g
		ON a.bname = g.bname
	LEFT JOIN sap_s4.v_addr_usr h
		ON h.persnumber = g.persnumber
WHERE a.mandt = %(mandt)s
AND (
	(SELECT max(to_date(logon_date, 'YYYYMMDD')) FROM sap_s4.usr41) -
	to_date(b.logon_date, 'YYYYMMDD') >= 60
	OR (b.logon_date IS NULL AND 
		(SELECT max(to_date(logon_date, 'YYYYMMDD')) FROM sap_s4.usr41) -
			to_date(a.erdat, 'YYYYMMDD') >= 60)
	)