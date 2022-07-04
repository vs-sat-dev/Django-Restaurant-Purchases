#!/bin/sh
#python manage.py makemigrations
#python manage.py migrate
python telegram_bot/dispatcher.py &
python telegram_bot2/dispatcher.py &
celery -A restaurant_purchases worker -l INFO &
#python manage.py dumpdata --format json -e contenttypes > data.json
#python manage.py dbbackup
#celery -A restaurant_purchases flower --address=0.0.0.0 --port=5555 &
#celery --app=restaurant_purchases.celery:app flower
#celery flower --url_prefix=flower &
#python manage.py collectstatic
gunicorn restaurant_purchases.wsgi:application --bind 0.0.0.0:8000
#gunicorn restaurant_purchases.wsgi:application --bind 68.183.201.244:8000

