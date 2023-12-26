<!-- Релизы -->
PGK-260 v0.005 Релиз - выход на новое доменное имя msc199-sas40

<!-- Help -->

Добавлены переменные окружения
Следующие шаги
Необходимо переопределить связи с дэшбордами из ics

# Капсула вы выгрузкой отчетов и расчетных задач
<!-- Запуск Develop -->

docker-compose up -d --build

<!--Запуск Prod -->
Инициализация базы данных:
export FLASK_APP=wsgi_prod.py

flask db migrate
flask db upgrade

docker-compose -f docker-compose.prod.yml up -d --build


<!-- Сертификация NGINX -->
Пароль: INC0223850

Перейдем в директорию, где расположен данный файл (например /root/site_certs/)

[root@server ~]# cd /root/site_certs/
Получим цепочку сертификатов

[root@server certs]# openssl pkcs12 -in cert.pfx -clcerts -nokeys -out public.crt
Получим приватный ключ

[root@server certs]# openssl pkcs12 -in cert.pfx -nocerts -nodes -out private.key

Установка
https://cyber01.ru/ustanovka-ssl-sertifikata-na-nginx/
https://www.leaderssl.ru/articles/224-ssl-nginx-ustanavlivaem-ssl-sertifikat-na-server-nginx


Доступ к папкам:
sudo setfacl -m u:svc_fs-uva:rwx dag_tm_transportaions.py

https://github.com/microsoft/vscode-python/releases/tag/2021.12.1559732655

