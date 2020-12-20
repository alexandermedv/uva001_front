# Заглушка, чтобы прописать внешнюю папку
import sys
from os import path
import datetime as dt

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
print('path', path.dirname(path.dirname(path.abspath(__file__))))

# так работает
# from front_ex.dash_osv.utils import get_osv_detail_by_dates

from front_ex.dash_osv_dev.utils import get_osv_detail_by_dates

df = get_osv_detail_by_dates(dt.datetime.strptime('20200226', '%Y%m%d'), dt.datetime.strptime('20200228', '%Y%m%d'), debug=True)
print(df.head())
print(df.info())