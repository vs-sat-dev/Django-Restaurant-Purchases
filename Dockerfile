FROM python:3.10.4
WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
RUN pip install Redis
RUN pip install eventlet
RUN pip install flower

RUN python manage.py makemigrations
RUN python manage.py migrate

#COPY celery_worker /usr/src/app
#RUN sed -i 's/\r$//g' celery_worker
#RUN chmod +x celery_worker

#COPY entrypoint.sh /usr/src/app
#ENTRYPOINT ["sh", "entrypoint.sh"]