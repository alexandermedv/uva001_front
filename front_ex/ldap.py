from pprint import pprint
import os 

# Запрос на авторизацию пользователя в реестр LDAPS
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL, SAFE_SYNC
from ldap3.core import exceptions

from . import app

def ldap_authentication(login_id, login_password):
    server = Server(os.environ['LDAP_HOST'], port=int(os.environ['LDAP_PORT']), use_ssl=True, get_info=ALL)
    try:
        conn = Connection(server, user='PGK\\{login_id}'.format(login_id=login_id), password=login_password, auto_bind=True)
        # Уточнить необходимость
        # conn.bind()
    except exceptions.LDAPException as err:
        pprint(err)
        return False
    return True