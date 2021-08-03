from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL, SAFE_SYNC
import requests

server = Server(host='msc00-sdc01.pgk.rzd', port=636, use_ssl=True, get_info=ALL)
# conn = Connection(server, user='svc_fs-uva', password='Hfesb#th45xao$qhjkc', auto_bind=True)
# conn =Connection(server, user='svc_fs-uva', password='Hfesb#th45xao$qhjkc', client_strategy=SAFE_SYNC, auto_bind=True)
conn =Connection(server, user='PGK\\turganovai', password='Savage11', auto_bind=True)

print('Соединение установлено')
# status, result, response, _ = conn.search('o=test', '(objectclass=*)')
print(server.info)
print(conn)
print('bind', conn.bind())
# 
print(conn.extend.standard.who_am_i())
# print(requests.environ.get('REMOTE_USER')) 