
from wtforms import Field
from wtforms.widgets import TextInput

from io import StringIO
import csv

# Extentions in forms
class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(' ')]
        else:
            self.data = []

def get_postgre_con_str():
    """Строка подключения к postgre тест"""
    return "postgresql://locadm:Temp001@msc199-sdb04.domain.local:8036/uva_cons"

def get_sap_s4_con_str():
    """Строка подключения к S4 тест"""
    return "hana+pyhdb://PGKAUDIT:Rfh,jyfhf21@sap-db-s4q.sap.tc:30115"

# -- Подключение
def psql_insert_copy(table, conn, keys, data_iter):
    """Метод для загрузки датафрейма в postgre"""
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