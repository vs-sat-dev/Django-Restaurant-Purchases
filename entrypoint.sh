#!/bin/sh

python manage.py migrate
python manage.py collectstatic
gunicorn restaurant_purchases.wsgi:application --bind 0.0.0.0:8000