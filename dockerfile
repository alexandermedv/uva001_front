FROM python:3.7.4
LABEL maintainer "Турганов Артем TurganovAI@pgkweb.ru"

USER root

RUN pip install --upgrade pip
COPY . /app  

WORKDIR /app
RUN pip install -r requirements.txt

# set TZ Moscow time
ENV TZ Europe/Moscow
RUN apt-get install tzdata
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ >/etc/timezone 

# run entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

EXPOSE 9102