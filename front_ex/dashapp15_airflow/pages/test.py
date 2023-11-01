import requests

res = requests.get('http://msc199-sdb04.domain.local:9002/api/reports/report_test')

task_id = res.task_id

task_check = requests.get('http://msc199-sdb04.domain.local:9002/api/reports/report_test')
