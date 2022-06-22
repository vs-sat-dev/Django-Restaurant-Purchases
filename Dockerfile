FROM python:3.10.4
WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY ./celery/worker/start /usr/src/app
RUN sed -i 's/\r$//g' ./start
RUN chmod +x ./start

COPY entrypoint.sh /usr/src/app
ENTRYPOINT ["sh", "entrypoint.sh"]