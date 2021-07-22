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
export FLASK_ENV=Prod

flask db migrate
flask db upgrade

docker-compose -f docker-compose.prod.yml up -d --build
