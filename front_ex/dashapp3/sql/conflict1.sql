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
h.FUNCTION AS "Функция",
a.AGR_NAME AS "Роль1",
a.object AS "Объект1",
a.field AS "Поле1",
a.low AS "Значение1",
a.high AS "Верх_значение1",
b.object AS "Объект2",
b.field AS "Поле2",
b.low AS "Значение2",
b.high AS "Верх_значение2",
c.object AS "Объект3",
c.field AS "Поле3",
c.low AS "Значение3",
c.high AS "Верх_значение3",
d.object AS "Объект4",
d.field AS "Поле4",
d.low AS "Значение4",
d.high AS "Верх_значение4"
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