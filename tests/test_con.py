from sqlalchemy import create_engine
import pandas as pd

sql = "select * from sap_s4.limit_oper"
limit_oper_data = pd.read_sql(sql, create_engine("postgresql://locadm:Temp001@msc199-sdb04.domain.local:8036/uva_cons", max_identifier_length=128, encoding='utf-8'))
print (limit_oper_data.head(3))