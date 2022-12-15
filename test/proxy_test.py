import requests
# proxies = {
#    'http': 'http://msc01-afw01.pgk.rzd:9090',
#    'https': 'http://msc01-afw01.pgk.rzd:9090',
# }
url = 'https://api.spark-interfax.ru/IfaxWebService/'
request = requests.get(url)
print (request.json)

# curl -x http://msc01-cfw01.pgk.rzd:9090 https://api.spark-interfax.ru/IfaxWebService/
