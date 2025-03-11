SELECT  
f.bname, 
f.GLTGV, 
f.GLTGB, 
f.USTYP,
a.AGR_NAME,
a.object,
a.field,
a.low,
a.high,
b.object,
b.field,
b.low,
b.high,
c.object,
c.field,
c.low,
c.high,
d.object,
d.field,
d.low,
d.high,
g.object,
g.field,
g.low,
g.high
FROM (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_TCODE'
		AND FIELD = 'TCD'
		AND LOW = 'PFCG'
		AND DELETED IS NULL
		AND MANDT = '315') a
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_USER_AGR'
		AND FIELD = 'ACTVT'
		AND (LOW = '22' OR LOW = '78')
		AND DELETED IS NULL
		AND MANDT = '315') b
	ON a.agr_NAME = b.agr_NAME
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_USER_GRP'
		AND FIELD = 'ACTVT'
		AND (LOW = '02' OR LOW = '22' OR LOW = '78')
		AND DELETED IS NULL
		AND MANDT = '315') c
	ON a.agr_NAME = c.agr_NAME
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_USER_GRP'
		AND FIELD = 'CLASS'
		AND LOW = '*'
		AND DELETED IS NULL
		AND MANDT = '315') d
	ON a.agr_NAME = d.agr_NAME
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_USER_PRO'
		AND FIELD = 'ACTVT'
		AND LOW = '22'
		AND DELETED IS NULL
		AND MANDT = '315') g
	ON a.agr_NAME = g.agr_NAME
	LEFT JOIN sap_s4.agr_users e
	ON a.AGR_NAME = e.agr_name
	left join sap_s4.usr02 f
	ON e.uname = f.bname
WHERE bname IS NOT NULL