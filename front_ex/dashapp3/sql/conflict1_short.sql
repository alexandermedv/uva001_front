SELECT DISTINCT
f.bname AS "Логин",
f.GLTGV AS "Действ. с", 
f.GLTGB AS "Действ. по", 
f.USTYP AS "Тип пользователя",
f.CLASS AS "Группа",
h.NAME_TEXT AS "ФИО",
h.NAME_FIRST AS "Имя",
h.NAME_LAST AS "Фамилия",
h.DEPARTMENT AS "Отдел",
h.FUNCTION AS "Функция"
FROM (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_TCODE'
		AND FIELD = 'TCD'
		AND LOW = 'SU01'
		AND DELETED IS NULL
		AND MANDT = %(mandt)s) a
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_USER_GRP'
		AND FIELD = 'ACTVT'
		AND (LOW = '01' OR LOW = '02' OR LOW = '06' OR LOW = '22')
		AND DELETED IS NULL
		AND MANDT = %(mandt)s) b
	ON a.agr_NAME = b.agr_NAME
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_USER_PRO'
		AND FIELD = 'ACTVT'
		AND LOW = '22'
		AND DELETED IS NULL
		AND MANDT = %(mandt)s) c
	ON a.AGR_NAME = c.AGR_NAME
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_USER_AGR'
		AND FIELD = 'ACTVT'
		AND LOW = '22'
		AND DELETED IS NULL
		AND MANDT = %(mandt)s) d
	ON a.AGR_NAME = d.AGR_NAME
	LEFT JOIN sap_s4.agr_users e
	ON a.AGR_NAME = e.agr_name
	LEFT JOIN sap_s4.usr02 f
	ON e.uname = f.bname
	LEFT JOIN sap_s4.USR21 g
	ON f.bname = g.bname
	LEFT JOIN sap_s4.v_addr_usr h
	ON h.persnumber = g.persnumber
WHERE f.bname IS NOT NULL