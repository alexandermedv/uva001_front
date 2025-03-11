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
b.high
FROM (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_TCODE'
		AND FIELD = 'TCD'
		AND (LOW = 'SE80' OR LOW = 'SE84')
		AND DELETED IS NULL
		AND MANDT = '315') a
	INNER JOIN (SELECT * 
		FROM sap_s4.agr_1251
		WHERE OBJECT = 'S_DEVELOP'
		AND FIELD = 'ACTVT'
		AND (LOW = '01' OR LOW = '02' OR LOW = '06' OR LOW = '07')
		AND DELETED IS NULL
		AND MANDT = '315') b
	ON a.agr_NAME = b.agr_NAME
	LEFT JOIN sap_s4.agr_users e
	ON a.AGR_NAME = e.agr_name
	left join sap_s4.usr02 f
	ON e.uname = f.bname
WHERE bname IS NOT NULL