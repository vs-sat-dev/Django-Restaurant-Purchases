#!/bin/sh

python manage.py migrate
python manage.py collectstatic
gunicorn restaurant_purchases.wsgi:application --bind 68.183.201.244:8000