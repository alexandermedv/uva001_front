import requests

# proxies = {
#    'http': 'http://msc01-afw01.pgk.rzd:9090',
#    'https': 'http://msc01-afw01.pgk.rzd:9090',
# }
url = 'http://ipwho.is/88.234.224.146'
request = requests.get(url)
print(request.json)
