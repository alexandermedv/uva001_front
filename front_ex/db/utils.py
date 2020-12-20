import csv, sys, os
from io import StringIO
import pyhdb
import time

# -- Подключение 
def psql_insert_copy(table, conn, keys, data_iter):
 
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection

    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

def get_postgre_con_str():
    return "postgresql://locadm:Temp001@msc199-sdb04.domain.local:8031/uva_cons"