from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from time import sleep


@shared_task
def test_task():
    with open('file.txt', 'w') as file:
        file.write('LogStart')
        sleep(100)
        file.write('LogEnd')
    """with open('file.txt', 'w') as file:
        file.write('LogStart')
        #sleep(10)
        file.write('LogEnd')"""

    return None
