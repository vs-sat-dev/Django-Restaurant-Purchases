#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python telegram_bot/dispatcher.py
#python manage.py collectstatic
gunicorn restaurant_purchases.wsgi:application --bind 0.0.0.0:8000
#gunicorn restaurant_purchases.wsgi:application --bind 68.183.201.244:8000