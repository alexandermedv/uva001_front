FROM python:3.7.4
LABEL maintainer "Турганов Артем TurganovAI@pgkweb.ru"

USER root

WORKDIR /opt/fron_ex
RUN pip install --upgrade pip
COPY requirements.txt /opt/fron_ex/requirements.txt

RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /opt/fron_ex/entrypoint.sh

# copy project
COPY . /opt/fron_ex

# run entrypoint.sh
ENTRYPOINT ["sh", "/opt/fron_ex/entrypoint.sh"]

EXPOSE 9102