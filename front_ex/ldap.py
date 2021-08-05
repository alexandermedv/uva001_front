# Запрос на авторизацию пользователя в реестр LDAPS
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL, SAFE_SYNC

from . import app

def ldap_authentication(login_id, login_password):
    server = Server(host='msc00-sdc01.pgk.rzd', port=636, use_ssl=True, get_info=ALL)
    conn = Connection(server, user='PGK\\{login_id}'.format(login_id=login_id), password=login_password, auto_bind=True)
    return conn.bind()
